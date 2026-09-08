import os
import pandas as pd
import numpy as np
import torch
from scipy.special import softmax as stable_softmax  # BUG FIX #9: stable (no overflow)
from sklearn.metrics import f1_score
from heads_mlp import MLPHead, CLASS_MAPPINGS, EmbeddingDataset, normalize_label
import warnings
warnings.filterwarnings("ignore")

ORDERED_ATTRIBUTES = list(CLASS_MAPPINGS.keys())

def get_class_priors(df, attr):
    labels = [normalize_label(attr, str(x)) for x in df[attr]]
    counts = np.bincount(labels, minlength=len(CLASS_MAPPINGS[attr]))
    priors = counts / counts.sum()
    priors = np.clip(priors, 1e-6, 1.0)
    return priors

def optimize_thresholds(val_probs, val_targets, num_classes):
    best_th = np.ones(num_classes)
    for c in range(num_classes):
        best_f1 = -1
        best_t = 1.0
        for t in np.linspace(0.01, 1.0, 100):
            th_vec = np.ones(num_classes)
            th_vec[c] = t
            scaled_probs = val_probs / th_vec
            preds = np.argmax(scaled_probs, axis=1)
            f1 = f1_score(val_targets, preds, average='macro', zero_division=0)
            if f1 > best_f1:
                best_f1 = f1
                best_t = t
        best_th[c] = best_t
    return best_th

def run():
    df = pd.read_csv('data/annotations.csv')
    train_df = df[df['split'] == 'train'].reset_index(drop=True)
    val_df = df[df['split'] == 'val'].reset_index(drop=True)
    test_df = df[df['split'] == 'test'].reset_index(drop=True)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    models = {'dinov2': {}, 'clip': {}}
    for backbone in ['dinov2', 'clip']:
        for attr in ORDERED_ATTRIBUTES:
            ds = EmbeddingDataset(test_df, backbone, attr)
            in_dim = ds.features.shape[1]
            num_cls = len(CLASS_MAPPINGS[attr])
            
            m = MLPHead(in_dim, 256, num_cls).to(device)
            ckpt_path = f'checkpoints/mlp_{backbone}_{attr}.pth'
            if os.path.exists(ckpt_path):
                m.load_state_dict(torch.load(ckpt_path, map_location=device))
            m.eval()
            models[backbone][attr] = m
            
    def get_logits(split_df):
        all_logits = {attr: {} for attr in ORDERED_ATTRIBUTES}
        targets = {}
        for attr in ORDERED_ATTRIBUTES:
            targets[attr] = np.array([normalize_label(attr, str(x)) for x in split_df[attr]])
            for backbone in ['dinov2', 'clip']:
                ds = EmbeddingDataset(split_df, backbone, attr)
                feats = torch.tensor(ds.features, dtype=torch.float32).to(device)
                with torch.no_grad():
                    logits = models[backbone][attr](feats).cpu().numpy()
                all_logits[attr][backbone] = logits
        return all_logits, targets

    val_logits, val_targets = get_logits(val_df)
    test_logits, test_targets = get_logits(test_df)
    
    results = {}
    
    # 1. Baseline DINOv2+CLIP
    baseline_f1s = {}
    for attr in ORDERED_ATTRIBUTES:
        # BUG FIX #9: was np.exp()/np.sum(np.exp()) which overflows for large logits
        t_probs = (stable_softmax(test_logits[attr]['dinov2'], axis=1) +
                   stable_softmax(test_logits[attr]['clip'], axis=1)) / 2
        preds = np.argmax(t_probs, axis=1)
        baseline_f1s[attr] = f1_score(test_targets[attr], preds, average='macro', zero_division=0)
    results['Baseline DINOv2+CLIP (reported)'] = baseline_f1s
    
    # 2. + per-class threshold tuning (no retrain)
    th_f1s = {}
    for attr in ORDERED_ATTRIBUTES:
        v_probs = (stable_softmax(val_logits[attr]['dinov2'], axis=1) +
                   stable_softmax(val_logits[attr]['clip'], axis=1)) / 2
        t_probs = (stable_softmax(test_logits[attr]['dinov2'], axis=1) +
                   stable_softmax(test_logits[attr]['clip'], axis=1)) / 2
        
        num_classes = len(CLASS_MAPPINGS[attr])
        best_th = optimize_thresholds(v_probs, val_targets[attr], num_classes)
        scaled_t_probs = t_probs / best_th
        preds = np.argmax(scaled_t_probs, axis=1)
        th_f1s[attr] = f1_score(test_targets[attr], preds, average='macro', zero_division=0)
    results['+ per-class threshold tuning (no retrain)'] = th_f1s
    
    # 3. + logit adjustment
    # Note: Using logit adjustment ON TOP of threshold tuning, as requested sequentially
    la_th_f1s = {}
    for attr in ORDERED_ATTRIBUTES:
        priors = get_class_priors(train_df, attr)
        log_priors = np.log(priors)
        
        v_logits_dino = val_logits[attr]['dinov2'] - log_priors
        v_logits_clip = val_logits[attr]['clip'] - log_priors
        v_probs = (stable_softmax(v_logits_dino, axis=1) +
                   stable_softmax(v_logits_clip, axis=1)) / 2
                   
        t_logits_dino = test_logits[attr]['dinov2'] - log_priors
        t_logits_clip = test_logits[attr]['clip'] - log_priors
        t_probs = (stable_softmax(t_logits_dino, axis=1) +
                   stable_softmax(t_logits_clip, axis=1)) / 2
                   
        num_classes = len(CLASS_MAPPINGS[attr])
        best_th = optimize_thresholds(v_probs, val_targets[attr], num_classes)
        
        scaled_t_probs = t_probs / best_th
        preds = np.argmax(scaled_t_probs, axis=1)
        la_th_f1s[attr] = f1_score(test_targets[attr], preds, average='macro', zero_division=0)
    results['+ logit adjustment'] = la_th_f1s

    print("\nInference Fixes Results (Test Macro-F1):")
    cols = ['exudate_type', 'infection_risk', 'urgency_level', 'closure_method']
    print(f"{'Config':<40} | {'Exudate Type':<15} | {'Infection Risk':<15} | {'Urgency Level':<15} | {'Closure Method':<15} | {'Mean (All Heads)'}")
    
    for row in ['Baseline DINOv2+CLIP (reported)', '+ per-class threshold tuning (no retrain)', '+ logit adjustment']:
        res = results[row]
        vals = [f"{res[c]*100:.2f}%" for c in cols]
        mean_all = np.mean([res[c] for c in ORDERED_ATTRIBUTES]) * 100
        print(f"{row:<40} | {vals[0]:<15} | {vals[1]:<15} | {vals[2]:<15} | {vals[3]:<15} | {mean_all:.2f}%")

if __name__ == "__main__":
    run()
