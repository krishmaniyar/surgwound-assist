import os
import sys
sys.path.insert(0, os.path.abspath('v8/src'))
import torch
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, roc_auc_score, cohen_kappa_score

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

w1, w2 = 0.60, 0.40
print(f"\n=======================================================")
print(f"OFFICIAL 137 TEST BENCHMARK — ENSEMBLE (M1: 0.60, M2: 0.40)")
print(f"=======================================================")

macro_f1s = []
exact_matches = 0
all_preds = {a: [] for a in BASE_ATTRIBUTES}

for a in BASE_ATTRIBUTES:
    probs = w1 * all_probs_m1[a] + w2 * all_probs_m2[a]
    preds = np.argmax(probs, axis=1)
    all_preds[a] = preds
    rep = classification_report(all_targets[a], preds, output_dict=True, zero_division=0)
    f1 = rep['macro avg']['f1-score']
    acc = rep['accuracy']
    macro_f1s.append(f1)
    print(f"  {a:16s}: Macro-F1 = {f1*100:5.2f}% | Accuracy = {acc*100:5.2f}%")

for i in range(len(df_test)):
    if all(all_preds[a][i] == all_targets[a][i] for a in BASE_ATTRIBUTES):
        exact_matches += 1

print("-------------------------------------------------------")
print(f"MEAN TEST MACRO-F1 : {np.mean(macro_f1s)*100:.2f}%")
print(f"EXACT MATCH RATIO  : {exact_matches/len(df_test)*100:.2f}% ({exact_matches}/{len(df_test)})")
print("=======================================================")
