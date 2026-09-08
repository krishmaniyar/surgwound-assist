"""
config.py — Centralized configuration and run management.
Every pipeline run gets a timestamped folder under runs/.
"""
import os
import json
from datetime import datetime

# ── Backbone config ────────────────────────────────────────────────────────────
DINOV2_MODEL   = "facebook/dinov2-large"   # 300M parameters, 1024-dim
CLIP_MODEL     = "ViT-L-14"              # 768-dim (was ViT-B-32 512-dim)
CLIP_PRETRAIN  = "laion2b_s32b_b82k"    # best publicly available ViT-L-14 weights
DINOV2_DIM     = 1024
CLIP_DIM       = 768
EMBEDDING_DIM  = DINOV2_DIM + CLIP_DIM  # 1536 total

# ── Attribute definitions ──────────────────────────────────────────────────────
BASE_ATTRIBUTES = [
    'location', 'healing_status', 'closure_method', 'exudate_type',
    'erythema', 'edema', 'infection_risk', 'urgency_level'
]

CLASS_MAPPINGS = {
    'location':         ['Abdomen', 'Patella', 'Ankle', 'Facial region', 'Manus', 'Cervical region', 'Other', 'Uncertain'],
    'healing_status':   ['Healed', 'Not Healed'],
    'closure_method':   ['Invisible', 'Sutures', 'Staples', 'Adhesives', 'Uncertain'],
    'exudate_type':     ['Non-existent', 'Serous', 'Sanguineous', 'Purulent', 'Seropurulent', 'Uncertain'],
    'erythema':         ['Non-existent', 'Existent', 'Uncertain'],
    'edema':            ['Non-existent', 'Existent', 'Uncertain'],
    'infection_risk':   ['Low', 'Medium', 'High'],
    'urgency_level':    ['Home Care (Green)', 'Clinic Visit (Yellow, <48h)', 'Emergency Care (Red, immediate)'],
}

# Heads where imbalance is extreme (ratio > 20:1) — get LDAM + DRW + SMOTE
IMBALANCED_HEADS = ['infection_risk', 'urgency_level', 'exudate_type', 'closure_method']

# ── Training defaults (overridden by Optuna per head) ──────────────────────────
TRAIN_DEFAULTS = {
    'epochs':       150,
    'lr':           3e-4,
    'weight_decay': 1e-4,
    'dropout':      0.3,
    'hidden_dim':   512,
    'focal_gamma':  2.0,
    'batch_size':   32,
    'label_smooth': 0.05,
    'drw_epoch':    0.6,   # fraction of epochs before switching to LDAM
    'patience':     25,    # early stopping patience
}

OPTUNA_TRIALS  = 30   # per head
CV_FOLDS       = 5

# ── Run management ─────────────────────────────────────────────────────────────
def create_run_dir(base="runs") -> str:
    """Create a timestamped run directory and return its path."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base, f"run_{ts}")
    os.makedirs(os.path.join(run_dir, "plots"), exist_ok=True)
    os.makedirs(os.path.join(run_dir, "checkpoints"), exist_ok=True)
    return run_dir

def save_run_config(run_dir: str, extra: dict = None):
    """Save the config used for this run."""
    cfg = {
        "dinov2_model":   DINOV2_MODEL,
        "clip_model":     CLIP_MODEL,
        "clip_pretrain":  CLIP_PRETRAIN,
        "dinov2_dim":     DINOV2_DIM,
        "clip_dim":       CLIP_DIM,
        "embedding_dim":  EMBEDDING_DIM,
        "train_defaults": TRAIN_DEFAULTS,
        "optuna_trials":  OPTUNA_TRIALS,
        "cv_folds":       CV_FOLDS,
        "attributes":     BASE_ATTRIBUTES,
    }
    if extra:
        cfg.update(extra)
    with open(os.path.join(run_dir, "config.json"), "w") as f:
        json.dump(cfg, f, indent=4)
    print(f"[config] Saved run config -> {run_dir}/config.json")
