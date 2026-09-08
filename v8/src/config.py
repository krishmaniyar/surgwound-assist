"""
v8/src/config.py — Centralized configuration, class mappings, semantic prompts, and run management for v8.
"""
import os
import yaml
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

BASE_ATTRIBUTES = [
    'location', 'healing_status', 'closure_method', 'exudate_type',
    'erythema', 'edema', 'infection_risk', 'urgency_level'
]

CLASS_MAPPINGS = {
    'location': [
        'Abdomen', 'Patella', 'Ankle', 'Facial region',
        'Manus', 'Cervical region', 'Other', 'Uncertain'
    ],
    'healing_status': [
        'Healed', 'Not Healed'
    ],
    'closure_method': [
        'Invisible', 'Sutures', 'Staples', 'Adhesives', 'Uncertain'
    ],
    'exudate_type': [
        'Non-existent', 'Serous', 'Sanguineous', 'Purulent', 'Seropurulent', 'Uncertain'
    ],
    'erythema': [
        'Non-existent', 'Existent', 'Uncertain'
    ],
    'edema': [
        'Non-existent', 'Existent', 'Uncertain'
    ],
    'infection_risk': [
        'Low', 'Medium', 'High'
    ],
    'urgency_level': [
        'Home Care (Green)',
        'Clinic Visit (Yellow, <48h)',
        'Emergency Care (Red, immediate)'
    ],
}

# Rich clinical text prompts for BiomedCLIP PubMedBERT text embedding generation
CLINICAL_PROMPTS = {
    'location': {
        'Abdomen': 'surgical wound located on the abdomen or belly',
        'Patella': 'surgical wound located on the knee or patella region',
        'Ankle': 'surgical wound located on the ankle or lower foot',
        'Facial region': 'surgical incision or wound on the face or head',
        'Manus': 'surgical wound located on the hand or wrist',
        'Cervical region': 'surgical wound located on the neck or cervical region',
        'Other': 'surgical wound located on other anatomical areas',
        'Uncertain': 'surgical wound location uncertain or undetermined',
    },
    'healing_status': {
        'Healed': 'completely closed and healed surgical wound incision with no complications',
        'Not Healed': 'unhealed or open surgical wound incision showing active tissue repair',
    },
    'closure_method': {
        'Invisible': 'surgical incision closed subcuticularly with no visible surface sutures or staples',
        'Sutures': 'surgical wound closed with visible surgical stitches or sutures',
        'Staples': 'surgical wound closed with metal surgical staples',
        'Adhesives': 'surgical wound closed with skin glue or tissue adhesive tape strips',
        'Uncertain': 'surgical wound closure method uncertain',
    },
    'exudate_type': {
        'Non-existent': 'dry surgical wound with no fluid drainage or exudate',
        'Serous': 'surgical wound with clear thin watery serous fluid drainage',
        'Sanguineous': 'surgical wound with fresh red blood drainage or sanguineous fluid',
        'Purulent': 'surgical wound with thick yellow white opaque purulent exudate or pus indicating infection',
        'Seropurulent': 'surgical wound with thin cloudy pale yellow seropurulent fluid discharge',
        'Uncertain': 'wound fluid exudate type uncertain',
    },
    'erythema': {
        'Non-existent': 'surgical wound with normal skin tone and no erythema or redness',
        'Existent': 'surgical wound with prominent erythema, redness, or inflammation around the incision',
        'Uncertain': 'wound erythema uncertain',
    },
    'edema': {
        'Non-existent': 'surgical wound with no edema, swelling, or puffiness around incision margins',
        'Existent': 'surgical wound with noticeable swelling, edema, or raised puffy tissue margins',
        'Uncertain': 'wound edema uncertain',
    },
    'infection_risk': {
        'Low': 'clean surgical wound with low risk of infection and no signs of bacterial colonization',
        'Medium': 'surgical wound with moderate infection risk, mild erythema or serous discharge',
        'High': 'surgical wound with high risk of infection, marked erythema, purulent pus, or tissue breakdown',
    },
    'urgency_level': {
        'Home Care (Green)': 'stable surgical wound suitable for routine outpatient home care',
        'Clinic Visit (Yellow, <48h)': 'surgical wound requiring outpatient clinical evaluation within 24 to 48 hours',
        'Emergency Care (Red, immediate)': 'critical surgical wound requiring immediate emergency medical care and intervention',
    },
}

BIOMEDCLIP_MODEL_ID = 'hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224'


def load_config(config_path: str) -> Dict[str, Any]:
    """Load a YAML configuration file."""
    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    return cfg


def create_v8_run_dir(base_dir: str = "v8/runs", prefix: str = "exp") -> str:
    """Create timestamped run directory."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(base_dir, f"{prefix}_{ts}")
    os.makedirs(os.path.join(run_dir, "checkpoints"), exist_ok=True)
    os.makedirs(os.path.join(run_dir, "plots"), exist_ok=True)
    return run_dir
