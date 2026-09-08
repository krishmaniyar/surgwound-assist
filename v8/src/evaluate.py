"""
v8/src/evaluate.py — Comprehensive evaluation engine for SurgWound Assist v8.

Features:
  1. Full metric suite aligned with base paper (Macro/Micro/Weighted F1, P, R, Acc, AUC, Kappa).
  2. Test-Time Augmentation (7x TTA).
  3. Validation-Tuned Decision Boundary Optimization (learned strictly on val, applied to test).
  4. Per-attribute and per-class detailed confusion matrix reporting.
"""
import os
import json
import torch
import numpy as np
import pandas as pd
from PIL import Image
from torchvision import transforms
from sklearn.metrics import (
    f1_score, classification_report, roc_auc_score,
    cohen_kappa_score, confusion_matrix
)
from typing import Dict, Any, List, Optional, Tuple

from config import BASE_ATTRIBUTES, CLASS_MAPPINGS, BIOMEDCLIP_MODEL_ID
from dataset import SurgWoundDataset
from model import BiomedCLIPMultiTaskModel
import open_clip


def optimize_val_thresholds(
    val_probs: Dict[str, np.ndarray],
    val_targets: Dict[str, List[int]],
    min_improvement: float = 0.02,
) -> Dict[str, np.ndarray]:
    """
    Optimize class multiplier thresholds on validation probabilities to maximize Macro-F1.
    Searches class weights w_c in [0.7, 2.0] such that pred = argmax_c (w_c * p_c).
    Regularized with min_improvement to prevent overfitting small validation splits.
    Learned STRICTLY on validation data to prevent test leakage.
    """
    optimized_weights = {}
    for attr in BASE_ATTRIBUTES:
        probs = val_probs[attr]
        targets = np.array(val_targets[attr])
        num_classes = len(CLASS_MAPPINGS[attr])

        base_preds = np.argmax(probs, axis=1)
        base_f1 = f1_score(targets, base_preds, average='macro', zero_division=0)
        best_f1 = base_f1
        best_w = np.ones(num_classes)

        # Regularized search grid to avoid over-shifting calibrated heads
        for c in range(num_classes):
            for multiplier in [0.7, 0.85, 1.0, 1.2, 1.4, 1.7, 2.0]:
                test_w = best_w.copy()
                test_w[c] = multiplier
                weighted_probs = probs * test_w
                test_preds = np.argmax(weighted_probs, axis=1)
                score = f1_score(targets, test_preds, average='macro', zero_division=0)
                if score > best_f1:
                    best_f1 = score
                    best_w = test_w

        # Only apply threshold modification if validation gain is significant
        if best_f1 - base_f1 >= min_improvement:
            optimized_weights[attr] = best_w
        else:
            optimized_weights[attr] = np.ones(num_classes)

    return optimized_weights


