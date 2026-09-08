"""
tune.py — Optuna Hyperparameter Optimization for Early Fusion Networks.
"""
import os
import json
import optuna
import torch
from config import BASE_ATTRIBUTES, IMBALANCED_HEADS, TRAIN_DEFAULTS
from train import train_one_head

def _quick_train(attr: str, df_train, df_val, params: dict, device, epochs: int):
    res = train_one_head(
        attr=attr,
        df_train=df_train,
        df_val=df_val,
        run_dir="runs/optuna_tmp",
        epochs=epochs,
        lr=params['lr'],
        weight_decay=params['weight_decay'],
        dropout=params['dropout'],
        hidden_dim=params['hidden_dim'],
        focal_gamma=params['focal_gamma'],
        drw_epoch=0.6,
        patience=10,
        apply_smote=(attr in IMBALANCED_HEADS),
        device=device,
    )
    return res['best_val_f1']

def run_optuna_for_attr(attr: str, df_train, df_val, n_trials=30, device=None):
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    os.makedirs("runs/optuna_tmp/checkpoints", exist_ok=True)

    def objective(trial):
        params = {
            'lr': trial.suggest_float('lr', 1e-4, 5e-3, log=True),
            'weight_decay': trial.suggest_float('weight_decay', 1e-5, 1e-2, log=True),
            'dropout': trial.suggest_float('dropout', 0.1, 0.5),
            'hidden_dim': trial.suggest_categorical('hidden_dim', [512, 1024, 2048]),
            'focal_gamma': trial.suggest_float('focal_gamma', 1.0, 3.0),
        }
        return _quick_train(attr, df_train, df_val, params, device, epochs=60)

    study = optuna.create_study(direction="maximize")
    print(f"\n  [Optuna] {attr}: {n_trials} trials...")
    study.optimize(objective, n_trials=n_trials, show_progress_bar=False)

    print(f"  [Optuna] Best val_macro_f1: {study.best_value:.4f}")
    print(f"  [Optuna] Params: {study.best_params}")
    return study.best_params

def tune_all_heads(df_train, df_val, run_dir: str, n_trials=30):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    best_params = {}
    
    total = len(BASE_ATTRIBUTES)
    for i, attr in enumerate(BASE_ATTRIBUTES, 1):
        print(f"\n[{i}/{total}] Optimizing {attr}")
        best = run_optuna_for_attr(attr, df_train, df_val, n_trials=n_trials, device=device)
        best_params[attr] = best

    out_path = os.path.join(run_dir, "optuna_best_params.json")
    with open(out_path, 'w') as f:
        json.dump(best_params, f, indent=4)
    print(f"\n[tune] All HPO complete. Saved to {out_path}")
    return best_params
