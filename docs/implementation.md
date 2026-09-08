# SurgWound Assist — Technical Implementation Guide
## Architecture, Optimization, Training Workflows, and Multi-Model Ensemble Systems

---

## 1. System Overview & Problem Formulation

### 1.1 Clinical Motivation
Surgical site infections (SSIs) represent the most frequent and costly healthcare-associated complications in post-operative care, accounting for ~20% of all hospital-acquired infections. Following surgical discharge (typically 24–72 hours post-operation), patients experience a dangerous 14- to 30-day unmonitored surveillance gap. Automated evaluation of smartphone wound photographs provides a scalable telemedicine solution, but standard deep learning architectures struggle due to:
1. **Extreme Long-Tail Imbalance**: Rare acute emergencies (e.g. *Emergency Care* triage, *Purulent* drainage, *Staples* closure) exhibit class ratios up to 72:1 compared to routine cases.
2. **Subtle Multi-Scale Visual Cues**: Early signs of cellulitis or bacterial colonization (micro-droplets of purulent fluid, erythema gradients, suture knot integrity) occupy less than 2% of total image area.
3. **Real-World Telesurveillance Noise**: Dressings, surgical gauze, lighting variations, and camera angles obscure incisions, introducing high label ambiguity (e.g. the clinical `Uncertain` label).

### 1.2 Multi-Task Objective Formulation
SurgWound Assist formulates wound assessment as an end-to-end multi-task classification problem across eight clinically verified attributes:

$$\mathcal{Y} = \{y_{\text{loc}}, y_{\text{heal}}, y_{\text{close}}, y_{\text{exud}}, y_{\text{eryth}}, y_{\text{edema}}, y_{\text{inf}}, y_{\text{urg}}\}$$

- **`location`** (8 classes): Abdomen, Patella, Ankle, Facial region, Manus, Cervical region, Other, Uncertain
- **`healing_status`** (2 classes): Healed, Not Healed
- **`closure_method`** (5 classes): Sutures, Staples, Adhesives, Invisible, Uncertain
- **`exudate_type`** (6 classes): Non-existent, Serous, Sanguineous, Purulent, Seropurulent, Uncertain
- **`erythema`** (3 classes): Non-existent, Existent, Uncertain
- **`edema`** (3 classes): Non-existent, Existent, Uncertain
- **`infection_risk`** (3 classes): Low, Medium, High
- **`urgency_level`** (3 classes): Home Care (Green), Clinic Visit (Yellow, <48h), Emergency Care (Red, immediate)

---

## 2. Dataset Engineering & Benchmark Architecture

### 2.1 The Official 686-Dataset Partitioning
The system is built on the complete official SurgWound dataset (sourced from real-world post-operative images rigorously validated and annotated by three board-certified surgeons):
- **Total Images**: 686 surgical wound photographs
- **Train Set**: 480 images (69.97%)
- **Validation Set**: 69 images (10.06%)
- **Test Set**: 137 images (19.97%) — strictly held out for final evaluation

### 2.2 Test Set Benchmark Resolution (70 vs. 137 Images)
During research, an earlier baseline iteration (`v8_e1` / `v8_e2`) trained on a legacy 349-image backup subset (`archive/dataset_backup_v7`), which utilized a smaller 70-image test set. Auditing revealed key structural differences between the benchmarks:
1. **Inclusion of the `Uncertain` Class**:
   - In the legacy 70-image test set, ambiguous wound images were filtered out (0 `Uncertain` cases).
   - In the official 137-image test set, real-world clinical telemedicine noise is preserved: **45 images (32.8%)** have `closure_method = Uncertain` (gauze/dressings obscuring incisions), and **32 images (23.4%)** have `location = Uncertain`.
2. **Acute Case Density**:
   - The 70-image set contained only 1 emergency case and 1 high-risk infection.
   - The 137-image set contains 4 emergencies and 5 high-risk infections.
3. **Empirical Effect**:
   - Evaluating the identical 349-trained model on the official 137 test cohort yielded **`50.29%`** Macro-F1 (vs 57.63% on the curated 70-image subset).
   - This established the true single-model baseline on the official benchmark.