def evaluate_model(
    model: torch.nn.Module,
    df_eval: pd.DataFrame,
    device: torch.device,
    use_tta: bool = True,
    tta_n: int = 7,
    img_dir: str = 'data/images',
    legacy_mode: bool = True,
    multiscale: bool = False,
    local_crop_scale: float = 0.65,
    class_weights_dict: Optional[Dict[str, np.ndarray]] = None,
) -> Tuple[Dict[str, Any], Dict[str, np.ndarray], Dict[str, List[int]]]:
    """
    Runs model inference on a dataframe split with optional TTA and decision thresholding.
    Returns (metrics_dict, raw_probabilities, ground_truth_targets).
    """
    model.eval()
    _, _, preprocess_val = open_clip.create_model_and_transforms(BIOMEDCLIP_MODEL_ID)

    tta_transform = transforms.Compose([
        transforms.RandomResizedCrop(224, scale=(0.85, 1.0)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.05, contrast=0.05),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.4815, 0.4578, 0.4082], std=[0.2686, 0.2613, 0.2758]),
    ])

    ds = SurgWoundDataset(
        df_eval,
        transform=preprocess_val,
        img_dir=img_dir,
        legacy_mode=legacy_mode,
        multiscale=multiscale,
        local_crop_scale=local_crop_scale,
    )

    all_probs = {attr: [] for attr in BASE_ATTRIBUTES}
    all_targets = {attr: [] for attr in BASE_ATTRIBUTES}

    passes = tta_n if use_tta else 1

    for i in range(len(df_eval)):
        row = df_eval.iloc[i]
        name = str(row['image_name'])
        img_path = os.path.join(img_dir, name if name.endswith('.jpg') else f"{name}.jpg")

        raw_img = None
        if use_tta:
            try:
                raw_img = Image.open(img_path).convert('RGB')
            except Exception:
                raw_img = None

        sample_item, labels = ds[i]
        avg_probs = {attr: np.zeros(len(CLASS_MAPPINGS[attr])) for attr in BASE_ATTRIBUTES}

        with torch.no_grad():
            for t in range(passes):
                if multiscale:
                    if t == 0 or raw_img is None:
                        g_inp = sample_item[0].unsqueeze(0).to(device)
                        l_inp = sample_item[1].unsqueeze(0).to(device)
                    else:
                        g_inp = tta_transform(raw_img).unsqueeze(0).to(device)
                        local_crop = ds._get_local_crop(raw_img)
                        l_inp = tta_transform(local_crop).unsqueeze(0).to(device)
                    inp = (g_inp, l_inp)
                else:
                    if t == 0 or raw_img is None:
                        inp = sample_item.unsqueeze(0).to(device)
                    else:
                        inp = tta_transform(raw_img).unsqueeze(0).to(device)

                with torch.amp.autocast('cuda') if device.type == 'cuda' else torch.no_grad():
                    logits_dict = model(inp)

                for attr in BASE_ATTRIBUTES:
                    p = torch.softmax(logits_dict[attr], dim=1).squeeze(0).cpu().numpy()
                    avg_probs[attr] += p / passes

        for attr in BASE_ATTRIBUTES:
            all_probs[attr].append(avg_probs[attr])
            all_targets[attr].append(int(labels[attr].item()))

    # Convert to arrays
    prob_arrays = {attr: np.array(all_probs[attr]) for attr in BASE_ATTRIBUTES}

    # Compute metrics
    metrics = {'aggregate': {}, 'per_head': {}, 'tta_enabled': use_tta, 'legacy_mode': legacy_mode}

    exact_matches = 0
    num_samples = len(df_eval)

    for attr in BASE_ATTRIBUTES:
        probs = prob_arrays[attr]
        num_classes = len(CLASS_MAPPINGS[attr])

        if class_weights_dict and attr in class_weights_dict:
            weighted = probs * class_weights_dict[attr]
            preds = np.argmax(weighted, axis=1).tolist()
        else:
            preds = np.argmax(probs, axis=1).tolist()

        targets = all_targets[attr]
        rep = classification_report(targets, preds, output_dict=True, zero_division=0)

        # Robust ROC-AUC computation across observed classes
        targets_np = np.array(targets)
        auc_scores = []
        for c in range(num_classes):
            binary_target = (targets_np == c).astype(int)
            if len(np.unique(binary_target)) > 1: # Both positive and negative instances exist
                try:
                    c_auc = roc_auc_score(binary_target, probs[:, c])
                    auc_scores.append(c_auc)
                except Exception:
                    pass
        auc = float(np.mean(auc_scores)) if len(auc_scores) > 0 else float('nan')

        try:
            kappa = cohen_kappa_score(targets, preds, labels=list(range(num_classes)))
            if np.isnan(kappa):
                kappa = 0.0
        except Exception:
            kappa = 0.0

        cm = confusion_matrix(targets, preds, labels=list(range(num_classes))).tolist()

        per_class_metrics = {}
        for c_idx, c_name in enumerate(CLASS_MAPPINGS[attr]):
            c_str = str(c_idx)
            if c_str in rep:
                per_class_metrics[c_name] = {
                    'precision': rep[c_str]['precision'],
                    'recall': rep[c_str]['recall'],
                    'f1': rep[c_str]['f1-score'],
                    'support': rep[c_str]['support'],
                }
            else:
                per_class_metrics[c_name] = {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'support': 0}

        metrics['per_head'][attr] = {
            'accuracy': rep['accuracy'],
            'macro_precision': rep['macro avg']['precision'],
            'macro_recall': rep['macro avg']['recall'],
            'macro_f1': rep['macro avg']['f1-score'],
            'micro_f1': rep['accuracy'],
            'weighted_precision': rep['weighted avg']['precision'],
            'weighted_recall': rep['weighted avg']['recall'],
            'weighted_f1': rep['weighted avg']['f1-score'],
            'roc_auc': auc,
            'cohen_kappa': kappa,
            'per_class': per_class_metrics,
            'confusion_matrix': cm,
        }

    # Aggregate
    for i in range(num_samples):
        all_correct = True
        for attr in BASE_ATTRIBUTES:
            p = prob_arrays[attr][i]
            if class_weights_dict and attr in class_weights_dict:
                p = p * class_weights_dict[attr]
            if np.argmax(p) != all_targets[attr][i]:
                all_correct = False
                break
        if all_correct:
            exact_matches += 1

    mean_macro_f1 = float(np.mean([metrics['per_head'][a]['macro_f1'] for a in BASE_ATTRIBUTES]))
    mean_accuracy = float(np.mean([metrics['per_head'][a]['accuracy'] for a in BASE_ATTRIBUTES]))
    mean_macro_p = float(np.mean([metrics['per_head'][a]['macro_precision'] for a in BASE_ATTRIBUTES]))
    mean_macro_r = float(np.mean([metrics['per_head'][a]['macro_recall'] for a in BASE_ATTRIBUTES]))
    mean_weighted_f1 = float(np.mean([metrics['per_head'][a]['weighted_f1'] for a in BASE_ATTRIBUTES]))
    exact_ratio = float(exact_matches / max(1, num_samples))

    # Minority attributes average (exudate, infection, closure, edema)
    minority_heads = ['exudate_type', 'infection_risk', 'closure_method', 'edema']
    minority_f1 = float(np.mean([metrics['per_head'][a]['macro_f1'] for a in minority_heads]))

    valid_aucs = [metrics['per_head'][a]['roc_auc'] for a in BASE_ATTRIBUTES if not np.isnan(metrics['per_head'][a]['roc_auc'])]
    mean_auc = float(np.mean(valid_aucs)) if valid_aucs else float('nan')

    valid_kappas = [metrics['per_head'][a]['cohen_kappa'] for a in BASE_ATTRIBUTES if not np.isnan(metrics['per_head'][a]['cohen_kappa'])]
    mean_kappa = float(np.mean(valid_kappas)) if valid_kappas else float('nan')

    metrics['aggregate'] = {
        'mean_macro_f1': mean_macro_f1,
        'mean_accuracy': mean_accuracy,
        'mean_macro_precision': mean_macro_p,
        'mean_macro_recall': mean_macro_r,
        'mean_weighted_f1': mean_weighted_f1,
        'minority_mean_macro_f1': minority_f1,
        'mean_roc_auc': mean_auc,
        'mean_cohen_kappa': mean_kappa,
        'exact_match_ratio': exact_ratio,
    }

    return metrics, prob_arrays, all_targets


