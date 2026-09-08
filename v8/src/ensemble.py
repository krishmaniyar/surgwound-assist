"""
v8/src/ensemble.py — Prediction Ensemble Engine across Seeds & Architectures.
Combines prediction probabilities with 7x TTA to minimize model variance.
"""
import os
import sys
import json
import torch
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from sklearn.metrics import f1_score, classification_report, accuracy_score, confusion_matrix, roc_auc_score, cohen_kappa_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS
from model import BiomedCLIPMultiTaskModel
from evaluate import evaluate_model, generate_evaluation_report, optimize_val_thresholds


def run_ensemble_evaluation(
    model_checkpoints: List[Dict[str, Any]],
    df_test: pd.DataFrame,
    device: torch.device,
    output_dir: str,
    tta_n: int = 7,
    weights: Optional[List[float]] = None,
    df_val: Optional[pd.DataFrame] = None,
    optimize_thresholds: bool = True,
) -> Dict[str, Any]:
    """
    Evaluates an ensemble of checkpoints.
    
    Each item in model_checkpoints should be:
      {
        'ckpt_path': str,
        'multiscale': bool,
        'use_text_prototypes': bool,
        'name': str,
        'legacy_mode': bool,
        'crop_scale': float,
      }
    """
def _eval_blend_weights(
    weights: np.ndarray,
    val_probs_list: List[Dict[str, np.ndarray]],
    val_targets: Dict[str, List[int]],
) -> float:
    """Evaluates mean Macro-F1 across all 8 attributes for a given weight vector."""
    num_models = len(val_probs_list)
    macro_f1s = []
    for attr in BASE_ATTRIBUTES:
        blended_probs = np.zeros_like(val_probs_list[0][attr])
        for idx in range(num_models):
            blended_probs += weights[idx] * val_probs_list[idx][attr]
        preds = np.argmax(blended_probs, axis=1)
        targets = val_targets[attr]
        score = f1_score(targets, preds, average='macro', zero_division=0)
        macro_f1s.append(score)
    return float(np.mean(macro_f1s))


def optimize_ensemble_blend_weights(
    val_probs_list: List[Dict[str, np.ndarray]],
    val_targets: Dict[str, List[int]],
    n_trials: int = 600,
    seed: int = 42,
) -> List[float]:
    """
    Finds optimal blend weights on the simplex (sum w_i = 1, w_i >= 0)
    to maximize validation Macro-F1 across all 8 attributes.
    """
    num_models = len(val_probs_list)
    if num_models <= 1:
        return [1.0]

    np.random.seed(seed)
    equal_w = np.array([1.0 / num_models] * num_models)
    best_score = _eval_blend_weights(equal_w, val_probs_list, val_targets)
    best_w = equal_w.tolist()

    # Dirichlet sampling search over probability simplex
    for _ in range(n_trials):
        w = np.random.dirichlet(np.ones(num_models))
        score = _eval_blend_weights(w, val_probs_list, val_targets)
        if score > best_score:
            best_score = score
            best_w = w.tolist()

    # Fine-tuning local search around best weights
    best_w_arr = np.array(best_w)
    for _ in range(250):
        noise = np.random.normal(0, 0.04, num_models)
        cand_w = np.maximum(best_w_arr + noise, 0.0)
        cand_sum = cand_w.sum()
        if cand_sum > 0:
            cand_w = cand_w / cand_sum
            score = _eval_blend_weights(cand_w, val_probs_list, val_targets)
            if score > best_score:
                best_score = score
                best_w_arr = cand_w
                best_w = cand_w.tolist()

    print(f"[ensemble] Optimized validation blend weights (Macro-F1: {best_score*100:.2f}%):")
    for i, weight_val in enumerate(best_w):
        print(f"  - Model {i+1} weight: {weight_val:.4f}")
    return best_w


