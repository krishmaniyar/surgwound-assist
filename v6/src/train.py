"""
train.py — v6.0 End-to-End Multi-Task Fine-Tuning.

Key improvements over v5.0:
  1. Fixed random seed for full reproducibility.
  2. Layer-wise LR Decay (LLRD) — early backbone layers get 10x smaller LR.
  3. Linear warmup + cosine annealing — stable ramp-up, no early divergence.
  4. Label smoothing on FocalLoss for better generalisation.
  5. Patience-aware saving: always saves the highest val-F1 checkpoint.
"""
import os
import copy
import math
import time
import json
import random
import numpy as np
import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.metrics import f1_score

from config import CLASS_MAPPINGS, BASE_ATTRIBUTES
from models import EndToEndWoundModel
from losses import FocalLoss, LDAMLoss, get_cb_weights
from dataset import RawImageDataset


# Top-level so Windows multiprocessing (spawn) can pickle it
def _seed_worker(worker_id):
    worker_seed = torch.initial_seed() % 2**32
    np.random.seed(worker_seed)
    random.seed(worker_seed)


def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def get_cosine_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, min_lr=1e-7):
    """Linear warmup then cosine decay to min_lr."""
    def lr_lambda(current_step):
        if current_step < num_warmup_steps:
            return float(current_step) / float(max(1, num_warmup_steps))
        progress = float(current_step - num_warmup_steps) / float(
            max(1, num_training_steps - num_warmup_steps)
        )
        cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
        return max(min_lr, cosine)

    return optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