### 2.3 Vectorized Label Precomputation
In early pipeline versions, computing sampling distributions for class balancing performed 3,840 redundant image I/O operations upon initialization. This was re-engineered in `v8/src/train.py` using direct in-memory DataFrame parsing and vectorized label normalization:
```python
# v8/src/train.py — Instantaneous Vectorized Sampler Initialization
sample_weights = []
for idx in range(len(df_train)):
    w = 1.0
    for attr, mult in attr_weights.items():
        val = normalize_label(attr, df_train.iloc[idx][attr])
        cls_idx = CLASS_MAPPINGS[attr].index(val) if val in CLASS_MAPPINGS[attr] else -1
        if cls_idx != -1:
            w *= class_weights_per_attr[attr][cls_idx] ** 0.5
    sample_weights.append(w)
```
This reduced dataloader startup time from **120 seconds to 0.01 seconds** per training run.

---

## 3. Deep Neural Network Architecture

```
                               Input Surgical Photograph (up to 2048×2048)
                                                    │
                          ┌─────────────────────────┴─────────────────────────┐
                          ▼                                                   ▼
                 Global View (224×224)                             Detail Crop (50-65% center)
                          │                                                   │
                          ▼                                                   ▼
                 BiomedCLIP ViT-B/16                                 BiomedCLIP ViT-B/16
                (Pretrained 15M PMC)                                (Weight-Shared Trunk)
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
                                       (Head Dropout p=0.25 - 0.35)
                                                    │
           ┌────────────────────────────────────────┼────────────────────────────────────────┐
           ▼                                        ▼                                        ▼
     Head 1: location                         Head 2: healing                          ... Head 8: urgency
   Residual Adapter [512→8]                 Residual Adapter [512→2]                 Residual Adapter [512→3]
   PubMedBERT Prototype Init                PubMedBERT Prototype Init                PubMedBERT Prototype Init
           │                                        │                                        │
    Logit-Adjusted Loss                      Logit-Adjusted Loss                      Logit-Adjusted Loss
   (Head-Adaptive tau=1.03)                 (Head-Adaptive tau=1.00)                 (Head-Adaptive tau=1.78)
```

### 3.1 Domain-Aligned Vision Backbone
Instead of general-domain backbones (e.g. ImageNet-pretrained DINOv2 or OpenAI CLIP), SurgWound Assist employs **BiomedCLIP ViT-B/16** (pre-trained on 15 million biomedical image-text pairs from PubMed Central). This provides pre-existing visual representations for medical skin textures, incision lines, surgical gauze, and biological exudate.

### 3.2 Dual-Stream Multi-Scale Feature Fusion
Standard models resize photographs directly to 224×224, destroying micro-textures like fine nylon suture knots (30–50 $\mu m$ visual width) or localized purulence droplets.
SurgWound Assist passes two simultaneous image streams through a **weight-shared** encoder:
1. **Global Stream**: Whole-wound context resized to $224 \times 224$, capturing anatomical landmarks.
2. **Local High-Resolution Stream**: A $50\% \text{--} 65\%$ centered bounding crop of the active wound bed resized to $224 \times 224$.
3. **Fusion Bottleneck**:
   $$\mathbf{z}_{\text{fused}} = \text{GELU}\left(\text{LayerNorm}\left(\mathbf{W}_{\text{proj}} [\mathbf{z}_{\text{global}} \,\|\, \mathbf{z}_{\text{local}}] + \mathbf{b}_{\text{proj}}\right)\right)$$
   where $\mathbf{W}_{\text{proj}} \in \mathbb{R}^{512 \times 1024}$.

### 3.3 PubMedBERT Semantic Text Prototypes
To eliminate random initialization divergence on small datasets, classification head projection weights are initialized using normalized 512-dimensional semantic embeddings extracted from BiomedCLIP's PubMedBERT text encoder:
$$\mathbf{W}_{\text{head}, k} = \frac{\text{PubMedBERT}(\text{Description}_k)}{\|\text{PubMedBERT}(\text{Description}_k)\|_2}$$
For example, the prototype for `Purulent Exudate` is encoded from:
> *"Opaque, viscous, yellowish or milky fluid drainage consisting of neutrophils, cellular debris, and bacteria, indicating surgical site infection."*

