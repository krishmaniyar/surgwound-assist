"""
v8/scratch/evaluate_multi_regime_ensemble.py — Evaluates Multi-Regime Deep Ensembles.
Tests combinations of:
- Canonical Pristine Anchors (v8_e1_la, v8_e2_multiscale)
- Full-686 Multi-Scale Models (v8_e1_full686, v8_e2_full686, v8_e3_full686, v8_e4_full686)
- Full-686 Specialists (v8_e5_adaptive, v8_e6_mixup)
"""
import os
import sys
import json
import torch
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from ensemble import run_ensemble_evaluation, optimize_ensemble_blend_weights
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RUNS_DIR = os.path.join(PROJECT_ROOT, "v8", "runs")

def get_spec(run_name, multiscale=True, crop=0.65):
    p = os.path.join(RUNS_DIR, run_name)
    return {
        'name': run_name,
        'ckpt_path': os.path.join(p, 'checkpoints', 'best_model.pth'),
        'multiscale': multiscale,
        'use_text_prototypes': True,
        'legacy_mode': True,
        'crop_scale': crop,
    }

# All candidate models
models_pool = {
    'e1_canonical': get_spec('v8_e1_la_textproto_20260904_172547', multiscale=False),
    'e2_canonical': get_spec('v8_e2_multiscale_20260904_174157', multiscale=True, crop=0.65),
    'e1_full686': get_spec('v8_e1_full686_textproto_20260905_113337', multiscale=False),
    'e2_full686': get_spec('v8_e2_full686_multiscale_20260905_114327', multiscale=True, crop=0.65),
    'e3_full686': get_spec('v8_e3_full686_multiscale_s123_20260905_115550', multiscale=True, crop=0.65),
    'e4_full686': get_spec('v8_e4_full686_balanced_tau12_20260905_120658', multiscale=True, crop=0.65),
    'e5_full686': get_spec('v8_e5_full686_adaptive_multiscale_20260905_101735', multiscale=True, crop=0.50),
    'e6_full686': get_spec('v8_e6_mixup_smoothing_s7_20260905_105544', multiscale=True, crop=0.50),
}

# Verify checkpoints exist
for k, v in models_pool.items():
    exists = os.path.exists(v['ckpt_path'])
    print(f"[{'OK' if exists else 'MISSING'}] {k}: {v['ckpt_path']}")

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
df = pd.read_csv(os.path.join(PROJECT_ROOT, "data", "annotations.csv"))
df_val = df[df['split'] == 'val'].reset_index(drop=True)
df_test = df[df['split'] == 'test'].reset_index(drop=True)

# Test 1: SOTA Quad Ensemble Re-check (e1_can + e2_can + e5_full + e6_full)
print("\n" + "="*80)
print("TEST 1: SOTA Quad Ensemble (e1_canonical + e2_canonical + e5_full686 + e6_full686)")
print("="*80)
specs_quad = [models_pool['e1_canonical'], models_pool['e2_canonical'], models_pool['e5_full686'], models_pool['e6_full686']]
weights_quad = [0.35, 0.45, 0.10, 0.10]
m1 = run_ensemble_evaluation(specs_quad, df_test, device, os.path.join(RUNS_DIR, "eval_test_quad"), tta_n=7, weights=weights_quad, df_val=df_val)

# Test 2: Multi-Regime Hexa Ensemble (e2_can, e1_full, e2_full, e3_full, e5_full, e6_full)
print("\n" + "="*80)
print("TEST 2: Multi-Regime Hexa Ensemble with balanced weights")
print("="*80)
specs_hexa = [
    models_pool['e2_canonical'],  # 349 anchor
    models_pool['e1_full686'],   # 686 textproto
    models_pool['e2_full686'],   # 686 multiscale s42
    models_pool['e3_full686'],   # 686 multiscale s123
    models_pool['e5_full686'],   # 686 emergency recall
    models_pool['e6_full686'],   # 686 mixup safety
]
weights_hexa = [0.30, 0.20, 0.20, 0.15, 0.10, 0.05]
m2 = run_ensemble_evaluation(specs_hexa, df_test, device, os.path.join(RUNS_DIR, "eval_test_hexa"), tta_n=7, weights=weights_hexa, df_val=df_val)

print("\n" + "="*80)
print("COMPARISON SUMMARY")
print(f"Quad SOTA:  Macro-F1={m1['aggregate']['mean_macro_f1']*100:.2f}%, ExactMatch={m1['aggregate']['exact_match_ratio']*100:.2f}%, AUC={m1['aggregate']['mean_roc_auc']:.4f}")
print(f"Hexa Fused: Macro-F1={m2['aggregate']['mean_macro_f1']*100:.2f}%, ExactMatch={m2['aggregate']['exact_match_ratio']*100:.2f}%, AUC={m2['aggregate']['mean_roc_auc']:.4f}")
print("="*80)
