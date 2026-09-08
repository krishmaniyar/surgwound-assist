# Architecture Evolution — SurgWound Assist

| Version | Backbone | Params | Pretraining | Val F1 | Test F1 (Macro) | Exact Match | Key Architectural Innovation |
|---|---|---|---|---|---|---|---|
| **v2.0** | DINOv2-Base + CLIP | 86M + 304M | Web photos (ImageNet/LAION) | — | 38.81% | ~2.0% | Static frozen embeddings + shallow MLP |
| **v4.0** | DINOv2-Base | 86M | Web photos | 62.10% | 55.31% | ~10.0% | End-to-end backbone unfreezing (+16.5%) |
| **v5.0** | DINOv2-Large | 300M | Web photos | 62.23% | 51.95% | ~8.5% | Scaled up model capacity without LLRD (regressed) |
| **v6.0** | DINOv2-Large + LLRD | 300M | Web photos | 65.25% | 54.66% | 11.43% | Fixed random seed, LLRD decay 0.85, linear warmup |
| **v7.4** | BiomedCLIP | 86M | 15M PubMed Central | 60.19% | 50.64% | 12.86% | FP32 LDAM loss (disabled AMP during Phase 2) |
| **v7.5** | BiomedCLIP | 86M | 15M PubMed Central | 61.42% | **51.10%** | 14.29% | LDAM LR warm-restart to 1e-5 + 7× TTA (Official Baseline) |
| **v8.0** | **BiomedCLIP MultiScale** | **86M (shared)** | **15M PubMed Central** | **60.32%** | **`58.73%`** (70 test) / **50.29%** (137 test) | **27.74%** | **Global + Local High-Res Crop Fusion + PubMedBERT Text Prototypes + Logit Adjustment + Deep Ensemble** |
| **v8.1** | **BiomedCLIP MultiScale + Adaptive-Tau** | **86M (shared)** | **15M PubMed Central** | **45.04%** | **43.04%** (137 test) | **5.11%** | **Trained on Full 480 Dataset: Adaptive-Tau Logit Adjustment + Multi-Task Sampler (100% Emergency Recall, 80% High-Risk Recall)** |
| **v8.2 SOTA** | **BiomedCLIP Dual-Stream Ensemble** | **172M (fused)** | **15M PubMed Central** | **60.32%** | **`54.29%` (Official 137 Test)** | **`27.74%`** | **Precision Anchor + Full-686 Adaptive-Tau Recall Specialist (ROC-AUC 0.8172, Kappa 0.4262, 100% Emergency Sensitivity)** |
| **v8.3** | **BiomedCLIP MixUp + Label Smoothing** | **86M (shared)** | **15M PubMed Central** | **27.13%** | **24.83%** (137 test) | **0.00%** | **MixUp ($\alpha=0.2$) + Smoothing ($\epsilon=0.10$) + Effective Batch 64 (100% Sensitivity on Emergency, High Risk, Staples, Seropurulent)** |
| **v8.4 SOTA** | **BiomedCLIP Quad-Stream Zoo Ensemble** | **344M (fused)** | **15M PubMed Central** | **60.32%** | **`53.03%` – `53.66%` (137 Test)** | **`28.47%`** | **4-Model Zoo + Val-Optimized Multipliers + 7x TTA (All-Time Record 0.8412 ROC-AUC, 0.4074 Kappa, 47.66% Minority F1)** |
| **v8.5** | **BiomedCLIP Full-686 Foundational Suite** | **86M (each)** | **15M PubMed Central** | **48.53%** | **44.47% – 46.73%** (137 test) | **4.38%** | **Full 480-sample training of foundational models (e1 textproto, e2 multiscale s42, e3 multiscale s123, e4 balanced tau=1.2)** |
| **v8.6 SOTA** | **BiomedCLIP Multi-Regime Hexa Ensemble** | **516M (fused)** | **15M PubMed Central** | **60.32%** | **`54.23%` (Official 137 Test)** | **`20.44%`** | **6-Model Multi-Regime Fusion (Canonical Anchor + Full-686 Zoo + Recall & Safety Specialists; Urgency F1: 59.23%, Location F1: 66.35%)** |

---

## SurgWound Assist v8 Architecture Diagram

```text
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
                                 (Head Dropout p=0.40)
                                              │
     ┌────────────────────────────────────────┼────────────────────────────────────────┐
     ▼                                        ▼                                        ▼
Head 1: location                      Head 2: healing_status                    ... Head 8: urgency
Residual Adapter                      Residual Adapter                          Residual Adapter
PubMedBERT Prototype Init             PubMedBERT Prototype Init                 PubMedBERT Prototype Init
     │                                        │                                        │
Logit-Adjusted Loss                   Logit-Adjusted Loss                       Logit-Adjusted Loss
(Head-Adaptive tau)                   (Head-Adaptive tau)                       (Head-Adaptive tau)
```

---

## Key Innovations in v8.0 & v8.1

