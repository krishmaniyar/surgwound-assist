"""
v8/src/train.py — Training Engine with Automated Failure Detection,
LLRD Optimization, Multi-Loss Strategy, and Metric Logging.
"""
import os
import copy
import math
import time
import json
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, WeightedRandomSampler
from sklearn.metrics import f1_score
from typing import Dict, Any, Optional

from config import BASE_ATTRIBUTES, CLASS_MAPPINGS, BIOMEDCLIP_MODEL_ID
from dataset import SurgWoundDataset, normalize_label
from model import BiomedCLIPMultiTaskModel
from losses import FocalLoss, LDAMLoss, LogitAdjustedLoss, AdaptiveTauLogitAdjustedLoss, BalancedSoftmaxLoss, get_cb_weights
import open_clip


def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def _seed_worker(worker_id):
    worker_seed = torch.initial_seed() % (2**32)
    np.random.seed(worker_seed)
    random.seed(worker_seed)


def get_cosine_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, min_lr=1e-7):
    def lr_lambda(current_step):
        if current_step < num_warmup_steps:
            return float(current_step) / float(max(1, num_warmup_steps))
        progress = float(current_step - num_warmup_steps) / float(max(1, num_training_steps - num_warmup_steps))
        return max(min_lr, 0.5 * (1.0 + math.cos(math.pi * progress)))
    return optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