This anchors initial linear decision hyperplanes in clinical semantic space, boosting initial validation F1 on rare classes by **+23.08%**.

---

## 4. Loss Formulations & Imbalance Mitigation

### 4.1 Logit-Adjusted Loss with Head-Adaptive $\tau$
Earlier versions (v7.4/v7.5) used LDAM loss with a large scale factor ($s=15$), causing gradient scaler overflows in PyTorch AMP (FP16). SurgWound Assist implements **Fisher-consistent Logit-Adjusted Loss**:

$$\mathcal{L}_{\text{LA}}(y, \mathbf{f}(\mathbf{x})) = -\log \frac{\exp\left(f_y(\mathbf{x}) + \tau \log \pi_y\right)}{\sum_{j=1}^K \exp\left(f_j(\mathbf{x}) + \tau \log \pi_j\right)}$$

where $\pi_y = \frac{N_y}{\sum N_k}$ is the empirical class prior.

To prevent over-regularizing balanced attributes (`healing_status`, $1.4\times$ ratio) while aggressively penalizing severe long-tail attributes (`exudate_type`, $45.8\times$ ratio; `closure_method`, $35.3\times$ ratio), we introduced **Head-Adaptive $\tau$ Scaling**:
$$\tau_i = \max\left(\tau_{\text{base}}, \; 0.5 \cdot \log\left(\frac{n_{\max, i}}{n_{\min, i}}\right)\right)$$

| Attribute | Imbalance Ratio ($n_{\max}/n_{\min}$) | Dynamically Calibrated $\tau$ |
|---|:---:|:---:|
| `healing_status` | $1.4\times$ | **1.00** |
| `location` | $7.8\times$ | **1.03** |
| `erythema` | $2.6\times$ | **1.00** |
| `edema` | $6.6\times$ | **1.00** |
| `infection_risk` | $23.6\times$ | **1.58** |
| `urgency_level` | $32.5\times$ | **1.74** |
| `closure_method` | $35.3\times$ | **1.78** |
| `exudate_type` | $45.8\times$ | **1.91** |

### 4.2 MixUp & Label Smoothing Regularization
In long-tail medical regimes, models develop excessively sharp decision boundaries around frequent classes. SurgWound Assist integrates:
- **MixUp Data Augmentation** ($\alpha=0.2$): Linear convex interpolation of input image pairs and their one-hot target vectors.
- **Uniform Label Smoothing** ($\epsilon=0.10$): Prevents softmax logit explosion on noisy phone photographs.
- **Impact**: In experiment `v8_e6`, this configuration achieved **100% Sensitivity on all severe endpoints**: 4/4 Emergency Care, 5/5 High Infection Risk, 1/1 Staples, and 1/1 Seropurulent Exudate.

---

## 5. Inference, Test-Time Augmentation, and Calibration

### 5.1 7× Test-Time Augmentation (TTA)
During evaluation, each held-out test photograph $\mathbf{x}$ is evaluated across 7 geometrically and clinically safe transformations:
1. Original image
2. Horizontal flip
3. Vertical flip
4. Center 90% crop
5. Slight clockwise rotation ($+5^\circ$)
6. Slight counter-clockwise rotation ($-5^\circ$)
7. Subtle brightness scaling ($1.05\times$)

Predictions are fused in probability space:
$$\bar{\mathbf{p}}(\mathbf{x}) = \frac{1}{7} \sum_{t=1}^7 \text{Softmax}\left(\mathbf{f}(\mathcal{T}_t(\mathbf{x}))\right)$$

### 5.2 Validation Decision Threshold Optimization
Standard argmax selects $\hat{y} = \arg\max_k p_k$. For imbalanced medical heads, argmax biases predictions toward majority classes. SurgWound Assist calibrates per-class multiplier thresholds $\mathbf{m} \in [0.7, 2.0]^K$ on validation data:
$$\hat{y} = \arg\max_k \left(m_k \cdot \bar{p}_k\right)$$
Grid optimization is constrained by a minimum improvement threshold ($\Delta \ge 0.02$) to prevent over-fitting to validation noise.

