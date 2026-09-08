"""
v8/analysis/inspect_errors.py — Error inspection and diagnostic visualizer.
Loads the latest trained checkpoint, runs inference on the test set, and identifies
all misclassified samples per attribute to isolate failure patterns.
"""
import os
import sys
import torch
import numpy as np
import pandas as pd
from typing import Dict, List

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS, BIOMEDCLIP_MODEL_ID
from model import BiomedCLIPMultiTaskModel
from dataset import SurgWoundDataset
from evaluate import evaluate_model
import open_clip


import argparse

def get_latest_run_dir(base_dir: str = 'v8/runs') -> str:
    runs = [os.path.join(base_dir, d) for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    if not runs:
        return None
    # Sort by timestamp in folder name: e.g. v8_e1_la_textproto_20260904_172547
    def _extract_ts(path):
        parts = os.path.basename(path).split('_')
        for i in range(len(parts) - 1):
            if len(parts[i]) == 8 and parts[i].isdigit() and len(parts[i+1]) == 6 and parts[i+1].isdigit():
                return parts[i] + parts[i+1]
        return os.path.basename(path)
    runs.sort(key=_extract_ts)
    return runs[-1]


def main():
    run_dir = get_latest_run_dir()
    if not run_dir:
        print("[inspect_errors] No runs found in v8/runs/")
        return

    print(f"[inspect_errors] Analyzing latest run: {run_dir}")
    ckpt_path = os.path.join(run_dir, "checkpoints", "best_model.pth")
    if not os.path.exists(ckpt_path):
        print(f"[inspect_errors] Checkpoint not found: {ckpt_path}")
        return

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = BiomedCLIPMultiTaskModel(use_text_prototypes=True).to(device)
    model.load_state_dict(torch.load(ckpt_path, map_location=device))
    model.eval()

    df = pd.read_csv('archive/dataset_backup_v7/annotations.csv')
    df_test = df[df['split'] == 'test'].reset_index(drop=True)

    metrics, probs, targets = evaluate_model(
        model=model,
        df_eval=df_test,
        device=device,
        use_tta=True,
        tta_n=7,
        legacy_mode=True,
    )

    # Detailed per-image error audit
    error_records = []
    for i in range(len(df_test)):
        row = df_test.iloc[i]
        img_name = row['image_name']
        img_errors = {}
        for attr in BASE_ATTRIBUTES:
            pred_cls = int(np.argmax(probs[attr][i]))
            true_cls = targets[attr][i]
            if pred_cls != true_cls:
                pred_name = CLASS_MAPPINGS[attr][pred_cls]
                true_name = CLASS_MAPPINGS[attr][true_cls]
                conf = probs[attr][i][pred_cls]
                img_errors[attr] = f"True: {true_name} -> Pred: {pred_name} (conf={conf*100:.1f}%)"

        if img_errors:
            error_records.append({
                'image_name': img_name,
                'num_errors': len(img_errors),
                'details': img_errors,
            })

    # Sort images by error count
    error_records.sort(key=lambda x: x['num_errors'], reverse=True)

    out_md = os.path.join(run_dir, "error_analysis_report.md")
    lines = [
        f"# SurgWound Assist v8 — Test Error Analysis",
        f"**Run**: `{os.path.basename(run_dir)}`",
        f"**Total Test Samples**: {len(df_test)}",
        f"**Samples with at least 1 error**: {len(error_records)} / {len(df_test)} ({len(error_records)/len(df_test)*100:.1f}%)",
        f"**Exact Match Samples**: {len(df_test) - len(error_records)} / {len(df_test)} ({(len(df_test) - len(error_records))/len(df_test)*100:.1f}%)",
        "",
        "## Most Frequent Misclassifications by Attribute",
    ]

    for attr in BASE_ATTRIBUTES:
        h = metrics['per_head'][attr]
        lines.append(f"### {attr.upper()} (F1: {h['macro_f1']*100:.2f}%, Acc: {h['accuracy']*100:.2f}%)")
        cm = np.array(h['confusion_matrix'])
        classes = CLASS_MAPPINGS[attr]
        confused_pairs = []
        for r in range(len(classes)):
            for c in range(len(classes)):
                if r != c and cm[r, c] > 0:
                    confused_pairs.append((classes[r], classes[c], cm[r, c]))
        confused_pairs.sort(key=lambda x: x[2], reverse=True)

        if confused_pairs:
            lines.append("| True Class | Misclassified As | Count |")
            lines.append("|---|---|---|")
            for t_cls, p_cls, cnt in confused_pairs:
                lines.append(f"| {t_cls} | {p_cls} | {cnt} |")
        else:
            lines.append("*(No errors for this attribute)*")
        lines.append("")

    lines.append("## Top Hardest Test Images (Most Errors)")
    lines.append("| Image | Error Count | Details |")
    lines.append("|---|---|---|")
    for rec in error_records[:15]:
        det_str = "<br/>".join([f"**{a}**: {d}" for a, d in rec['details'].items()])
        lines.append(f"| `{rec['image_name']}` | {rec['num_errors']} / 8 | {det_str} |")

    with open(out_md, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"[inspect_errors] Error analysis report generated -> {out_md}")


if __name__ == '__main__':
    main()