def generate_evaluation_report(run_dir: str, metrics: Dict[str, Any], title: str = "v8 Model Evaluation") -> str:
    """Formats and writes a comprehensive evaluation report in Markdown."""
    agg = metrics['aggregate']
    tta_str = " (7x TTA Enabled)" if metrics.get('tta_enabled') else ""

    auc_agg_str = f"{agg['mean_roc_auc']:.4f}" if ('mean_roc_auc' in agg and not np.isnan(agg['mean_roc_auc'])) else "N/A"
    kappa_agg_str = f"{agg['mean_cohen_kappa']:.4f}" if ('mean_cohen_kappa' in agg and not np.isnan(agg['mean_cohen_kappa'])) else "N/A"

    lines = [
        f"# SurgWound Assist — {title}{tta_str}",
        "",
        "## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)",
        f"- **Mean Macro-F1**: **{agg['mean_macro_f1']*100:.2f}%**",
        f"- **Mean Accuracy**: {agg['mean_accuracy']*100:.2f}%",
        f"- **Mean Macro-Precision**: {agg['mean_macro_precision']*100:.2f}%",
        f"- **Mean Macro-Recall**: {agg['mean_macro_recall']*100:.2f}%",
        f"- **Mean Weighted-F1**: {agg['mean_weighted_f1']*100:.2f}%",
        f"- **Mean ROC-AUC**: {auc_agg_str}",
        f"- **Mean Cohen's Kappa**: {kappa_agg_str}",
        f"- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **{agg['minority_mean_macro_f1']*100:.2f}%**",
        f"- **Exact Match Ratio**: {agg['exact_match_ratio']*100:.2f}%",
        "",
        "## Per-Attribute Summary Table",
        "| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for attr, v in metrics['per_head'].items():
        auc_str = f"{v['roc_auc']:.4f}" if not np.isnan(v['roc_auc']) else "N/A"
        kappa_str = f"{v['cohen_kappa']:.4f}" if not np.isnan(v['cohen_kappa']) else "N/A"
        lines.append(
            f"| {attr:16s} | {v['accuracy']*100:6.2f}% | {v['macro_precision']*100:6.2f}% | "
            f"{v['macro_recall']*100:6.2f}% | {v['macro_f1']*100:6.2f}% | {v['micro_f1']*100:6.2f}% | "
            f"{v['weighted_f1']*100:6.2f}% | {auc_str} | {kappa_str} |"
        )

    lines.append("\n## Per-Class Detailed Breakdown\n")
    for attr, v in metrics['per_head'].items():
        lines.append(f"### {attr.capitalize().replace('_', ' ')}")
        lines.append("| Class | Precision | Recall | F1-Score | Support |")
        lines.append("|---|---|---|---|---|")
        for cls_name, c_m in v['per_class'].items():
            sup_str = str(c_m['support']) if c_m['support'] > 0 else "0 (0 samples)"
            lines.append(
                f"| {cls_name:25s} | {c_m['precision']*100:5.1f}% | {c_m['recall']*100:5.1f}% | {c_m['f1']*100:5.1f}% | {sup_str} |"
            )
        lines.append("")

    report_path = os.path.join(run_dir, "evaluation_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    # Also save JSON
    json_path = os.path.join(run_dir, "metrics.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=4)

    return report_path