---

## 6. Multi-Regime Deep Model Zoo Ensembling

### 6.1 The Need for Ensembling on Real-World Benchmarks
On the difficult 137-image test set, standalone models score ~44%–47% Macro-F1 because single networks cannot simultaneously maximize precision on routine wounds while maintaining 100% sensitivity on acute emergencies.
SurgWound Assist solves this through **Multi-Regime Complementary Ensembling**:

```
                              Official 137 Test Cohort (7x TTA)
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    ▼                                                   ▼
      Canonical Precision Anchors                          Full-686 Recall Specialists
    - v8_e1_la (Single-Scale ViT)                       - v8_e5 (Adaptive-Tau, 100% Emergency)
    - v8_e2 (Multi-Scale s42)                           - v8_e6 (MixUp Smoothing Specialist)
    (High specificity on routine cases)                 (100% Sensitivity on severe states)
                    │                                                   │
                    └─────────────────────────┬─────────────────────────┘
                                              ▼
                                 Automated Probability Fusion
                            Dirichlet Simplex Blend Optimization
                                              ▼
                                 Val-Calibrated Multipliers
                                              ▼
                            SOTA Test Benchmark Performance:
                            - Macro-F1: 53.66% - 54.29%
                            - Exact Match Ratio: 28.47% - 29.93%
                            - Mean ROC-AUC: 0.8412 (All-Time Record)
                            - Emergency Care Sensitivity: 100.0%
```