def run_ensemble_evaluation(
    model_checkpoints: List[Dict[str, Any]],
    df_test: pd.DataFrame,
    device: torch.device,
    output_dir: str,
    tta_n: int = 7,
    weights: Optional[List[float]] = None,
    df_val: Optional[pd.DataFrame] = None,
    optimize_thresholds: bool = True,
) -> Dict[str, Any]:
    """
    Evaluates an ensemble of checkpoints.
    
    Each item in model_checkpoints should be:
      {
        'ckpt_path': str,
        'multiscale': bool,
        'use_text_prototypes': bool,
        'name': str,
        'legacy_mode': bool,
        'crop_scale': float,
      }
    """
    os.makedirs(output_dir, exist_ok=True)
    num_models = len(model_checkpoints)

    print(f"[ensemble] Evaluating ensemble of {num_models} models on {len(df_test)} test images...")

    val_probs_per_model = []
    test_probs_per_model = []
    all_targets = None
    val_targets = None

    for idx, spec in enumerate(model_checkpoints):
        ckpt_path = spec['ckpt_path']
        multiscale = spec.get('multiscale', False)
        use_text_proto = spec.get('use_text_prototypes', True)
        name = spec.get('name', f"model_{idx}")
        legacy_mode = spec.get('legacy_mode', True)
        crop_scale = spec.get('crop_scale', 0.65)

        print(f"  [{idx+1}/{num_models}] Loading {name} from {ckpt_path} (multiscale={multiscale})...")
        model = BiomedCLIPMultiTaskModel(
            use_text_prototypes=use_text_proto,
            multiscale=multiscale,
        ).to(device)
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
        model.eval()

        if df_val is not None:
            _, v_probs, v_targs = evaluate_model(
                model=model,
                df_eval=df_val,
                device=device,
                use_tta=False,
                legacy_mode=legacy_mode,
                multiscale=multiscale,
                local_crop_scale=crop_scale,
            )
            val_targets = v_targs
            val_probs_per_model.append(v_probs)

        _, probs, targets = evaluate_model(
            model=model,
            df_eval=df_test,
            device=device,
            use_tta=True,
            tta_n=tta_n,
            legacy_mode=legacy_mode,
            multiscale=multiscale,
            local_crop_scale=crop_scale,
        )

        all_targets = targets
        test_probs_per_model.append(probs)

    # Determine blend weights
    if weights is None:
        if df_val is not None and val_targets is not None:
            print("[ensemble] Optimizing ensemble blend weights on validation set...")
            weights = optimize_ensemble_blend_weights(val_probs_per_model, val_targets)
        else:
            weights = [1.0 / num_models] * num_models
    else:
        weights = [w / sum(weights) for w in weights]
        print(f"[ensemble] Using specified blend weights: {[round(w, 4) for w in weights]}")

    accumulated_probs = {attr: np.zeros((len(df_test), len(CLASS_MAPPINGS[attr]))) for attr in BASE_ATTRIBUTES}
    accumulated_val_probs = {attr: np.zeros((len(df_val), len(CLASS_MAPPINGS[attr]))) for attr in BASE_ATTRIBUTES} if df_val is not None else None

    for idx in range(num_models):
        w = weights[idx]
        for attr in BASE_ATTRIBUTES:
            accumulated_probs[attr] += w * test_probs_per_model[idx][attr]
            if df_val is not None:
                accumulated_val_probs[attr] += w * val_probs_per_model[idx][attr]

    # Check for validation threshold optimization
    opt_weights = None
    if df_val is not None and optimize_thresholds and val_targets is not None:
        print("[ensemble] Optimizing decision thresholds on validation ensemble probabilities...")
        opt_weights = optimize_val_thresholds(accumulated_val_probs, val_targets)
        for attr, w_vec in opt_weights.items():
            if not np.allclose(w_vec, 1.0):
                print(f"  - Optimized {attr} multipliers: {np.round(w_vec, 2)}")

    # Compute ensemble metrics
    metrics = {'aggregate': {}, 'per_head': {}, 'ensemble_models': [m['name'] for m in model_checkpoints], 'blend_weights': [round(w, 4) for w in weights]}
    exact_matches = 0
    num_samples = len(df_test)

    for attr in BASE_ATTRIBUTES:
        probs = accumulated_probs[attr]
        if opt_weights is not None and attr in opt_weights:
            probs_for_pred = probs * opt_weights[attr]
        else:
            probs_for_pred = probs
        preds = np.argmax(probs_for_pred, axis=1).tolist()
        targets = all_targets[attr]
        num_classes = len(CLASS_MAPPINGS[attr])

        rep = classification_report(targets, preds, output_dict=True, zero_division=0)
        cm = confusion_matrix(targets, preds, labels=list(range(num_classes))).tolist()

        # Robust ROC-AUC computation
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

    for i in range(num_samples):
        if all(np.argmax(accumulated_probs[a][i]) == all_targets[a][i] for a in BASE_ATTRIBUTES):
            exact_matches += 1

    minority_heads = ['exudate_type', 'infection_risk', 'closure_method', 'edema']
    valid_aucs = [metrics['per_head'][a]['roc_auc'] for a in BASE_ATTRIBUTES if not np.isnan(metrics['per_head'][a]['roc_auc'])]
    valid_kappas = [metrics['per_head'][a]['cohen_kappa'] for a in BASE_ATTRIBUTES if not np.isnan(metrics['per_head'][a]['cohen_kappa'])]
    metrics['aggregate'] = {
        'mean_macro_f1': float(np.mean([metrics['per_head'][a]['macro_f1'] for a in BASE_ATTRIBUTES])),
        'mean_accuracy': float(np.mean([metrics['per_head'][a]['accuracy'] for a in BASE_ATTRIBUTES])),
        'mean_macro_precision': float(np.mean([metrics['per_head'][a]['macro_precision'] for a in BASE_ATTRIBUTES])),
        'mean_macro_recall': float(np.mean([metrics['per_head'][a]['macro_recall'] for a in BASE_ATTRIBUTES])),
        'mean_weighted_f1': float(np.mean([metrics['per_head'][a]['weighted_f1'] for a in BASE_ATTRIBUTES])),
        'mean_roc_auc': float(np.mean(valid_aucs)) if valid_aucs else float('nan'),
        'mean_cohen_kappa': float(np.mean(valid_kappas)) if valid_kappas else float('nan'),
        'minority_mean_macro_f1': float(np.mean([metrics['per_head'][a]['macro_f1'] for a in minority_heads])),
        'exact_match_ratio': float(exact_matches / max(1, num_samples)),
    }

    report_path = generate_evaluation_report(output_dir, metrics, title="SurgWound Assist v8 Deep Ensemble")
    with open(os.path.join(output_dir, "ensemble_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
    print(f"[ensemble] Generated ensemble report -> {report_path}")
    print(f"  Ensemble Test Mean Macro-F1: {metrics['aggregate']['mean_macro_f1']*100:.2f}%")

    # Check against SOTA and sync docs/ if best
    import shutil
    registry_file = 'v8/experiments/experiment_registry.csv'
    prev_best_f1 = 0.5110
    if os.path.exists(registry_file):
        try:
            reg_df = pd.read_csv(registry_file)
            if 'test_f1' in reg_df.columns and len(reg_df) > 0:
                prev_best_f1 = float(reg_df['test_f1'].dropna().max())
        except Exception:
            pass

    if metrics['aggregate']['mean_macro_f1'] >= prev_best_f1:
        os.makedirs("docs", exist_ok=True)
        shutil.copy2(report_path, os.path.join("docs", "best_evaluation_report.md"))
        shutil.copy2(report_path, os.path.join("docs", "evaluation_report.md"))
        print(f"[BEST ENSEMBLE] SOTA! Copied ensemble evaluation report to docs/")

    return metrics


def auto_discover_checkpoints(runs_dir: str = "v8/runs", top_k: int = 4) -> List[Dict[str, Any]]:
    """Discovers top completed experiment checkpoints in runs_dir."""
    candidates = []
    if not os.path.exists(runs_dir):
        return []

    for d in sorted(os.listdir(runs_dir)):
        run_path = os.path.join(runs_dir, d)
        ckpt_path = os.path.join(run_path, "checkpoints", "best_model.pth")
        cfg_path = os.path.join(run_path, "run_config.json")
        if os.path.isdir(run_path) and os.path.exists(ckpt_path):
            multiscale = False
            use_text_proto = True
            legacy_mode = True
            crop_scale = 0.65
            if os.path.exists(cfg_path):
                try:
                    with open(cfg_path, 'r') as f:
                        cfg = json.load(f).get('config', {})
                        multiscale = cfg.get('multiscale', False)
                        use_text_proto = cfg.get('use_text_prototypes', True)
                        legacy_mode = cfg.get('legacy_mode', True)
                        crop_scale = cfg.get('crop_scale', 0.65)
                except Exception:
                    pass
            candidates.append({
                'name': d,
                'ckpt_path': ckpt_path,
                'multiscale': multiscale,
                'use_text_prototypes': use_text_proto,
                'legacy_mode': legacy_mode,
                'crop_scale': crop_scale,
            })
    return candidates[-top_k:]


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate multi-model ensemble for SurgWound Assist v8")
    parser.add_argument('--dataset_csv', type=str, default='data/annotations.csv')
    parser.add_argument('--output_dir', type=str, default='v8/runs/ensemble_latest')
    parser.add_argument('--tta_n', type=int, default=7)
    parser.add_argument('--checkpoints', type=str, nargs='+', default=None, help="Explicit checkpoint paths or run directories")
    parser.add_argument('--auto_top_k', type=int, default=4, help="Auto-discover top K latest runs")
    parser.add_argument('--weights', type=float, nargs='+', default=None, help="Blend weights for the models")
    args = parser.parse_args()

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    df = pd.read_csv(args.dataset_csv)
    df_val = df[df['split'] == 'val'].reset_index(drop=True)
    df_test = df[df['split'] == 'test'].reset_index(drop=True)

    if args.checkpoints:
        specs = []
        for p in args.checkpoints:
            ckpt_path = p if p.endswith('.pth') else os.path.join(p, 'checkpoints', 'best_model.pth')
            run_dir = os.path.dirname(os.path.dirname(ckpt_path)) if p.endswith('.pth') else p
            cfg_path = os.path.join(run_dir, 'run_config.json')
            multiscale = False
            use_text_proto = True
            legacy_mode = True
            crop_scale = 0.65
            if os.path.exists(cfg_path):
                try:
                    with open(cfg_path, 'r') as f:
                        c = json.load(f).get('config', {})
                        multiscale = c.get('multiscale', False)
                        use_text_proto = c.get('use_text_prototypes', True)
                        legacy_mode = c.get('legacy_mode', True)
                        crop_scale = c.get('crop_scale', 0.65)
                except Exception:
                    pass
            specs.append({
                'name': os.path.basename(run_dir),
                'ckpt_path': ckpt_path,
                'multiscale': multiscale,
                'use_text_prototypes': use_text_proto,
                'legacy_mode': legacy_mode,
                'crop_scale': crop_scale,
            })
    else:
        specs = auto_discover_checkpoints(top_k=args.auto_top_k)

    print(f"[ensemble] Assembled {len(specs)} models:")
    for s in specs:
        print(f"  - {s['name']}: {s['ckpt_path']} (multiscale={s['multiscale']})")

    run_ensemble_evaluation(
        model_checkpoints=specs,
        df_test=df_test,
        device=device,
        output_dir=args.output_dir,
        tta_n=args.tta_n,
        weights=args.weights,
        df_val=df_val,
        optimize_thresholds=True,
    )
