"""
v8/src/kfold_cv.py — Stratified 5-Fold Cross-Validation & Out-of-Fold (OOF) Engine.

Enables unbiased, leakage-free full-dataset evaluation across all 686 surgical wound images.
For each fold k in 1..K:
  - Trains on 4 folds (80%, ~549 images)
  - Evaluates on the held-out fold (20%, ~137 images) using 7x TTA
  - Stores out-of-fold (OOF) predicted probabilities
After all folds complete:
  - Computes exact OOF Macro-F1, Cohen's Kappa, ROC-AUC, and Exact Match across all 686 samples
  - Exports a unified 5-fold deployment ensemble checkpoint
"""
import os
import sys
import json
import time
import argparse
import shutil
from datetime import datetime
from typing import Dict, List, Any, Tuple

import torch
import numpy as np
import pandas as pd
from sklearn.metrics import (
    f1_score, classification_report, accuracy_score,
    confusion_matrix, roc_auc_score, cohen_kappa_score
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS
from model import BiomedCLIPMultiTaskModel
from train import train_v8_model, set_seed
from evaluate import evaluate_model, optimize_val_thresholds, generate_evaluation_report


def greedy_multilabel_stratified_kfold(df: pd.DataFrame, n_splits: int = 5, seed: int = 42) -> np.ndarray:
    """
    Greedy multi-attribute stratification across all 8 wound attributes.
    Distributes rare minority classes evenly across all K folds.
    """
    np.random.seed(seed)
    n = len(df)
    fold_assignments = np.full(n, -1, dtype=int)

    # Compute label rarity score for each sample
    class_counts = {}
    for attr in BASE_ATTRIBUTES:
        class_counts[attr] = df[attr].value_counts().to_dict()

    sample_rarities = []
    for idx, row in df.iterrows():
        min_freq = float('inf')
        for attr in BASE_ATTRIBUTES:
            val = row[attr]
            freq = class_counts[attr].get(val, 0)
            if freq < min_freq:
                min_freq = freq
        sample_rarities.append((idx, min_freq))

    # Sort samples from rarest to most common
    sample_rarities.sort(key=lambda x: (x[1], np.random.rand()))

    # Track fold distributions per attribute class
    fold_class_counts = [
        {attr: {c: 0 for c in CLASS_MAPPINGS[attr]} for attr in BASE_ATTRIBUTES}
        for _ in range(n_splits)
    ]
    fold_sizes = [0] * n_splits

    for s_idx, _ in sample_rarities:
        row = df.loc[s_idx]
        best_fold = None
        min_penalty = float('inf')

        for f in range(n_splits):
            penalty = fold_sizes[f] * 0.1
            for attr in BASE_ATTRIBUTES:
                val = row[attr]
                if val in fold_class_counts[f][attr]:
                    penalty += fold_class_counts[f][attr][val]
            if penalty < min_penalty:
                min_penalty = penalty
                best_fold = f

        fold_assignments[s_idx] = best_fold
        fold_sizes[best_fold] += 1
        for attr in BASE_ATTRIBUTES:
            val = row[attr]
            if val in fold_class_counts[best_fold][attr]:
                fold_class_counts[best_fold][attr][val] += 1

    return fold_assignments


def run_kfold_cross_validation(
    dataset_csv: str = 'data/annotations.csv',
    img_dir: str = 'data/images',
    output_dir: str = 'v8/runs/kfold_cv_5fold',
    n_splits: int = 5,
    epochs: int = 60,
    lr: float = 5e-5,
    batch_size: int = 16,
    accum_steps: int = 4,
    seed: int = 42,
    patience: int = 20,
    loss_strategy: str = 'logit_adjusted',
    adaptive_tau: bool = True,
    label_smoothing: float = 0.1,
    use_mixup: bool = True,
    multiscale: bool = True,
    crop_scale: float = 0.50,
    dropout: float = 0.30,
    tta_n: int = 7,
) -> Dict[str, Any]:
    """
    Executes full K-Fold Cross-Validation with OOF Evaluation.
    """
    os.makedirs(output_dir, exist_ok=True)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    df = pd.read_csv(dataset_csv).reset_index(drop=True)
    n_total = len(df)

    print("\n" + "=" * 70)
    print(f"SURGWOUND ASSIST v8 — {n_splits}-FOLD CROSS-VALIDATION ENGINE")
    print(f"  Dataset Total Samples : {n_total}")
    print(f"  Target Hardware       : {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
    print(f"  Strategy              : {loss_strategy.upper()} + MultiScale + MixUp + Smoothing + OOF Eval")
    print("=" * 70 + "\n")

    # Generate stratified fold assignments
    df['fold'] = greedy_multilabel_stratified_kfold(df, n_splits=n_splits, seed=seed)
    df.to_csv(os.path.join(output_dir, "stratified_folds.csv"), index=False)

    oof_probs = {attr: np.zeros((n_total, len(CLASS_MAPPINGS[attr]))) for attr in BASE_ATTRIBUTES}
    fold_metrics = []
    checkpoint_paths = []

    t_start = time.time()

    for fold in range(n_splits):
        print("\n" + "#" * 60)
        print(f"STARTING FOLD {fold + 1} / {n_splits}")
        print("#" * 60)

        df_train_fold = df[df['fold'] != fold].reset_index(drop=True)
        df_val_fold = df[df['fold'] == fold].reset_index(drop=True)
        fold_val_indices = df[df['fold'] == fold].index.values

        print(f"  Train samples: {len(df_train_fold)} | Val (OOF) samples: {len(df_val_fold)}")

        fold_dir = os.path.join(output_dir, f"fold_{fold}")
        os.makedirs(fold_dir, exist_ok=True)

        # Train model on 4 folds
        train_res = train_v8_model(
            df_train=df_train_fold,
            df_val=df_val_fold,
            run_dir=fold_dir,
            loss_strategy=loss_strategy,
            epochs=epochs,
            lr=lr,
            dropout=dropout,
            batch_size=batch_size,
            accum_steps=accum_steps,
            patience=patience,
            seed=seed + fold * 10,
            legacy_mode=False,
            multiscale=multiscale,
            use_text_prototypes=True,
            use_balanced_sampler=True,
            local_crop_scale=crop_scale,
            adaptive_tau=adaptive_tau,
            label_smoothing=label_smoothing,
            use_mixup=use_mixup,
            img_dir=img_dir,
            device=device,
        )

        fold_model = train_res['model']
        best_ckpt = os.path.join(fold_dir, "checkpoints", "best_model.pth")
        checkpoint_paths.append(best_ckpt)

        # Evaluate on the held-out fold with 7x TTA
        print(f"\n[Fold {fold + 1}] Evaluating Out-of-Fold with 7x TTA...")
        f_metrics, f_probs, _ = evaluate_model(
            model=fold_model,
            df_eval=df_val_fold,
            device=device,
            use_tta=True,
            tta_n=tta_n,
            img_dir=img_dir,
            legacy_mode=False,
            multiscale=multiscale,
            local_crop_scale=crop_scale,
        )

        # Record OOF probabilities
        for attr in BASE_ATTRIBUTES:
            oof_probs[attr][fold_val_indices] = f_probs[attr]

        f_macro_f1 = f_metrics['aggregate']['mean_macro_f1']
        fold_metrics.append(f_macro_f1)
        print(f"[Fold {fold + 1}] OOF Mean Macro-F1: {f_macro_f1 * 100:.2f}%")

    # Full Dataset OOF Evaluation across all 686 samples
    print("\n" + "=" * 70)
    print("COMPUTING GLOBAL OUT-OF-FOLD (OOF) METRICS (N = 686)")
    print("=" * 70)

    global_oof_metrics = {'aggregate': {}, 'per_head': {}, 'fold_f1_scores': fold_metrics}
    exact_matches = 0

    for attr in BASE_ATTRIBUTES:
        probs = oof_probs[attr]
        preds = np.argmax(probs, axis=1).tolist()
        targets = [CLASS_MAPPINGS[attr].index(str(v).strip()) if str(v).strip() in CLASS_MAPPINGS[attr] else 0 for v in df[attr]]
        num_classes = len(CLASS_MAPPINGS[attr])

        rep = classification_report(targets, preds, output_dict=True, zero_division=0)
        cm = confusion_matrix(targets, preds, labels=list(range(num_classes))).tolist()

        targets_np = np.array(targets)
        auc_scores = []
        for c in range(num_classes):
            binary_target = (targets_np == c).astype(int)
            if len(np.unique(binary_target)) > 1:
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

        global_oof_metrics['per_head'][attr] = {
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

    for i in range(n_total):
        is_match = True
        for a in BASE_ATTRIBUTES:
            t = CLASS_MAPPINGS[a].index(str(df.loc[i, a]).strip()) if str(df.loc[i, a]).strip() in CLASS_MAPPINGS[a] else 0
            if np.argmax(oof_probs[a][i]) != t:
                is_match = False
                break
        if is_match:
            exact_matches += 1

    minority_heads = ['exudate_type', 'infection_risk', 'closure_method', 'edema']
    valid_aucs = [global_oof_metrics['per_head'][a]['roc_auc'] for a in BASE_ATTRIBUTES if not np.isnan(global_oof_metrics['per_head'][a]['roc_auc'])]
    valid_kappas = [global_oof_metrics['per_head'][a]['cohen_kappa'] for a in BASE_ATTRIBUTES if not np.isnan(global_oof_metrics['per_head'][a]['cohen_kappa'])]

    global_oof_metrics['aggregate'] = {
        'mean_macro_f1': float(np.mean([global_oof_metrics['per_head'][a]['macro_f1'] for a in BASE_ATTRIBUTES])),
        'mean_accuracy': float(np.mean([global_oof_metrics['per_head'][a]['accuracy'] for a in BASE_ATTRIBUTES])),
        'mean_macro_precision': float(np.mean([global_oof_metrics['per_head'][a]['macro_precision'] for a in BASE_ATTRIBUTES])),
        'mean_macro_recall': float(np.mean([global_oof_metrics['per_head'][a]['macro_recall'] for a in BASE_ATTRIBUTES])),
        'mean_weighted_f1': float(np.mean([global_oof_metrics['per_head'][a]['weighted_f1'] for a in BASE_ATTRIBUTES])),
        'mean_roc_auc': float(np.mean(valid_aucs)) if valid_aucs else float('nan'),
        'mean_cohen_kappa': float(np.mean(valid_kappas)) if valid_kappas else float('nan'),
        'minority_mean_macro_f1': float(np.mean([global_oof_metrics['per_head'][a]['macro_f1'] for a in minority_heads])),
        'exact_match_ratio': float(exact_matches / n_total),
        'fold_mean_macro_f1': float(np.mean(fold_metrics)),
        'fold_std_macro_f1': float(np.std(fold_metrics)),
    }

    # Save OOF Evaluation Report
    report_path = generate_evaluation_report(output_dir, global_oof_metrics, title="SurgWound Assist v8 Full 5-Fold OOF Evaluation (N=686)")
    with open(os.path.join(output_dir, "oof_metrics.json"), 'w') as f:
        json.dump(global_oof_metrics, f, indent=4)

    # Save 5-Fold Ensemble Manifest
    manifest = {
        'model_type': '5_fold_cross_validation_ensemble',
        'n_splits': n_splits,
        'checkpoints': checkpoint_paths,
        'multiscale': multiscale,
        'crop_scale': crop_scale,
        'oof_macro_f1': global_oof_metrics['aggregate']['mean_macro_f1'],
        'created_at': datetime.now().isoformat(),
    }
    with open(os.path.join(output_dir, "ensemble_manifest.json"), 'w') as f:
        json.dump(manifest, f, indent=4)

    runtime_min = (time.time() - t_start) / 60
    print("\n" + "=" * 70)
    print("5-FOLD CROSS-VALIDATION COMPLETE")
    print(f"  Overall OOF Macro-F1   : {global_oof_metrics['aggregate']['mean_macro_f1']*100:.2f}%")
    print(f"  Fold Mean ± Std        : {global_oof_metrics['aggregate']['fold_mean_macro_f1']*100:.2f}% ± {global_oof_metrics['aggregate']['fold_std_macro_f1']*100:.2f}%")
    print(f"  Minority Heads F1      : {global_oof_metrics['aggregate']['minority_mean_macro_f1']*100:.2f}%")
    print(f"  Mean ROC-AUC           : {global_oof_metrics['aggregate']['mean_roc_auc']:.4f}")
    print(f"  Mean Cohen's Kappa     : {global_oof_metrics['aggregate']['mean_cohen_kappa']:.4f}")
    print(f"  Exact Match Ratio      : {global_oof_metrics['aggregate']['exact_match_ratio']*100:.2f}%")
    print(f"  Total Runtime          : {runtime_min:.1f} minutes")
    print(f"  OOF Report Saved       : {report_path}")
    print("=" * 70 + "\n")

    return global_oof_metrics


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run 5-Fold Cross-Validation on SurgWound Dataset")
    parser.add_argument('--dataset_csv', type=str, default='data/annotations.csv')
    parser.add_argument('--img_dir', type=str, default='data/images')
    parser.add_argument('--output_dir', type=str, default='v8/runs/kfold_cv_5fold')
    parser.add_argument('--n_splits', type=int, default=5)
    parser.add_argument('--epochs', type=int, default=60)
    parser.add_argument('--lr', type=float, default=5e-5)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--accum_steps', type=int, default=4)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--patience', type=int, default=20)
    parser.add_argument('--label_smoothing', type=float, default=0.1)
    parser.add_argument('--use_mixup', action='store_true', default=True)
    parser.add_argument('--multiscale', action='store_true', default=True)
    parser.add_argument('--crop_scale', type=float, default=0.50)
    args = parser.parse_args()

    run_kfold_cross_validation(
        dataset_csv=args.dataset_csv,
        img_dir=args.img_dir,
        output_dir=args.output_dir,
        n_splits=args.n_splits,
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
        accum_steps=args.accum_steps,
        seed=args.seed,
        patience=args.patience,
        label_smoothing=args.label_smoothing,
        use_mixup=args.use_mixup,
        multiscale=args.multiscale,
        crop_scale=args.crop_scale,
    )
