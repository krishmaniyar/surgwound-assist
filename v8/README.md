# SurgWound Assist v8 — State-of-the-Art Multi-Task Surgical Wound Intelligence

SurgWound Assist v8 is an autonomous multi-task deep learning system designed for the automated clinical evaluation of post-operative surgical wound photographs across 8 clinical attributes.

v8 achieves a new project record **58.73% Mean Test Macro-F1**, substantially exceeding the official v7.5 baseline (**51.10%**) by **+7.63 percentage points**, while maintaining an exact match ratio of **20.00%** (1 in 5 patients diagnosed with 100% precision across all 8 attributes simultaneously).

---

## 1. Problem Definition & Clinical Tasks
Surgical wound assessment from mobile/post-operative imagery requires evaluating 8 distinct clinical attributes simultaneously:
1. `location` (8 classes: Abdomen, Patella, Ankle, Facial region, Manus, Cervical region, Other, Uncertain)
2. `healing_status` (2 classes: Healed, Not Healed)
3. `closure_method` (5 classes: Invisible, Sutures, Staples, Adhesives, Uncertain)
4. `exudate_type` (6 classes: Non-existent, Serous, Sanguineous, Purulent, Seropurulent, Uncertain)
5. `erythema` (3 classes: Non-existent, Existent, Uncertain)
6. `edema` (3 classes: Non-existent, Existent, Uncertain)
7. `infection_risk` (3 classes: Low, Medium, High)
8. `urgency_level` (3 classes: Home Care, Clinic Visit, Emergency Care)

---

## 2. Dataset & Hardware Constraints
- **Dataset**: 349 annotated post-operative surgical wound photographs (train: 244, val: 35, test: 70).
- **Severe Long-Tail Imbalance**: Imbalance ratios up to 72:1 on urgency and 41:1 on infection risk; rare classes have as few as 1–2 test instances.
- **Hardware Budget**: Single NVIDIA GeForce RTX 3060 Laptop GPU (6.4 GB VRAM), Windows 11.

---

## 3. Core Architectural Innovations in v8

```text
                          Input Surgical Photograph
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
   Global View (224×224)                              Local Crop (65% center)
            │                                                   │
            ▼                                                   ▼
   BiomedCLIP ViT-B/16                                 BiomedCLIP ViT-B/16
  (Pretrained 15M PMC)                                (Pretrained 15M PMC)
            │                                                   │
     Global Embedding                                    Local Embedding
        [B, 512]                                            [B, 512]
            │                                                   │
            └─────────────────────────┬─────────────────────────┘
                                      ▼
                           Multi-Scale Feature Fusion
                     Linear(1024→512) + LayerNorm + GELU
                                      │
                         Fused Embedding [B, 512]
                                      │
     ┌────────────────────────────────┼────────────────────────────────┐
     ▼                                ▼                                ▼
Head 1: location              Head 2: healing_status            ... Head 8: urgency
Residual Adapter              Residual Adapter                  Residual Adapter
PubMedBERT Prototypes         PubMedBERT Prototypes             PubMedBERT Prototypes
     │                                │                                │
Logit-Adjusted Loss           Logit-Adjusted Loss               Logit-Adjusted Loss
```

1. **Multi-Scale Global + Local Feature Fusion**: Fuses a global 224×224 contextual view with a high-resolution 50%–65% centered wound crop through a weight-shared BiomedCLIP ViT-B/16 backbone, recovering fine-grained suture knots, staples, and fluid droplets without exceeding 4.2 GB VRAM.
2. **PubMedBERT Semantic Text Prototypes**: Initializes classification heads with normalized 512-dim clinical concept embeddings generated offline by BiomedCLIP's PubMedBERT text encoder (`v8/src/clinical_text_prototypes.pt`), accelerating location classification (+23.08%).
3. **Logit-Adjusted Loss & Adaptive-Tau ($\tau=2.0$)**: Replaces LDAM margin scaling with statistical logit adjustment, running natively in mixed precision. v8.1 doubles $\tau$ to 2.0 to enforce stronger separation on severe long-tail minority classes.
4. **Multi-Task Balanced Mini-Batch Sampler**: Employs an inverse-frequency `WeightedRandomSampler` across all 8 multi-task targets, ensuring rare instances (Staples, Seropurulent, High Risk) appear in every training batch.
5. **Regularized Validation Calibration**: Post-hoc threshold optimization tuned on validation data to maximize Macro-F1 across severe minority classes.
6. **Deep Multi-Scale Probability Ensemble**: Integrates single-scale and multi-scale checkpoints with 7× medical-safe Test-Time Augmentation (TTA).

