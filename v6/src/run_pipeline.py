"""
run_pipeline.py — v4.0 End-to-End Pipeline Orchestrator.
"""
import os
import sys
import torch
import pandas as pd
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import create_run_dir, save_run_config

def check_gpu():
    print("\n" + "=" * 60)
    print("DEVICE CHECK")
    print("=" * 60)
    if torch.cuda.is_available():
        name  = torch.cuda.get_device_name(0)
        vram  = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"  GPU             : {name}")
        print(f"  VRAM            : {vram:.1f} GB")
        device = torch.device('cuda')
    else:
        print("  GPU             : NOT AVAILABLE — running on CPU")
        device = torch.device('cpu')
    print("=" * 60 + "\n")
    return device

def main():
    start_ts = datetime.now()
    device = check_gpu()
    run_dir = create_run_dir()
    
    save_run_config(run_dir, {
        'started_at': start_ts.isoformat(),
        'architecture': 'End-to-End Fine-Tuning v4.0'
    })

    log_path = os.path.join(run_dir, "training_log.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write(f"SurgWound Pipeline v4.0 (End-to-End) — {start_ts}\nDevice: {device}\n\n")

    df = pd.read_csv('data/annotations.csv')
    df_train = df[df['split'] == 'train'].reset_index(drop=True)
    df_val   = df[df['split'] == 'val'].reset_index(drop=True)

    print("\n[pipeline] Step 1: End-to-End Fine-Tuning of DINOv2...")
    from train import train_end_to_end
    
    # Using small batch size and accumulation to fit 6GB VRAM
    res = train_end_to_end(
        df_train=df_train,
        df_val=df_val,
        run_dir=run_dir,
        epochs=60,
        lr=1e-5,
        lr_decay=0.85,       # LLRD: each backbone layer gets 85% LR of the layer above
        weight_decay=1e-3,
        batch_size=4,
        accum_steps=4,
        warmup_ratio=0.1,    # 10% warm-up steps
        seed=42,             # Fixed seed for reproducibility
        device=device
    )

    print(f"\n[pipeline] Training Complete. Best Mean Macro-F1: {res['best_val_f1']*100:.2f}%")

    print("\n[pipeline] Step 2: Evaluating on test set...")
    from evaluate import run_evaluation
    metrics = run_evaluation(run_dir, df)
    agg = metrics['aggregate']

    print("\n[pipeline] Step 3: Exporting ONNX model...")
    from export_onnx import export_onnx
    onnx_path = export_onnx(run_dir)

    elapsed = (datetime.now() - start_ts).total_seconds() / 60
    print(f"\n{'='*60}")
    print(f"  ✓ v4.0 PIPELINE COMPLETE")
    print(f"  Elapsed: {elapsed:.1f} min")
    print(f"  Run dir: {run_dir}/")
    print(f"  Final Mean Macro-F1: {agg['mean_macro_f1']*100:.2f}%")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