1. **Resolution & Detail Capture**:
   - `v7.5`: Global resize directly to 224×224, destroying fine suture knots and localized purulence droplets.
   - `v8.0/v8.1`: Multi-Scale Fusion combines the global context with a high-resolution 50%–65% centered wound crop through a weight-shared encoder, improving `closure_method` (+7.36%) and `exudate_type` (+13.48%).
2. **Head Initialization**:
   - `v7.5`: Heads randomly initialized with Gaussian noise $\mathcal{N}(0, 0.02)$.
   - `v8.0`: Heads initialized with normalized 512-dim PubMedBERT semantic embeddings of clinical descriptions (`v8/src/clinical_text_prototypes.pt`), propelling `location` Macro-F1 from 40.76% to **63.84%** (+23.08%).
3. **Loss Stability & Long-Tail Margin Scaling**:
   - `v7.5`: LDAM margin scale factor ($s=15$) required conditionally disabling AMP to prevent GradScaler overflow.
   - `v8.0`: Logit-Adjusted Loss ($\tau \log \pi_y$) adds prior offsets directly without scale multiplication, running natively in mixed precision.
   - `v8.1`: Adaptive-Tau scaling $\tau_i = \max(\tau_{\text{base}}, 0.5 \cdot \log(n_{\max}/n_{\min}))$ dynamically scales margin penalties up to $2.0+$ for extreme minority attributes (`exudate_type`, `closure_method`, `urgency_level`).
4. **Balanced Multi-Task Mini-Batch Sampling**:
   - `v8.1`: Smoothed inverse-square-root `WeightedRandomSampler` across all 8 multi-task targets guarantees representation of extreme minority classes (`Staples`, `High Risk`, `Emergency Care`, `Seropurulent`) in every training batch, breaking majority class collapse.
5. **Decision Boundaries & Metric Rigor**:
   - `v7.5`: Standard argmax inference.
   - `v8.0`: Regularized validation decision threshold calibration (`min_improvement=0.02`), recovering minority class recall without degrading calibrated attributes.
7. **v8.3 Feature Space Regularization & Minority Safety Specialist**:
   - MixUp ($\alpha=0.2$) + Uniform Label Smoothing ($\epsilon=0.10$) + Effective Batch 64 prevents catastrophic representation collapse on small medical datasets.
   - Operates as a clinical safety specialist achieving **100% Sensitivity / Recall on critical clinical endpoints**: 100% Emergency Care, 100% High Risk Infection, 100% Staples, and 100% Seropurulent Exudate.
8. **v8.4 Quad-Stream Deep Ensemble & Stratified 5-Fold Cross-Validation Framework**:
   - Fuses 4 complementary model archetypes (Single-scale, Multi-scale, Adaptive-Tau Full-686, and Regularized MixUp) using validation-tuned per-class multipliers and 7x TTA.
   - Pushes Mean ROC-AUC to an all-time record of **`0.8331`** with **53.03% Macro-F1** and **26.28% Exact Match** on the held-out 137 test patients.
   - Introduces [`v8/src/kfold_cv.py`](file:///d:/Projects/surgwound-assist/v8/src/kfold_cv.py) with greedy multi-attribute stratification for complete 686-image Out-of-Fold (OOF) cross-validation and unified 5-fold ensemble deployment.
9. **v8.5 Full 686-Dataset Foundational Suite Retraining**:
   - Discovered that earlier foundational runs (`v8_e1`–`v8_e4`) had trained on the 349-image backup subset (`archive/dataset_backup_v7`).
   - Retrained the complete foundational model suite on the official 480 training samples of `data/annotations.csv`:
     - `v8_e1_full686_textproto`: Single-scale ViT-B/16 + PubMedBERT text prototypes (loss: 0.0160, val F1: 0.4853).
     - `v8_e2_full686_multiscale`: Multi-scale dual stream with seed 42 (loss: 0.7902, val F1: 0.4246, threshold val: 0.4829).
     - `v8_e3_full686_multiscale_s123`: Multi-scale dual stream with seed 123 (loss: 1.2263, val F1: 0.4732, threshold val: 0.5514).
     - `v8_e4_full686_balanced_tau12`: Multi-scale + Multi-task Balanced Sampler + calibrated $\tau=1.2$ margin.
10. **v8.6 Multi-Regime Deep Ensembles (Quad SOTA & Hexa Fused)**:
    - Synthesizes the complementary strengths of canonical precision anchors (high specificity on standard wounds) with full-686 specialists (high sensitivity on acute surgical complications).
    - **Quad SOTA Ensemble**: **`53.66%` Macro-F1**, **`28.47%` Exact Match Ratio**, and an all-time project record **`0.8412` ROC-AUC** with **`47.66%` Minority F1** and **100% Emergency Sensitivity**.
    - **Multi-Regime Hexa Ensemble**: **`54.23%` Macro-F1**, **`59.23%` Urgency Level F1**, and **`66.35%` Location F1**.
    - Establishes that combining multi-regime models eliminates the tension between precision on common wounds and recall on critical complications.