def train_v8_model(
    df_train: pd.DataFrame,
    df_val: pd.DataFrame,
    run_dir: str,
    loss_strategy: str  = 'logit_adjusted', # 'logit_adjusted', 'adaptive_logit_adjusted', 'balanced_softmax', 'focal_ldam', 'focal'
    epochs: int         = 80,
    lr: float           = 3e-5,
    lr_decay: float     = 0.85,
    weight_decay: float = 1e-3,
    dropout: float      = 0.25,
    batch_size: int     = 16,
    accum_steps: int    = 2,
    warmup_ratio: float = 0.1,
    patience: int       = 20,
    seed: int           = 42,
    legacy_mode: bool   = True,
    multiscale: bool    = False,
    use_text_prototypes: bool = True,
    use_balanced_sampler: bool = False,
    local_crop_scale: float = 0.65,
    adaptive_tau: bool  = False,
    drw_epoch: float    = 0.7,   # For focal_ldam strategy
    ldam_restart_lr: float = 1e-5,
    tau: float          = 1.0,   # For logit_adjusted
    label_smoothing: float = 0.0,  # Label smoothing epsilon (0.0 = off, 0.1 recommended)
    use_mixup: bool     = False,  # MixUp augmentation (alpha=0.2)
    img_dir: str        = 'data/images',
    device              = None,
) -> Dict[str, Any]:
    """
    Executes an end-to-end training run with real-time monitoring and diagnostics.
    """
    set_seed(seed)
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    os.makedirs(run_dir, exist_ok=True)
    log_path = os.path.join(run_dir, "training_log.txt")

    def _log(msg: str):
        print(msg)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    _log("=" * 70)
    _log(f"SURGWOUND ASSIST V8 TRAINING — Strategy: {loss_strategy.upper()}")
    _log(f"Device: {device} | Epochs: {epochs} | Batch: {batch_size} | Accum: {accum_steps} | LR: {lr:.2e} | Dropout: {dropout}")
    _log(f"Multiscale: {multiscale} (Crop: {local_crop_scale}) | Balanced Sampler: {use_balanced_sampler} | Text Prototypes: {use_text_prototypes}")
    _log(f"Tau: {tau} | Adaptive Tau: {adaptive_tau} | Legacy Mode: {legacy_mode} | Seed: {seed} | Patience: {patience}")
    _log(f"Label Smoothing: {label_smoothing} | MixUp: {use_mixup} | Effective Batch: {batch_size * accum_steps}")
    _log("=" * 70)

    # BiomedCLIP image transforms
    _, preprocess_train, preprocess_val = open_clip.create_model_and_transforms(BIOMEDCLIP_MODEL_ID)

    ds_train = SurgWoundDataset(
        df_train,
        transform=preprocess_train,
        img_dir=img_dir,
        legacy_mode=legacy_mode,
        multiscale=multiscale,
        local_crop_scale=local_crop_scale,
    )
    ds_val = SurgWoundDataset(
        df_val,
        transform=preprocess_val,
        img_dir=img_dir,
        legacy_mode=legacy_mode,
        multiscale=multiscale,
        local_crop_scale=local_crop_scale,
    )

    g = torch.Generator()
    g.manual_seed(seed)

    # Precompute integer labels directly from dataframe (instantaneous, avoids opening images)
    train_labels = {
        attr: [normalize_label(df_train.iloc[i].get(attr), attr, legacy_mode=legacy_mode) for i in range(len(df_train))]
        for attr in BASE_ATTRIBUTES
    }

    if use_balanced_sampler:
        head_inv_freq = {}
        for attr in BASE_ATTRIBUTES:
            num_classes = len(CLASS_MAPPINGS[attr])
            labels = train_labels[attr]
            counts = np.bincount(labels, minlength=num_classes)
            safe_counts = np.where(counts == 0, 1.0, counts.astype(float))
            inv_freq = 1.0 / np.sqrt(safe_counts)
            inv_freq = inv_freq / inv_freq.sum()
            head_inv_freq[attr] = inv_freq

        attr_weights = {
            'location': 1.5,
            'healing_status': 1.0,
            'closure_method': 3.0,
            'exudate_type': 3.0,
            'erythema': 1.0,
            'edema': 2.0,
            'infection_risk': 3.0,
            'urgency_level': 3.0,
        }

        sample_weights = []
        for i in range(len(df_train)):
            sw = 0.0
            for attr in BASE_ATTRIBUTES:
                label_idx = train_labels[attr][i]
                sw += attr_weights.get(attr, 1.0) * head_inv_freq[attr][label_idx]
            sample_weights.append(sw)

        sampler_weights = torch.tensor(sample_weights, dtype=torch.double)
        sampler = WeightedRandomSampler(
            weights=sampler_weights,
            num_samples=len(sampler_weights),
            replacement=True,
            generator=g,
        )
        train_loader = DataLoader(
            ds_train, batch_size=batch_size, sampler=sampler,
            pin_memory=(device.type == 'cuda'), num_workers=0,
            worker_init_fn=_seed_worker,
        )
        _log(f"[train] Balanced Sampler enabled: min_w={sampler_weights.min():.4f}, max_w={sampler_weights.max():.4f}, ratio={sampler_weights.max()/sampler_weights.min():.2f}x")
    else:
        train_loader = DataLoader(
            ds_train, batch_size=batch_size, shuffle=True,
            pin_memory=(device.type == 'cuda'), num_workers=0,
            worker_init_fn=_seed_worker, generator=g,
        )
    val_loader = DataLoader(ds_val, batch_size=batch_size * 2, shuffle=False, num_workers=0)

    # Initialize loss functions per attribute
    criterions_p1 = {}
    criterions_p2 = {}

    for attr in BASE_ATTRIBUTES:
        num_classes = len(CLASS_MAPPINGS[attr])
        labels = train_labels[attr]
        cls_num_list = np.bincount(labels, minlength=num_classes).tolist()
        cb_weights = get_cb_weights(cls_num_list).to(device)

        if loss_strategy == 'adaptive_logit_adjusted' or (loss_strategy == 'logit_adjusted' and adaptive_tau):
            criterions_p1[attr] = AdaptiveTauLogitAdjustedLoss(
                cls_num_list, base_tau=tau, label_smoothing=label_smoothing
            ).to(device)
            criterions_p2[attr] = criterions_p1[attr]
            _log(f"  Head {attr:16s}: Adaptive tau = {criterions_p1[attr].tau:.2f}  smooth={label_smoothing}")
        elif loss_strategy == 'logit_adjusted':
            criterions_p1[attr] = LogitAdjustedLoss(
                cls_num_list, tau=tau, label_smoothing=label_smoothing
            ).to(device)
            criterions_p2[attr] = criterions_p1[attr]
        elif loss_strategy == 'balanced_softmax':
            criterions_p1[attr] = BalancedSoftmaxLoss(cls_num_list).to(device)
            criterions_p2[attr] = criterions_p1[attr]
        elif loss_strategy == 'focal_ldam':
            criterions_p1[attr] = FocalLoss(alpha=cb_weights, gamma=2.0).to(device)
            criterions_p2[attr] = LDAMLoss(cls_num_list, max_m=0.5, s=15.0, weight=cb_weights).to(device)
        else: # pure focal
            criterions_p1[attr] = FocalLoss(alpha=cb_weights, gamma=2.0).to(device)
            criterions_p2[attr] = criterions_p1[attr]

    # Initialize model
    model = BiomedCLIPMultiTaskModel(
        dropout=dropout,
        hidden_dim=256,
        use_text_prototypes=use_text_prototypes,
        multiscale=multiscale,
    ).to(device)

    param_groups = model.get_llrd_param_groups(base_lr=lr, lr_decay=lr_decay, weight_decay=weight_decay)
    optimizer = optim.AdamW(param_groups)

    total_steps = (len(train_loader) // accum_steps) * epochs
    warmup_steps = int(total_steps * warmup_ratio)
    scheduler = get_cosine_schedule_with_warmup(optimizer, warmup_steps, total_steps)

    use_amp = (device.type == 'cuda')
    scaler = torch.amp.GradScaler('cuda') if use_amp else None

    best_val_f1 = 0.0
    best_weights = None
    no_improve = 0
    t0 = time.time()
    drw_start = int(epochs * drw_epoch) if loss_strategy == 'focal_ldam' else epochs + 1
    restarted_ldam = False

    history = []

    for epoch in range(epochs):
        # LDAM Warm restart handling if using focal_ldam
        if loss_strategy == 'focal_ldam' and epoch >= drw_start and not restarted_ldam:
            restarted_ldam = True
            no_improve = 0
            rem_epochs = epochs - drw_start
            p2_steps = (len(train_loader) // accum_steps) * rem_epochs
            for g_ in optimizer.param_groups:
                g_['lr'] = ldam_restart_lr
            scheduler = get_cosine_schedule_with_warmup(
                optimizer, num_warmup_steps=int(p2_steps * 0.05), num_training_steps=p2_steps, min_lr=1e-7
            )
            _log(f"\n>>> [Phase 2: LDAM Warm-Restart] LR reset to {ldam_restart_lr:.1e} <<<\n")

        phase_tag = "P1:Focal" if (loss_strategy == 'focal_ldam' and epoch < drw_start) else (
            "P2:LDAM" if (loss_strategy == 'focal_ldam') else loss_strategy.upper()
        )
        criterions = criterions_p1 if (loss_strategy == 'focal_ldam' and epoch < drw_start) else criterions_p2
        in_ldam = (phase_tag == "P2:LDAM")

        model.train()
        epoch_loss = 0.0
        optimizer.zero_grad()

        for batch_idx, (inputs, label_dict) in enumerate(train_loader):
            if multiscale:
                inputs = (inputs[0].to(device), inputs[1].to(device))
            else:
                inputs = inputs.to(device)

            targets = {a: label_dict[a].to(device) for a in BASE_ATTRIBUTES}

            # MixUp augmentation: 50% probability, alpha=0.2
            # Mixes image pairs and computes weighted sum of per-attribute losses
            apply_mixup = use_mixup and (not in_ldam) and (np.random.random() < 0.5)
            if apply_mixup:
                alpha = 0.2
                lam = float(np.random.beta(alpha, alpha))
                bs = inputs[0].size(0) if multiscale else inputs.size(0)
                mix_idx = torch.randperm(bs, device=device)
                if multiscale:
                    inputs = (
                        lam * inputs[0] + (1.0 - lam) * inputs[0][mix_idx],
                        lam * inputs[1] + (1.0 - lam) * inputs[1][mix_idx],
                    )
                else:
                    inputs = lam * inputs + (1.0 - lam) * inputs[mix_idx]
                targets_b = {a: targets[a][mix_idx] for a in BASE_ATTRIBUTES}

            # Safe AMP execution
            if use_amp and not in_ldam:
                with torch.amp.autocast('cuda'):
                    logits = model(inputs)
                    if apply_mixup:
                        loss = sum(
                            lam * criterions[a](logits[a], targets[a]) +
                            (1.0 - lam) * criterions[a](logits[a], targets_b[a])
                            for a in BASE_ATTRIBUTES
                        ) / accum_steps
                    else:
                        loss = sum(criterions[a](logits[a], targets[a]) for a in BASE_ATTRIBUTES) / accum_steps

                # Failure detection: Check for NaN / Inf
                if torch.isnan(loss) or torch.isinf(loss):
                    _log(f"[FATAL FAILURE] NaN/Inf loss encountered at epoch {epoch+1}, batch {batch_idx}! Stopping run.")
                    return {'status': 'FAILED', 'error': 'NaN/Inf loss', 'best_val_f1': best_val_f1}
                scaler.scale(loss).backward()

                if (batch_idx + 1) % accum_steps == 0 or (batch_idx + 1) == len(train_loader):
                    scaler.unscale_(optimizer)
                    grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    if math.isnan(grad_norm) or math.isinf(grad_norm):
                        # Expected during early GradScaler calibration: scale will be reduced automatically
                        pass
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad()
                    scheduler.step()
            else:
                # Full FP32 forward & backward (used for LDAM phase or CPU)
                logits = model(inputs)
                loss = sum(criterions[a](logits[a], targets[a]) for a in BASE_ATTRIBUTES) / accum_steps

                if torch.isnan(loss) or torch.isinf(loss):
                    _log(f"[FATAL FAILURE] NaN/Inf loss encountered in FP32 at epoch {epoch+1}!")
                    return {'status': 'FAILED', 'error': 'NaN/Inf loss', 'best_val_f1': best_val_f1}

                loss.backward()

                if (batch_idx + 1) % accum_steps == 0 or (batch_idx + 1) == len(train_loader):
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    optimizer.step()
                    optimizer.zero_grad()
                    scheduler.step()

            epoch_loss += loss.item() * accum_steps

        avg_loss = epoch_loss / len(train_loader)
        current_lr = optimizer.param_groups[0]['lr']

        # Validation evaluation
        model.eval()
        val_targets = {a: [] for a in BASE_ATTRIBUTES}
        val_preds = {a: [] for a in BASE_ATTRIBUTES}

        with torch.no_grad():
            for inputs, label_dict in val_loader:
                if multiscale:
                    inputs = (inputs[0].to(device), inputs[1].to(device))
                else:
                    inputs = inputs.to(device)

                with torch.amp.autocast('cuda') if use_amp else torch.no_grad():
                    logits = model(inputs)

                for a in BASE_ATTRIBUTES:
                    val_preds[a].extend(torch.argmax(logits[a], dim=1).cpu().numpy())
                    val_targets[a].extend(label_dict[a].numpy())

        macro_f1s = [
            f1_score(val_targets[a], val_preds[a], average='macro', zero_division=0)
            for a in BASE_ATTRIBUTES
        ]
        mean_macro_f1 = float(np.mean(macro_f1s))

        if mean_macro_f1 > best_val_f1 or best_weights is None:
            best_val_f1 = mean_macro_f1
            best_weights = copy.deepcopy(model.state_dict())
            no_improve = 0
            marker = " *"
        else:
            no_improve += 1
            marker = ""

        elapsed = time.time() - t0
        _log(f"  Epoch {epoch+1:2d}/{epochs} [{phase_tag:12s}] "
             f"loss={avg_loss:.4f}  val_f1={mean_macro_f1:.4f}  "
             f"best={best_val_f1:.4f}{marker}  lr={current_lr:.2e}  "
             f"elapsed={elapsed:.0f}s  no_improve={no_improve}")

        history.append({
            'epoch': epoch + 1,
            'loss': avg_loss,
            'val_macro_f1': mean_macro_f1,
            'lr': current_lr,
        })

        if no_improve >= patience:
            _log(f"  [EarlyStopping] Triggered at epoch {epoch+1} (patience={patience})")
            break

    # Save best checkpoint
    ckpt_dir = os.path.join(run_dir, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    ckpt_path = os.path.join(ckpt_dir, "best_model.pth")
    if best_weights is not None:
        torch.save(best_weights, ckpt_path)
        _log(f"[train] Best model checkpoint saved -> {ckpt_path} (val_macro_f1={best_val_f1:.4f})")

    # Load best weights before returning
    if best_weights is not None:
        model.load_state_dict(best_weights)

    return {
        'status': 'SUCCESS',
        'best_val_f1': best_val_f1,
        'ckpt_path': ckpt_path,
        'model': model,
        'history': history,
        'epochs_run': len(history),
    }