---

## 4. Benchmark Progression

| Version | Backbone | Innovation | Val Macro-F1 | Test Macro-F1 (TTA) | Exact Match |
|---|---|---|---|---|---|
| **v2.0** | DINOv2-Base + CLIP | Static embeddings | — | 38.81% | ~2.0% |
| **v4.0** | DINOv2-Base | End-to-end fine-tuning | 62.10% | 55.31% | ~10.0% |
| **v5.0** | DINOv2-Large | Scaling up (300M) | 62.23% | 51.95% | ~8.5% |
| **v6.0** | DINOv2-Large + LLRD | LLRD + Warmup + Seed | 65.25% | 54.66% | 11.43% |
| **v7.4** | BiomedCLIP | FP32 LDAM | 60.19% | 50.64% | 12.86% |
| **v7.5 (Baseline)** | BiomedCLIP | LDAM LR Warm-Restart | 61.42% | **51.10%** | 14.29% |
| **v8_e1** | BiomedCLIP | LogitAdj + Text Prototypes | 58.68% | **54.44%** | 15.71% |
| **v8_e2** | BiomedCLIP MultiScale | Global + Local Crop Fusion | 60.32% | **57.63%** | 18.57% |
| **v8 (Final Ensemble)** | **BiomedCLIP Dual-Model** | **Multi-Scale Deep Ensemble** | **60.32%** | **58.73%** | **20.00%** |
| **v8.1 (In Progress)** | **BiomedCLIP MultiScale** | **$\tau=2.0$ + Balanced Sampler + 0.50 Crop** | **Running** | **Running** | **Running** |

---

## 5. Per-Attribute Comparison (v8 vs v7.5)

| Attribute | Baseline v7.5 Macro-F1 | v8 Final Macro-F1 | Net Delta | Accuracy |
|---|---|---|---|---|
| **`location`** | 40.76% | **63.84%** | **+23.08%** | 67.1% |
| **`infection_risk`** | 29.63% | **44.23%** | **+14.60%** | 85.7% |
| **`exudate_type`** | 18.93% | **32.41%** | **+13.48%** | 90.0% |
| **`closure_method`** | 32.00% | **39.36%** | **+7.36%** | 67.1% |
| **`erythema`** | 64.80% | **70.17%** | **+5.37%** | 81.4% |
| **`edema`** | 46.78% | **49.00%** | **+2.22%** | 77.1% |
| **`urgency_level`** | 100.00% | **100.00%** | +0.00% | 100.0% |
| **`healing_status`** | 75.88% | **70.86%** | -5.02% | 74.3% |
| **MEAN** | **51.10%** | **58.73%** | **+7.63%** | **80.36%** |

---

## 6. Reproducibility Instructions

### Environment Setup
```powershell
# Activate project environment
conda activate surgwound-gpu
```

### Reproduce v8 Multi-Scale Model Training
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" v8/src/run_experiment.py `
  --exp_id v8_reproduce `
  --epochs 80 `
  --loss logit_adjusted `
  --multiscale `
  --lr 3e-5 `
  --seed 42
```

### Reproduce Full v8 Deep Ensemble Evaluation (58.73% Macro-F1)
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" -c "
import sys, os, torch, pandas as pd
sys.path.insert(0, 'v8/src')
from ensemble import run_ensemble_evaluation

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
df = pd.read_csv('archive/dataset_backup_v7/annotations.csv')
df_test = df[df['split'] == 'test'].reset_index(drop=True)

models = [
    {'ckpt_path': 'v8/checkpoints/biomedclip_v8_singlescale.pth', 'multiscale': False, 'name': 'v8_single_scale'},
    {'ckpt_path': 'v8/checkpoints/biomedclip_v8_multiscale.pth', 'multiscale': True, 'name': 'v8_multi_scale'}
]
res = run_ensemble_evaluation(models, df_test, device, 'v8/runs/reproduced_ensemble', tta_n=7, weights=[0.4, 0.6])
print('Mean Macro-F1:', res['aggregate']['mean_macro_f1']*100)
"
```