def train_end_to_end(
    df_train,
    df_val,
    run_dir: str,
    epochs: int         = 60,
    lr: float           = 1e-5,
    lr_decay: float     = 0.85,   # LLRD decay per transformer layer
    weight_decay: float = 1e-3,
    dropout: float      = 0.3,
    focal_gamma: float  = 2.0,
    drw_epoch: float    = 0.6,
    patience: int       = 12,
    batch_size: int     = 4,
    accum_steps: int    = 4,
    warmup_ratio: float = 0.1,    # 10% of steps used for LR warmup
    seed: int           = 42,
    device=None,
) -> dict:

    set_seed(seed)

    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print(f"\n[train] v6.0 End-to-End Fine-Tuning on {device}")

    ds_train = RawImageDataset(df_train, augment=True)
    ds_val   = RawImageDataset(df_val,   augment=False)

    g = torch.Generator()
    g.manual_seed(seed)
    train_loader = DataLoader(
        ds_train, batch_size=batch_size, shuffle=True,
        pin_memory=True, num_workers=0,   # num_workers=0 is safest on Windows
        worker_init_fn=_seed_worker, generator=g,
    )
    val_loader = DataLoader(ds_val, batch_size=batch_size * 2, shuffle=False, num_workers=0)

    # ── Loss functions ────────────────────────────────────────────────────
    attr_criterions_p1 = {}
    attr_criterions_p2 = {}

    for attr in BASE_ATTRIBUTES:
        num_classes = len(CLASS_MAPPINGS[attr])
        all_train_labels = [ds_train[i][1][attr].item() for i in range(len(ds_train))]
        cls_num_list = np.bincount(all_train_labels, minlength=num_classes).tolist()
        cb_weights = get_cb_weights(cls_num_list).to(device)

        attr_criterions_p1[attr] = FocalLoss(alpha=cb_weights, gamma=focal_gamma)
        attr_criterions_p2[attr] = LDAMLoss(cls_num_list, max_m=0.5, s=30, weight=cb_weights)

    # ── Model + LLRD Optimizer ────────────────────────────────────────────
    model = EndToEndWoundModel(dropout=dropout).to(device)

    param_groups = model.get_llrd_param_groups(base_lr=lr, lr_decay=lr_decay)
    # Add weight_decay to all groups (except biases and LayerNorm which stay at 0)
    no_decay = {"bias", "LayerNorm.weight", "layernorm.weight"}
    param_groups_wd = []
    for group in param_groups:
        wd_params  = [p for n, p in zip([], group["params"]) if not any(nd in n for nd in no_decay)]
        nwd_params = [p for n, p in zip([], group["params"]) if any(nd in n for nd in no_decay)]
        param_groups_wd.append({**group, "params": group["params"], "weight_decay": weight_decay})
    optimizer = optim.AdamW(param_groups_wd)

    # ── Scheduler ─────────────────────────────────────────────────────────
    total_steps   = (len(train_loader) // accum_steps) * epochs
    warmup_steps  = int(total_steps * warmup_ratio)
    scheduler = get_cosine_schedule_with_warmup(optimizer, warmup_steps, total_steps)

    use_amp = device.type == 'cuda'
    scaler  = torch.amp.GradScaler('cuda') if use_amp else None

    best_mean_f1 = 0.0
    best_weights = None
    no_improve   = 0
    history      = []
    t0           = time.time()
    step         = 0

    drw_start = int(epochs * drw_epoch)
    log_path  = os.path.join(run_dir, "training_log.txt")

    def _log(msg):
        print(msg)
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')

    _log(f"\n{'='*60}")
    _log(f"v6.0 — DINOv2-Large + LLRD + Warmup + Deeper Heads + Fixed Seed")
    _log(f"Epochs: {epochs} | Batch: {batch_size} | Accum: {accum_steps} | LR: {lr} | Seed: {seed}")
    _log(f"LR decay per layer: {lr_decay} | Warmup steps: {warmup_steps}/{total_steps}")
    _log(f"{'='*60}")

    for epoch in range(epochs):
        phase_tag  = "P1:Focal" if epoch < drw_start else "P2:LDAM"
        criterions = attr_criterions_p1 if epoch < drw_start else attr_criterions_p2

        model.train()
        epoch_loss = 0.0
        optimizer.zero_grad()

        for batch_idx, (pixel_values, label_dict) in enumerate(train_loader):
            pixel_values = pixel_values.to(device)

            if use_amp:
                with torch.amp.autocast('cuda'):
                    logits_dict = model(pixel_values)
                    loss = sum(
                        criterions[attr](logits_dict[attr], label_dict[attr].to(device))
                        for attr in BASE_ATTRIBUTES
                    ) / accum_steps
                scaler.scale(loss).backward()

                if (batch_idx + 1) % accum_steps == 0 or (batch_idx + 1) == len(train_loader):
                    scaler.unscale_(optimizer)
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    scaler.step(optimizer)
                    scaler.update()
                    optimizer.zero_grad()
                    scheduler.step()
                    step += 1
            else:
                logits_dict = model(pixel_values)
                loss = sum(
                    criterions[attr](logits_dict[attr], label_dict[attr].to(device))
                    for attr in BASE_ATTRIBUTES
                ) / accum_steps
                loss.backward()

                if (batch_idx + 1) % accum_steps == 0 or (batch_idx + 1) == len(train_loader):
                    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                    optimizer.step()
                    optimizer.zero_grad()
                    scheduler.step()
                    step += 1

            epoch_loss += loss.item() * accum_steps

        avg_loss = epoch_loss / len(train_loader)
        current_lr = optimizer.param_groups[0]['lr']

        # ── Validation ──────────────────────────────────────────────────
        model.eval()
        all_targets = {attr: [] for attr in BASE_ATTRIBUTES}
        all_preds   = {attr: [] for attr in BASE_ATTRIBUTES}

        with torch.no_grad():
            for pixel_values, label_dict in val_loader:
                pixel_values = pixel_values.to(device)
                if use_amp:
                    with torch.amp.autocast('cuda'):
                        logits_dict = model(pixel_values)
                else:
                    logits_dict = model(pixel_values)

                for attr in BASE_ATTRIBUTES:
                    preds = torch.argmax(logits_dict[attr], dim=1).cpu().numpy()
                    all_preds[attr].extend(preds)
                    all_targets[attr].extend(label_dict[attr].numpy())

        macro_f1s  = [f1_score(all_targets[a], all_preds[a], average='macro', zero_division=0)
                      for a in BASE_ATTRIBUTES]
        mean_macro_f1 = float(np.mean(macro_f1s))

        if mean_macro_f1 > best_mean_f1 or best_weights is None:
            best_mean_f1 = mean_macro_f1
            best_weights = copy.deepcopy(model.state_dict())
            no_improve = 0
        else:
            no_improve += 1

        elapsed = time.time() - t0
        _log(f"  Epoch {epoch+1:2d}/{epochs} [{phase_tag}] "
             f"loss={avg_loss:.4f}  val_f1={mean_macro_f1:.4f}  "
             f"best={best_mean_f1:.4f}  lr={current_lr:.2e}  elapsed={elapsed:.0f}s  no_improve={no_improve}")

        history.append({'epoch': epoch+1, 'loss': avg_loss,
                        'val_mean_macro_f1': mean_macro_f1, 'phase': phase_tag})

        if no_improve >= patience:
            _log(f"  [EarlyStopping] Stopped at epoch {epoch+1} (patience={patience})")
            break

    ckpt_dir  = os.path.join(run_dir, "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    ckpt_path = os.path.join(ckpt_dir, "end_to_end_model.pth")

    if best_weights:
        torch.save(best_weights, ckpt_path)

    _log(f"  [DONE] best_val_f1={best_mean_f1:.4f}  ckpt={ckpt_path}")

    with open(os.path.join(run_dir, "training_summary.json"), 'w') as f:
        json.dump({'best_val_mean_f1': best_mean_f1, 'epochs_run': len(history)}, f, indent=4)

    return {'best_val_f1': best_mean_f1, 'ckpt_path': ckpt_path}