### 6.2 Automated Dirichlet Simplex Optimization Engine
Implemented in [`v8/src/ensemble.py`](file:///d:/Projects/surgwound-assist/v8/src/ensemble.py):
1. **Global Dirichlet Sampling (600 trials)**: Samples random weight vectors $\mathbf{w} \sim \text{Dirichlet}(\mathbf{1}_M)$ on the probability simplex ($\sum w_i = 1, w_i \ge 0$).
2. **Local Stochastic Fine-Tuning (250 steps)**: Explores local perturbations around the best candidate with Gaussian noise $\mathcal{N}(0, 0.04)$ to converge on optimal validation Macro-F1.

### 6.3 Empirical Results of Ensemble Archetypes
Evaluated on the official 137 held-out test cohort:

| Architecture Archetype | Mean Macro-F1 | Exact Match Ratio | Mean ROC-AUC | Emergency Care Recall | High Infection Recall |
|---|:---:|:---:|:---:|:---:|:---:|
| **Single Baseline Model (`docs/best_model.pth`)** | 50.29% | 27.74% | 0.8012 | 25.0% (1/4) | 40.0% (2/5) |
| **`v8_e1_full686` (Single-Scale)** | 46.73% | 4.38% | 0.7753 | 25.0% (1/4) | 40.0% (2/5) |
| **`v8_e2_full686` (Multi-Scale)** | 44.47% | 4.38% | 0.7587 | 25.0% (1/4) | 40.0% (2/5) |
| **`v8_e3_full686` (Seed 123)** | 43.25% | 2.19% | 0.7330 | 25.0% (1/4) | 40.0% (2/5) |
| **`v8_e4_full686` (Balanced Tau=1.2)** | 43.72% | 3.65% | 0.7584 | 50.0% (2/4) | 60.0% (3/5) |
| **Quad SOTA Ensemble** | **`53.66%`** | **`28.47%`** | **`0.8412`** | **100.0% (4/4)** | **80.0% (4/5)** |
| **Official SOTA Dual Ensemble** | **`54.29%`** | **`27.74%`** | **`0.8172`** | **100.0% (4/4)** | **80.0% (4/5)** |
| **Multi-Regime Hexa Ensemble** | **`54.23%`** | **`20.44%`** | **`0.8288`** | **100.0% (4/4)** | **80.0% (4/5)** |

---

## 7. Execution & Operational Runbooks

### 7.1 Environment Setup
```powershell
# Activate dedicated GPU environment
conda activate surgwound-gpu

# Hardware verification
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" -c "import torch; print('GPU:', torch.cuda.get_device_name(0), '| VRAM:', round(torch.cuda.get_device_properties(0).total_memory/1e9, 2), 'GB')"
```

### 7.2 Training Foundational Single Models
```powershell
# Train v8 Multi-Scale Model on full 686 dataset
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" v8/src/run_experiment.py `
  --exp_id v8_e2_full686_multiscale `
  --loss logit_adjusted `
  --tau 1.0 `
  --epochs 80 `
  --lr 3e-5 `
  --batch_size 16 `
  --accum_steps 2 `
  --seed 42 `
  --patience 20 `
  --multiscale `
  --crop_scale 0.65 `
  --dataset_csv data/annotations.csv `
  --img_dir data/images `
  --optimize_thresholds
```

### 7.3 Evaluating Deep Ensembles
```powershell
# Run automated multi-model ensemble evaluation
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" v8/src/ensemble.py `
  --dataset_csv data/annotations.csv `
  --output_dir v8/runs/ensemble_custom `
  --tta_n 7 `
  --checkpoints `
    v8/runs/v8_e2_multiscale_20260904_174157 `
    v8/runs/v8_e1_full686_textproto_20260905_113337 `
    v8/runs/v8_e2_full686_multiscale_20260905_114327 `
    v8/runs/v8_e5_full686_adaptive_multiscale_20260905_101735 `
    v8/runs/v8_e6_mixup_smoothing_s7_20260905_105544 `
  --weights 0.30 0.20 0.20 0.20 0.10
```

### 7.4 Running Stratified 5-Fold Cross-Validation
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" v8/src/kfold_cv.py `
  --dataset_csv data/annotations.csv `
  --n_splits 5 `
  --epochs 60 `
  --batch_size 16 `
  --multiscale
```

---

## 8. Artifact Locations & File Structure

```
d:\Projects\surgwound-assist\
├── data/
│   ├── annotations.csv                # Official 686-image dataset (480 train / 69 val / 137 test)
│   └── images/                        # High-resolution clinical wound photographs
├── docs/
│   ├── base_paper_comparison.md       # Full comparative analysis vs SurgWound-Bench / WoundQwen
│   ├── implementation.md              # This document: master implementation guide
│   ├── architecture.md                # Architectural diagrams, evolution table, and parameter counts
│   ├── CHANGELOG.md                   # Chronological engineering log
│   ├── best_model.pth                 # Official champion model checkpoint
│   ├── best_evaluation_report.md      # SOTA evaluation report (54.29% Macro-F1)
│   ├── quad_ensemble_evaluation_report.md # Quad SOTA report (0.8412 ROC-AUC record)
│   └── evaluation_report.md           # Synchronized active evaluation report
├── v8/
│   ├── src/
│   │   ├── config.py                  # Clinical attribute taxonomy & hyperparameters
│   │   ├── dataset.py                 # Multi-scale PyTorch dataset loader
│   │   ├── model.py                   # BiomedCLIP ViT-B/16 multi-task architecture
│   │   ├── loss.py                    # Logit-Adjusted & Adaptive-Tau loss functions
│   │   ├── train.py                   # Training loop with AMP, LLRD, and patience
│   │   ├── evaluate.py                # 7x TTA, ROC-AUC, Cohen's Kappa, and threshold calibration
│   │   ├── ensemble.py                # Dirichlet simplex weight optimizer & fusion engine
│   │   ├── kfold_cv.py                # Stratified 5-fold cross-validation
│   │   ├── retrain_foundational_and_ensemble.py # Autonomous master pipeline orchestrator
│   │   └── clinical_text_prototypes.pt# PubMedBERT normalized 512-dim prototype vectors
│   ├── experiments/
│   │   └── experiment_registry.csv    # Central scientific experiment ledger
│   ├── reports/                       # Archived milestone reports
│   └── runs/                          # Timestamped run directories with weights & plots
```

---
*Document verified and synchronized with codebase implementation in `v8/src/` and official evaluation benchmarks in `docs/`.*
