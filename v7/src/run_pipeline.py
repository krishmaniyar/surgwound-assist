"""
run_pipeline.py — v7.4 BiomedCLIP Pipeline Orchestrator.

v7.4 is the DEFINITIVE NaN fix:
  Root cause: GradScaler multiplies gradients by ~65536 for FP16 stability.
  LDAM also has s=15 scale factor. Combined: 65536 * 15 * gradient overflows FP16.
  No amount of casting inside LDAMLoss.forward() fixes this — the NaN is in backprop.

  Fix: Disable AMP entirely for LDAM phase. Run FP32 forward+backward.
  AMP weights are always FP32 — only activations are FP16. Switching to FP32
  forward in LDAM phase is architecturally safe and eliminates overflow completely.
"""
import os
import sys
import torch
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import create_run_dir, save_run_config

VERSION = "v7.6"


def check_gpu():
    print("\n" + "=" * 60)
    print("DEVICE CHECK")
    print("=" * 60)
    if torch.cuda.is_available():
        name = torch.cuda.get_device_name(0)
        vram = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"  GPU  : {name}")
        print(f"  VRAM : {vram:.1f} GB")
        device = torch.device('cuda')
    else:
        print("  GPU  : NOT AVAILABLE")
        device = torch.device('cpu')
    print("=" * 60 + "\n")
    return device


def main():
    start_ts = datetime.now()
    device   = check_gpu()
    run_dir  = create_run_dir()

    save_run_config(run_dir, {
        'started_at':   start_ts.isoformat(),
        'version':      VERSION,
        'architecture': 'BiomedCLIP v7.6 (Full 686 SurgWound Dataset + LDAM LR Warm-Restart + Base Paper Metrics)',
        'changes_from_v75': 'Trained on the complete official 686-image dataset (480 train / 69 val / 137 test) directly unpacked from Hugging Face with all 8 attributes and base-paper benchmark comparisons',
    })

    log_path = os.path.join(run_dir, "training_log.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"SurgWound Pipeline {VERSION} (BiomedCLIP) — {start_ts}\nDevice: {device}\n\n")

    df       = pd.read_csv('../../data/annotations.csv')
    df_train = df[df['split'] == 'train'].reset_index(drop=True)
    df_val   = df[df['split'] == 'val'].reset_index(drop=True)

    print(f"\n[pipeline] Step 1: BiomedCLIP End-to-End Fine-Tuning ({VERSION})...")
    from train import train_biomedclip
    res = train_biomedclip(
        df_train=df_train,
        df_val=df_val,
        run_dir=run_dir,
        epochs=80,
        lr=3e-5,          # v7.2: Restored - worked in v7.0 Focal phase
        lr_decay=0.85,
        weight_decay=1e-3,
        batch_size=16,
        accum_steps=2,    # v7.2: Restored - worked in v7.0
        warmup_ratio=0.1,
        drw_epoch=0.7,    # v7.2: Keep - LDAM at ep56 (70%)
        patience=20,      # v7.2: Keep
        seed=42,
        device=device,
    )

    print(f"\n[pipeline] Training Complete. Best Val Mean Macro-F1: {res['best_val_f1']*100:.2f}%")

    print("\n[pipeline] Step 2: Evaluating with 7x Test-Time Augmentation...")
    from evaluate import run_biomedclip_evaluation
    metrics = run_biomedclip_evaluation(run_dir, df, use_tta=True)
    agg = metrics['aggregate']

    elapsed = (datetime.now() - start_ts).total_seconds() / 60
    print(f"\n{'='*60}")
    print(f"  OK {VERSION} BIOMEDCLIP PIPELINE COMPLETE")
    print(f"  Elapsed: {elapsed:.1f} min")
    print(f"  Run dir: {run_dir}/")
    print(f"  Final Mean Macro-F1 (TTA): {agg['mean_macro_f1']*100:.2f}%")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
