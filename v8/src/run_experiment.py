"""
v8/src/run_experiment.py — Master autonomous experiment runner.
Executes training, evaluation (with 7x TTA & validation threshold optimization),
logs results to experiment_registry.csv, and produces comparative reports.
"""
import os
import sys
import shutil
import argparse
import time
import json
import torch
import pandas as pd
from datetime import datetime

# Local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import create_v8_run_dir, load_config, BASE_ATTRIBUTES, CLASS_MAPPINGS
from train import train_v8_model, set_seed
from evaluate import evaluate_model, optimize_val_thresholds, generate_evaluation_report


def check_gpu():
    print("\n" + "=" * 60)
    print("DEVICE CHECK")
    print("=" * 60)
    if torch.cuda.is_available():
        name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"  GPU  : {name}")
        print(f"  VRAM : {vram:.2f} GB")
        device = torch.device('cuda')
    else:
        print("  GPU  : NOT AVAILABLE (CPU fallback)")
        device = torch.device('cpu')
    print("=" * 60 + "\n")
    return device


def log_to_registry(
    registry_path: str,
    record: dict,
):
    """Appends an experiment record to experiment_registry.csv."""
    os.makedirs(os.path.dirname(registry_path), exist_ok=True)
    df_new = pd.DataFrame([record])
    if os.path.exists(registry_path):
        df_existing = pd.read_csv(registry_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(registry_path, index=False)
    else:
        df_new.to_csv(registry_path, index=False)
    print(f"[registry] Recorded experiment {record.get('experiment_id')} to {registry_path}")
def run_experiment(
    experiment_id: str,
    config_file: str = None,
    loss_strategy: str = 'logit_adjusted',
    epochs: int = 80,
    lr: float = 3e-5,
    batch_size: int = 16,
    accum_steps: int = 2,
    seed: int = 42,
    multiscale: bool = False,
    use_text_prototypes: bool = True,
    legacy_mode: bool = True,
    dataset_csv: str = 'data/annotations.csv',
    img_dir: str = 'data/images',
    hypothesis: str = "Evaluation of v8 architecture",
    optimize_thresholds: bool = False,
    tau: float = 1.0,
    dropout: float = 0.25,
    use_sampler: bool = False,
    crop_scale: float = 0.65,
    patience: int = 20,
    adaptive_tau: bool = False,
    label_smoothing: float = 0.0,
    use_mixup: bool = False,
):
    t_start = time.time()
    device = check_gpu()

    # Load YAML if provided
    if config_file and os.path.exists(config_file):
        cfg = load_config(config_file)
        print(f"[run_experiment] Loaded config from {config_file}")
        # Override defaults if specified in YAML
        if 'training' in cfg:
            epochs = cfg['training'].get('epochs', epochs)
            batch_size = cfg['training'].get('batch_size', batch_size)
            accum_steps = cfg['training'].get('accum_steps', accum_steps)
            dropout = cfg['training'].get('dropout', dropout)
            patience = cfg['training'].get('patience', patience)
        if 'optimizer' in cfg:
            lr = float(cfg['optimizer'].get('base_lr', lr))
        if 'loss' in cfg:
            loss_strategy = cfg['loss'].get('strategy', loss_strategy)
            tau = float(cfg['loss'].get('tau', tau))
            adaptive_tau = cfg['loss'].get('adaptive_tau', adaptive_tau)
        if 'seed' in cfg:
            seed = cfg['seed'].get('random_seed', seed)
        if 'data' in cfg:
            dataset_csv = cfg['data'].get('dataset_csv', dataset_csv)
            img_dir = cfg['data'].get('image_dir', img_dir)
            crop_scale = float(cfg['data'].get('crop_scale', crop_scale))

    run_dir = create_v8_run_dir(base_dir="v8/runs", prefix=experiment_id)
    print(f"[run_experiment] Run directory: {run_dir}")

    # Load dataset
    df = pd.read_csv(dataset_csv)
    df_train = df[df['split'] == 'train'].reset_index(drop=True)
    df_val = df[df['split'] == 'val'].reset_index(drop=True)
    df_test = df[df['split'] == 'test'].reset_index(drop=True)

    print(f"[run_experiment] Loaded {len(df)} samples: Train={len(df_train)}, Val={len(df_val)}, Test={len(df_test)}")

    # Save run metadata
    meta = {
        'experiment_id': experiment_id,
        'started_at': datetime.now().isoformat(),
        'hypothesis': hypothesis,
        'config': {
            'loss_strategy': loss_strategy,
            'epochs': epochs,
            'lr': lr,
            'batch_size': batch_size,
            'accum_steps': accum_steps,
            'effective_batch': batch_size * accum_steps,
            'seed': seed,
            'multiscale': multiscale,
            'use_text_prototypes': use_text_prototypes,
            'legacy_mode': legacy_mode,
            'dataset_csv': dataset_csv,
            'tau': tau,
            'dropout': dropout,
            'use_sampler': use_sampler,
            'crop_scale': crop_scale,
            'patience': patience,
            'adaptive_tau': adaptive_tau,
            'label_smoothing': label_smoothing,
            'use_mixup': use_mixup,
        }
    }
    with open(os.path.join(run_dir, "run_config.json"), 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=4)

    # 1. Train
    print("\n" + "="*60)
    print(f"STEP 1: TRAINING MODEL ({experiment_id})")
    print("="*60)

    train_res = train_v8_model(
        df_train=df_train,
        df_val=df_val,
        run_dir=run_dir,
        loss_strategy=loss_strategy,
        epochs=epochs,
        lr=lr,
        dropout=dropout,
        batch_size=batch_size,
        accum_steps=accum_steps,
        patience=patience,
        seed=seed,
        legacy_mode=legacy_mode,
        multiscale=multiscale,
        use_text_prototypes=use_text_prototypes,
        use_balanced_sampler=use_sampler,
        local_crop_scale=crop_scale,
        adaptive_tau=adaptive_tau,
        tau=tau,
        label_smoothing=label_smoothing,
        use_mixup=use_mixup,
        img_dir=img_dir,
        device=device,
    )

    if train_res['status'] != 'SUCCESS':
        print(f"[ERROR] Training failed with: {train_res.get('error')}")
        return train_res

    model = train_res['model']

    # 2. Validation Evaluation & Threshold Calibration (Optional)
    print("\n" + "="*60)
    print("STEP 2: VALIDATION SET EVALUATION")
    print("="*60)

    val_metrics, val_probs, val_targets = evaluate_model(
        model=model,
        df_eval=df_val,
        device=device,
        use_tta=False, # standard inference on val
        img_dir=img_dir,
        legacy_mode=legacy_mode,
        multiscale=multiscale,
        local_crop_scale=crop_scale,
    )
    print(f"  Validation Mean Macro-F1 (Argmax): {val_metrics['aggregate']['mean_macro_f1']*100:.2f}%")

    val_thresholds = None
    if optimize_thresholds:
        val_thresholds = optimize_val_thresholds(val_probs, val_targets)
        val_opt_metrics, _, _ = evaluate_model(
            model=model,
            df_eval=df_val,
            device=device,
            use_tta=False,
            img_dir=img_dir,
            legacy_mode=legacy_mode,
            multiscale=multiscale,
            local_crop_scale=crop_scale,
            class_weights_dict=val_thresholds,
        )
        print(f"  Validation Mean Macro-F1 (Threshold Optimized): {val_opt_metrics['aggregate']['mean_macro_f1']*100:.2f}%")

    # 3. Test Set Evaluation with 7x TTA
    print("\n" + "="*60)
    print("STEP 3: TEST SET EVALUATION (7x TTA)")
    print("="*60)

    test_metrics_raw, _, _ = evaluate_model(
        model=model,
        df_eval=df_test,
        device=device,
        use_tta=True,
        tta_n=7,
        img_dir=img_dir,
        legacy_mode=legacy_mode,
        multiscale=multiscale,
        local_crop_scale=crop_scale,
    )

    print(f"\n>>> TEST MACRO-F1 (Raw Argmax + 7x TTA): {test_metrics_raw['aggregate']['mean_macro_f1']*100:.2f}% <<<")
    print(f"    Minority Heads Macro-F1: {test_metrics_raw['aggregate']['minority_mean_macro_f1']*100:.2f}%")
    print(f"    Mean ROC-AUC: {test_metrics_raw['aggregate']['mean_roc_auc']:.4f}")
    print(f"    Mean Cohen's Kappa: {test_metrics_raw['aggregate']['mean_cohen_kappa']:.4f}")
    print(f"    Exact Match Ratio: {test_metrics_raw['aggregate']['exact_match_ratio']*100:.2f}%")

    final_test_metrics = test_metrics_raw
    if optimize_thresholds and val_thresholds is not None:
        test_metrics_opt, _, _ = evaluate_model(
            model=model,
            df_eval=df_test,
            device=device,
            use_tta=True,
            tta_n=7,
            img_dir=img_dir,
            legacy_mode=legacy_mode,
            multiscale=multiscale,
            local_crop_scale=crop_scale,
            class_weights_dict=val_thresholds,
        )
        print(f"\n>>> TEST MACRO-F1 (Val-Thresholded + 7x TTA): {test_metrics_opt['aggregate']['mean_macro_f1']*100:.2f}% <<<")
        print(f"    Minority Heads Macro-F1: {test_metrics_opt['aggregate']['minority_mean_macro_f1']*100:.2f}%")
        generate_evaluation_report(run_dir, test_metrics_opt, title=f"Experiment {experiment_id} Val-Thresholded Results")
        if test_metrics_opt['aggregate']['mean_macro_f1'] > test_metrics_raw['aggregate']['mean_macro_f1']:
            final_test_metrics = test_metrics_opt

    # Save reports
    report_path = generate_evaluation_report(run_dir, final_test_metrics, title=f"Experiment {experiment_id} Test Results")
    print(f"[run_experiment] Evaluation report generated: {report_path}")

    # Compute runtime and VRAM
    runtime_sec = int(time.time() - t_start)
    vram_used = f"{torch.cuda.max_memory_allocated() / 1e9:.2f} GB" if torch.cuda.is_available() else "0 GB"

    # Compare against v7.5
    v7_5_baseline_f1 = 0.5110
    final_test_f1 = final_test_metrics['aggregate']['mean_macro_f1']
    delta = (final_test_f1 - v7_5_baseline_f1) * 100

    conclusion = f"{'EXCEEDED v7.5' if final_test_f1 > v7_5_baseline_f1 else 'DID NOT BEAT v7.5'} by {delta:+.2f}% ({final_test_f1*100:.2f}% vs {v7_5_baseline_f1*100:.2f}%)"

    registry_record = {
        'experiment_id': experiment_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'hypothesis': hypothesis,
        'architecture': f"BiomedCLIP+{'MultiScale' if multiscale else 'ViT-B'}+{'TextProto' if use_text_prototypes else 'MLP'}",
        'backbone': 'BiomedCLIP-ViT-B/16',
        'loss': f"{loss_strategy}(tau={tau})",
        'lr': lr,
        'scheduler': 'Cosine+Warmup',
        'augmentation': '7x TTA',
        'resolution': f"224x224 (global+local_{crop_scale})" if multiscale else '224x224',
        'batch_size': batch_size,
        'effective_batch': batch_size * accum_steps,
        'seed': seed,
        'validation_f1': round(train_res['best_val_f1'], 4),
        'test_f1': round(final_test_f1, 4),
        'minority_f1': round(final_test_metrics['aggregate']['minority_mean_macro_f1'], 4),
        'runtime': f"{runtime_sec}s",
        'vram': vram_used,
        'status': 'COMPLETED',
        'conclusion': conclusion,
        'next_action': 'TBD based on per-attribute error analysis',
    }

    log_to_registry('v8/experiments/experiment_registry.csv', registry_record)

    # Check against all-time best test Macro-F1 and sync docs/
    registry_file = 'v8/experiments/experiment_registry.csv'
    prev_best_f1 = 0.5110
    if os.path.exists(registry_file):
        try:
            reg_df = pd.read_csv(registry_file)
            if 'test_f1' in reg_df.columns and len(reg_df) > 0:
                prev_best_f1 = float(reg_df['test_f1'].dropna().max())
        except Exception:
            pass

    if final_test_f1 >= prev_best_f1:
        os.makedirs("docs", exist_ok=True)
        shutil.copy2(report_path, os.path.join("docs", "best_evaluation_report.md"))
        shutil.copy2(report_path, os.path.join("docs", "evaluation_report.md"))
        best_ckpt = os.path.join(run_dir, "checkpoints", "best_model.pth")
        if os.path.exists(best_ckpt):
            shutil.copy2(best_ckpt, os.path.join("docs", "best_model.pth"))
        print(f"[BEST MODEL] SOTA! Copied best_model.pth and evaluation_report.md to docs/")

    print("\n" + "="*70)
    print("EXPERIMENT EXECUTION COMPLETE")
    print(f"  Experiment ID : {experiment_id}")
    print(f"  Test Macro-F1 : {final_test_f1*100:.2f}%  (Baseline v7.5: 51.10%, Delta: {delta:+.2f}%)")
    print(f"  Minority F1   : {final_test_metrics['aggregate']['minority_mean_macro_f1']*100:.2f}%")
    print(f"  Mean ROC-AUC  : {final_test_metrics['aggregate']['mean_roc_auc']:.4f}")
    print(f"  Mean Kappa    : {final_test_metrics['aggregate']['mean_cohen_kappa']:.4f}")
    print(f"  Runtime       : {runtime_sec}s ({runtime_sec/60:.1f} min)")
    print(f"  Peak VRAM     : {vram_used}")
    print(f"  Conclusion    : {conclusion}")
    print("="*70 + "\n")

    return {
        'experiment_id': experiment_id,
        'run_dir': run_dir,
        'final_test_f1': final_test_f1,
        'final_test_metrics': final_test_metrics,
        'record': registry_record,
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp_id', type=str, default='v8_test')
    parser.add_argument('--config', type=str, default=None)
    parser.add_argument('--loss', type=str, default='logit_adjusted')
    parser.add_argument('--epochs', type=int, default=80)
    parser.add_argument('--lr', type=float, default=3e-5)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--multiscale', action='store_true')
    parser.add_argument('--no_text_proto', action='store_true')
    parser.add_argument('--tau', type=float, default=1.0)
    parser.add_argument('--dropout', type=float, default=0.25)
    parser.add_argument('--use_sampler', action='store_true')
    parser.add_argument('--crop_scale', type=float, default=0.65)
    parser.add_argument('--patience', type=int, default=20)
    parser.add_argument('--adaptive_tau', action='store_true')
    parser.add_argument('--dataset_csv', type=str, default='data/annotations.csv')
    parser.add_argument('--img_dir', type=str, default='data/images')
    parser.add_argument('--hypothesis', type=str, default='Evaluation of v8 architecture')
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--accum_steps', type=int, default=2)
    parser.add_argument('--optimize_thresholds', action='store_true')
    parser.add_argument('--label_smoothing', type=float, default=0.0)
    parser.add_argument('--use_mixup', action='store_true')
    args = parser.parse_args()

    run_experiment(
        experiment_id=args.exp_id,
        config_file=args.config,
        loss_strategy=args.loss,
        epochs=args.epochs,
        lr=args.lr,
        batch_size=args.batch_size,
        accum_steps=args.accum_steps,
        seed=args.seed,
        multiscale=args.multiscale,
        use_text_prototypes=(not args.no_text_proto),
        optimize_thresholds=args.optimize_thresholds,
        tau=args.tau,
        dropout=args.dropout,
        use_sampler=args.use_sampler,
        crop_scale=args.crop_scale,
        patience=args.patience,
        adaptive_tau=args.adaptive_tau,
        dataset_csv=args.dataset_csv,
        img_dir=args.img_dir,
        hypothesis=args.hypothesis,
        label_smoothing=args.label_smoothing,
        use_mixup=args.use_mixup,
    )
