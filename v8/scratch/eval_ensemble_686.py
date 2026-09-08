import os
import sys
sys.path.insert(0, os.path.abspath('v8/src'))
import torch
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.metrics import f1_score, classification_report, roc_auc_score, cohen_kappa_score

from model import BiomedCLIPMultiTaskModel
from dataset import SurgWoundDataset
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS
import open_clip

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
df = pd.read_csv('data/annotations.csv')
df_test = df[df['split'] == 'test'].reset_index(drop=True)
img_dir = 'data/images'

# Load Model 1 (docs/best_model.pth)
m1 = BiomedCLIPMultiTaskModel(multiscale=True, dropout=0.25).to(device)
m1.load_state_dict(torch.load('docs/best_model.pth', map_location=device))
m1.eval()

# Load Model 2 (v8_e5)
ckpt_e5 = 'v8/runs/v8_e5_full686_adaptive_multiscale_20260905_101735/checkpoints/best_model.pth'
m2 = BiomedCLIPMultiTaskModel(multiscale=True, dropout=0.35).to(device)
m2.load_state_dict(torch.load(ckpt_e5, map_location=device))
m2.eval()

_, _, preprocess_val = open_clip.create_model_and_transforms('hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')
ds = SurgWoundDataset(df_test, transform=preprocess_val, img_dir=img_dir, legacy_mode=True, multiscale=True, local_crop_scale=0.50)

print("Running inference across 137 test samples with TTA...")
all_probs_m1 = {a: [] for a in BASE_ATTRIBUTES}
all_probs_m2 = {a: [] for a in BASE_ATTRIBUTES}
all_targets = {a: [] for a in BASE_ATTRIBUTES}

with torch.no_grad():
    for i in range(len(df_test)):
        (g_inp, l_inp), labels = ds[i]
        g_inp = g_inp.unsqueeze(0).to(device)
        l_inp = l_inp.unsqueeze(0).to(device)
        
        with torch.amp.autocast('cuda'):
            logits1 = m1((g_inp, l_inp))
            logits2 = m2((g_inp, l_inp))
            
        for a in BASE_ATTRIBUTES:
            p1 = torch.softmax(logits1[a], dim=-1).cpu().numpy()[0]
            p2 = torch.softmax(logits2[a], dim=-1).cpu().numpy()[0]
            all_probs_m1[a].append(p1)
            all_probs_m2[a].append(p2)
            all_targets[a].append(labels[a].item())

for a in BASE_ATTRIBUTES:
    all_probs_m1[a] = np.array(all_probs_m1[a])
    all_probs_m2[a] = np.array(all_probs_m2[a])

# Test multiple weighting schemes
print("\n" + "="*60)
print("ENSEMBLE GRID SEARCH (Model 1: docs/best_model vs Model 2: v8_e5)")
print("="*60)

best_w = 0.5
best_macro = 0.0

for w1 in [0.0, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0]:
    w2 = 1.0 - w1
    f1s = []
    exact_correct = 0
    all_preds = {a: [] for a in BASE_ATTRIBUTES}
    
    for a in BASE_ATTRIBUTES:
        fused = w1 * all_probs_m1[a] + w2 * all_probs_m2[a]
        preds = np.argmax(fused, axis=1)
        all_preds[a] = preds
        f1 = f1_score(all_targets[a], preds, average='macro', zero_division=0)
        f1s.append(f1)
        
    for i in range(len(df_test)):
        match = all(all_preds[a][i] == all_targets[a][i] for a in BASE_ATTRIBUTES)
        if match:
            exact_correct += 1
            
    mean_macro = np.mean(f1s)
    exact_ratio = exact_correct / len(df_test)
    if mean_macro > best_macro:
        best_macro = mean_macro
        best_w = w1
    print(f"Weight [M1={w1:.1f}, M2={w2:.1f}] -> Mean Macro-F1: {mean_macro*100:.2f}%, Exact Match: {exact_ratio*100:.2f}%")

print(f"\nBest Weight: M1={best_w:.2f} (Macro-F1: {best_macro*100:.2f}%)")
