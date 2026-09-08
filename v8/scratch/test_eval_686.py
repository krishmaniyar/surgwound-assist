import os
import sys
sys.path.insert(0, os.path.abspath('v8/src'))
import torch
import pandas as pd
from model import BiomedCLIPMultiTaskModel
from evaluate import evaluate_model
from config import BASE_ATTRIBUTES

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
df = pd.read_csv('data/annotations.csv')
df_test = df[df['split'] == 'test'].reset_index(drop=True)
print(f'Official Test Samples: {len(df_test)}')

ckpt_path = 'docs/best_model.pth'
if os.path.exists(ckpt_path):
    print(f'Checking {ckpt_path}...')
    try:
        model = BiomedCLIPMultiTaskModel(multiscale=True).to(device)
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
        metrics, _, _ = evaluate_model(model, df_test, device, use_tta=True, tta_n=7, img_dir='data/images', multiscale=True)
        print(f"docs/best_model.pth (multiscale) on 686 test set: Macro-F1 = {metrics['aggregate']['mean_macro_f1']*100:.2f}%, Exact Match = {metrics['aggregate']['exact_match_ratio']*100:.2f}%")
        for a in BASE_ATTRIBUTES:
            print(f"  {a:16s}: {metrics['per_head'][a]['macro_f1']*100:.2f}%")
    except Exception as e:
        print(f'Multiscale failed: {e}')
        model = BiomedCLIPMultiTaskModel(multiscale=False).to(device)
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
        metrics, _, _ = evaluate_model(model, df_test, device, use_tta=True, tta_n=7, img_dir='data/images', multiscale=False)
        print(f"docs/best_model.pth (single-scale) on 686 test set: Macro-F1 = {metrics['aggregate']['mean_macro_f1']*100:.2f}%, Exact Match = {metrics['aggregate']['exact_match_ratio']*100:.2f}%")
        for a in BASE_ATTRIBUTES:
            print(f"  {a:16s}: {metrics['per_attribute'][a]['macro_f1']*100:.2f}%")
