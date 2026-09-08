"""
evaluate.py — Generate detailed metrics for the End-to-End Fine-Tuned model.
"""
import os
import json
import torch
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, roc_auc_score, cohen_kappa_score, confusion_matrix
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS
from dataset import RawImageDataset
from models import EndToEndWoundModel
from calibrate import ECELoss

def compute_ece(probs: np.ndarray, targets: np.ndarray) -> float:
    ece_fn = ECELoss()
    logits = np.log(np.clip(probs, 1e-15, 1.0))
    return ece_fn(
        torch.tensor(logits, dtype=torch.float32),
        torch.tensor(targets, dtype=torch.long)
    ).item()

def run_evaluation(run_dir: str, df: pd.DataFrame):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    df_test = df[df['split'] == 'test'].reset_index(drop=True)
    if len(df_test) == 0:
        print("[WARN] No test set found! Evaluating on validation set instead.")
        df_test = df[df['split'] == 'val'].reset_index(drop=True)

    ds_test = RawImageDataset(df_test, augment=False)
    metrics = {'aggregate': {}, 'per_head': {}}
    
    ckpt_path = os.path.join(run_dir, "checkpoints", "end_to_end_model.pth")
    
    model = EndToEndWoundModel().to(device)
    if os.path.exists(ckpt_path):
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
    else:
        print(f"[WARN] Missing checkpoint {ckpt_path}!")
        
    model.eval()
    
    all_attr_preds = {attr: [] for attr in BASE_ATTRIBUTES}
    all_attr_probs = {attr: [] for attr in BASE_ATTRIBUTES}
    all_attr_targets = {attr: [] for attr in BASE_ATTRIBUTES}
    
    with torch.no_grad():
        for i in range(len(ds_test)):
            pixel_values, labs = ds_test[i]
            pixel_values = pixel_values.unsqueeze(0).to(device)
            
            logits_dict = model(pixel_values)
            
            for attr in BASE_ATTRIBUTES:
                prob = torch.softmax(logits_dict[attr], dim=1).squeeze(0).cpu().numpy()
                all_attr_probs[attr].append(prob)
                all_attr_preds[attr].append(int(np.argmax(prob)))
                all_attr_targets[attr].append(int(labs[attr].item()))
                
    for attr in BASE_ATTRIBUTES:
        probs = np.array(all_attr_probs[attr])
        preds = all_attr_preds[attr]
        targets = all_attr_targets[attr]
        num_classes = len(CLASS_MAPPINGS[attr])
        
        rep = classification_report(targets, preds, output_dict=True, zero_division=0)
        
        try:
            if num_classes == 2:
                auc = roc_auc_score(targets, probs[:, 1])
            else:
                auc = roc_auc_score(targets, probs, multi_class='ovr')
        except ValueError:
            auc = float('nan')
            
        kappa = cohen_kappa_score(targets, preds)
        ece = compute_ece(probs, targets)
        cm = confusion_matrix(targets, preds, labels=list(range(num_classes))).tolist()
        
        metrics['per_head'][attr] = {
            'accuracy': rep['accuracy'],
            'macro_precision': rep['macro avg']['precision'],
            'macro_recall': rep['macro avg']['recall'],
            'macro_f1': rep['macro avg']['f1-score'],
            'weighted_precision': rep['weighted avg']['precision'],
            'weighted_recall': rep['weighted avg']['recall'],
            'weighted_f1': rep['weighted avg']['f1-score'],
            'roc_auc': auc,
            'cohen_kappa': kappa,
            'ece': ece,
            'confusion_matrix': cm,
            'per_class': {
                cls_name: {
                    'support': rep.get(str(cls_idx), {}).get('support', 0),
                    'sensitivity': rep.get(str(cls_idx), {}).get('recall', 0.0),
                    'specificity': sum([cm[i][i] for i in range(num_classes) if i != cls_idx]) / 
                                   max(1, sum([sum(cm[i]) for i in range(num_classes) if i != cls_idx]))
                }
                for cls_idx, cls_name in enumerate(CLASS_MAPPINGS[attr])
            }
        }
        
    exact_matches = 0
    total_samples = len(ds_test)
    hamming_errors = 0
    num_attrs = len(BASE_ATTRIBUTES)
    
    for i in range(total_samples):
        match = True
        for attr in BASE_ATTRIBUTES:
            if all_attr_preds[attr][i] != all_attr_targets[attr][i]:
                match = False
                hamming_errors += 1
        if match:
            exact_matches += 1
            
    mean_macro_f1 = np.mean([metrics['per_head'][attr]['macro_f1'] for attr in BASE_ATTRIBUTES])
    
    metrics['aggregate'] = {
        'exact_match_ratio': exact_matches / total_samples if total_samples > 0 else 0,
        'hamming_loss': hamming_errors / (total_samples * num_attrs) if total_samples > 0 else 0,
        'mean_macro_f1': mean_macro_f1
    }
    
    with open(os.path.join(run_dir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
        
    _generate_markdown_report(run_dir, metrics)
    return metrics


def _generate_markdown_report(run_dir: str, metrics: dict):
    lines = [
        "# SurgWound Assist — v4.0 End-to-End Metrics Report",
        "",
        "## Aggregate Metrics",
        f"- **Mean Macro-F1**: {metrics['aggregate']['mean_macro_f1']*100:.2f}%",
        f"- **Exact Match Ratio**: {metrics['aggregate']['exact_match_ratio']*100:.2f}%",
        f"- **Hamming Loss**: {metrics['aggregate']['hamming_loss']:.4f}",
        "",
        "## Per-Attribute Breakdown",
        "| Attribute | Macro-F1 | Accuracy | AUC | ECE | Kappa |",
        "|-----------|----------|----------|-----|-----|-------|"
    ]
    
    for attr, vals in metrics['per_head'].items():
        auc_str = f"{vals['roc_auc']:.4f}" if not np.isnan(vals['roc_auc']) else "N/A"
        lines.append(f"| {attr} | {vals['macro_f1']*100:.2f}% | {vals['accuracy']*100:.2f}% | {auc_str} | {vals['ece']:.4f} | {vals['cohen_kappa']:.4f} |")
        
    report_path = os.path.join(run_dir, "metrics_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\n[evaluate] Generated {report_path}")
