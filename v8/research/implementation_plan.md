# SurgWound Assist v8 — Autonomous ML Research & Implementation Plan

## Executive Summary

The objective of **SurgWound Assist v8** is to autonomously research, design, implement, train, evaluate, and iterate a superior multi-task surgical wound attribute classification pipeline on the held-out test set, with the explicit requirement of exceeding the official **v7.5 baseline test Macro-F1 of 51.10%**.

The task classifies **8 clinical attributes** from post-operative surgical wound photographs:
1. `location` (8 classes)
2. `healing_status` (2 classes)
3. `closure_method` (5 classes)
4. `exudate_type` (6 classes)
5. `erythema` (3 classes)
6. `edema` (3 classes)
7. `infection_risk` (3 classes)
8. `urgency_level` (3 classes)

Operating constraints:
- Hardware: NVIDIA GeForce RTX 3060 Laptop GPU (6 GB VRAM)
- OS: Windows 11, PyTorch 2.6.0+cu124, Python 3.10, open_clip 3.3.0
- Small-data regime: 349 annotated images (train: 244, val: 35, test: 70)
- Strict test-set integrity: all model selection and hyperparameter decisions will be made solely on the training/validation splits.

---

## Phase 0 Audit & Ground Truth Discoveries

### 1. The Official v7.5 Baseline Metrics

From `v7/src/runs/run_20260904_163252/biomedclip_metrics.json`:
- **Mean Test Macro-F1 (with 7× TTA)**: **51.10%** (0.51097)
- **Mean Test Accuracy**: **77.50%**
- **Mean Test Macro-Precision**: **50.65%**
- **Mean Test Macro-Recall**: **52.12%**
- **Mean Test Weighted-F1**: **75.04%**
- **Exact Match Ratio**: **14.29%** (10 / 70 images)

Per-Attribute Breakdown in v7.5:
| Attribute | Test Accuracy | Test Macro-Recall | Test Macro-F1 | Bottleneck Diagnosis |
|---|---|---|---|---|
| `healing_status` | 77.14% | 75.88% | **75.88%** | Strong; tractable binary task |
| `erythema` | 80.00% | 65.95% | **64.80%** | Moderate; detects redness patterns |
| `urgency_level` | 100.00% | 100.00% | **100.00%** | *Diagnostic anomaly (see discovery below)* |
| `edema` | 72.86% | 47.71% | **46.78%** | Weak minority recall: Existent edema recall is only 7.7% |
| `location` | 54.29% | 42.22% | **40.76%** | Confusion: 9/13 Patella classified as "Other" |
| `closure_method` | 67.14% | 32.78% | **32.00%** | Minority collapse: Staples F1=0%, Adhesives F1=0% |
| `infection_risk` | 80.00% | 32.75% | **29.63%** | Minority collapse: Medium F1=0%, High F1=0% |
| `exudate_type` | 88.57% | 19.68% | **18.93%** | Minority collapse: Purulent, Sanguineous, Serous, Seropurulent all F1=0% |

> [!IMPORTANT]
> **Key Insight on v7.5 Macro-F1 Composition**:
> Excluding `urgency_level`, the mean Macro-F1 across the other 7 real clinical attributes is **44.11%**. The minority classes in `exudate_type`, `infection_risk`, `closure_method`, and `edema` collapsed to near 0% recall under standard argmax prediction. This means the primary headroom for v8 lies in **recovering minority-class recall** on these four weak attributes.

### 2. Dataset Audit & Audit Discovery: `urgency_level` String Normalization

During our audit of `archive/dataset_backup_v7/annotations.csv` vs `v7/src/config.py`:
- In the 349-image annotation file, the `urgency_level` values are:
  - `"Home Care (Green): Manage with routine care"` (311 samples: 216 train, 33 val, 62 test)
  - `"Clinic Visit (Yellow): Requires professional evaluation within 48 hours"` (34 samples: 25 train, 2 val, 7 test)
  - `"Emergency Care (Red): Seek immediate medical attention"` (4 samples: 3 train, 0 val, 1 test)
- In `v7/src/config.py`, `CLASS_MAPPINGS['urgency_level']` was defined as:
  `['Home Care (Green)', 'Clinic Visit (Yellow, <48h)', 'Emergency Care (Red, immediate)']`.
- In `v7/src/dataset.py`, `normalize_label()` fell back to `return 0` whenever `val not in CLASS_MAPPINGS[attr]`.
- Consequently, in v7.5, every sample in train, val, and test was normalized to label `0`. The model predicted label `0` for all 70 test samples, yielding an artificial 100% Macro-F1.
- In `data/annotations.csv` (used in v7.6 with 686 images), the labels were normalized to short strings, and `urgency_level` true Macro-F1 was **34.41%**.

**Decision for v8 Baseline Reproducibility and Integrity**:
To ensure direct, apples-to-apples comparability with v7.5:
1. `v8/configs/v7_5_baseline.yaml` will reproduce the exact v7.5 setup on the 349-image split, logging both the raw v7.5 reproduction (with the legacy mapping) and the sanitized mapping.
2. In v8 experiments, we will provide both:
   - The **Legacy-aligned Macro-F1** (for direct 1-to-1 comparison with v7.5's 51.10% baseline).
   - The **Cleaned 8-head Macro-F1** (with true urgency labels evaluated).
   This guarantees complete scientific transparency without ambiguity.

---

## Literature Research & Research Matrix

We surveyed current literature in medical foundation models, long-tailed learning, multi-task learning, and small-data vision regimes:

1. **Medical Vision Foundation Models**:
   - *BiomedCLIP* (Zhang et al., 2023): ViT-B/16 pretrained on 15M PubMed Central figure-caption pairs. Pretrained feature space natively embeds clinical wound concepts ("erythema", "sutures", "purulent"). Fits comfortably in 6GB VRAM (batch size 16 requires ~2.8 GB VRAM).
   - *DINOv2-Base/Large*: Pretrained on web photos. Demonstrated in v4/v5/v6 to underperform domain-specific pretraining due to lack of medical alignment.
   - *BioViL / BioViL-T*: Exclusively pretrained on chest radiographs (CXR); inappropriate for surgical wound photography.
   - *Conclusion*: BiomedCLIP remains the optimal vision encoder for 6GB VRAM.

2. **Long-Tail Imbalance Objectives**:
   - *Logit Adjustment (LA)* (Menon et al., ICLR 2021): Statistically optimal Fisher-consistent formulation for balanced error. Enforces additive margin $\log \pi_y$ directly into logits during training, or post-hoc logit shift during inference. Completely eliminates LDAM's `s * logits` gradient scaling instability!
   - *Balanced Softmax* (Ren et al., NeurIPS 2020): Reformulates multi-class cross-entropy with class-prior conditional probability $\log(n_y / \sum n_j)$. Extremely stable under standard AMP.
   - *Asymmetric Loss (ASL)* (Ridnik et al., ICCV 2021): Asymmetrically discounts negative sample gradients for dominant classes.

3. **Multi-Scale / High-Resolution Representation**:
   - Surgical wound photographs have median resolution 640×853 (up to 2048×2048). Downsampling to 224×224 removes suture knots, subtle purulence droplets, and localized edema borders.
   - *Global + Local Multi-Scale Fusion*: Extract a global 224×224 view (capturing body location and overall wound context) + high-resolution local crops (center wound bed or multi-crop patch) encoded by BiomedCLIP, concatenated into a 1024-dim fused representation.

4. **Vision-Language Semantic Prototype Heads**:
   - Instead of initializing classification heads with random Gaussian weights, pass attribute class names and medical descriptions through BiomedCLIP's PubMedBERT text encoder to generate normalized text embeddings $T_c$.
   - Initialize linear classifier weights with $W_c = T_c$, or use cosine-similarity classifier heads with learnable temperature $\tau$. This gives minority classes strong initial direction in feature space.

5. **Validation-Tuned Decision Thresholding**:
   - Argmax classification fails on long-tailed distributions because posterior probabilities of rare classes remain suppressed.
   - Tuning decision thresholds on validation data to maximize per-attribute Macro-F1 shifts decision boundaries toward optimal trade-offs without modifying the backbone.

### Research Prioritization Matrix (`v8/research/research_matrix.md`)

| Idea | Theoretical Basis | Relevance to SurgWound | Cost (VRAM / Time) | Risk | Expected Gain (Macro-F1) | Priority |
|---|---|---|---|---|---|---|
| **E1: Loss Modernization (Logit Adjustment / Balanced Softmax)** | Menon et al. ICLR 2021; Ren et al. NeurIPS 2020 | Direct fix for minority collapse without LDAM instability | Low (0 extra VRAM, fast) | Very Low | +3.0% to +5.0% on minority classes | **P0 (First)** |
| **E2: Semantic Text Prototype Classifier Heads** | Zhang et al. 2023; Radford et al. 2021 | Leverages PubMedBERT text embeddings to anchor rare classes | Low (offline text encoding) | Low | +2.0% to +4.0% | **P0 (First)** |
| **E3: Validation Decision Boundary Optimization** | Provost 2000; Collinearity / threshold tuning | Post-hoc adjustment of argmax for Macro-F1 maximization | Zero training cost | Zero | +2.0% to +4.0% | **P1 (Immediate)** |
| **E4: Global + Local Multi-Scale Feature Fusion** | Multi-crop ViT, Wang et al. 2023 | Recovers fine-grained suture/exudate details lost at 224×224 | Medium (+1.2 GB VRAM, fits 6GB) | Low | +3.0% to +6.0% | **P1 (High)** |
| **E5: Task-Specific Adapter Bottlenecks & Loss Balancing** | Houlsby et al. 2019; Kendall et al. CVPR 2018 | Reduces multi-task gradient conflict between easy & hard tasks | Low (+100K params per head) | Low | +1.5% to +3.0% | **P2** |
| **E6: Multi-Seed Ensemble + Medical-Safe TTA** | Deep Ensembles (Lakshminarayanan et al.) | Averages prediction variance across seeds (42, 123, 3407) | Inference only | Zero | +2.0% to +3.5% | **P2 (Final boost)** |

---

## Proposed Changes & V8 Architecture

We will create a clean, independent `v8/` directory structure without modifying existing `v7/` code.

```
v8/
├── configs/
│   ├── v7_5_baseline.yaml       # Exact machine-readable v7.5 baseline configuration
│   ├── v8_pilot.yaml            # Fast sanity check config
│   ├── v8_e1_balanced_loss.yaml # Loss modernization (Balanced Softmax / Logit Adjustment)
│   ├── v8_e2_text_prototypes.yaml # Text semantic prototype heads
│   ├── v8_e3_multiscale.yaml    # Global + Local feature fusion
│   └── v8_best.yaml             # Final selected v8 pipeline
├── src/
│   ├── __init__.py
│   ├── config.py                # v8 configuration schema and loader
│   ├── dataset.py               # Dataset loading, dual-scale image support, audited labels
│   ├── model.py                 # BiomedCLIP + Text prototypes + Global/Local multi-scale encoder
│   ├── losses.py                # Balanced Softmax, Logit-Adjusted CE, Class-Balanced Focal
│   ├── train.py                 # Multi-phase training engine with gradient monitoring & failure detection
│   ├── evaluate.py              # Full metric suite, TTA, validation threshold optimizer, reports
│   └── run_experiment.py        # Autonomous experiment runner and evaluator
├── experiments/
│   └── experiment_registry.csv  # Tracking table for every experiment
├── research/
│   └── research_matrix.md       # Literature and hypothesis matrix
├── research_journal.md          # Chronological log of hypotheses, runs, diagnostics, and takeaways
├── runs/                        # Run outputs (weights, logs, plots, reports)
├── reports/
│   └── V8_FINAL_REPORT.md       # Final scientific synthesis
└── README.md                    # Reproducibility documentation
```

### Component Details

#### 1. Configuration & Baseline Reproduction
- [NEW] `v8/configs/v7_5_baseline.yaml`: Machine-readable YAML specifying exact parameters of v7.5:
  - Backbone: `hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`
  - LR: `3e-5`, LLRD decay: `0.85`, AdamW weight decay: `1e-3`
  - Batch size: `16`, Accumulation: `2`, Warmup: `0.1` (64 steps)
  - Phase 1: Focal loss (`gamma=2.0`, `alpha=cb_weights`) for 70% of epochs (56 epochs)
  - Phase 2: LDAM loss (`max_m=0.5`, `s=15`, `in_ldam=True` with AMP disabled) with warm restart to `1e-5`
  - Seed: `42`
  - TTA: 7× stochastic passes

#### 2. Model Architecture Innovations (`v8/src/model.py`)
- **Text-Informed Classifier Heads**:
  Encode clinical attribute names and descriptors (e.g. `"purulent wound exudate"`, `"staples wound closure"`) using BiomedCLIP's PubMedBERT text encoder. Project text embeddings to 512-dim normalized feature space to initialize head weights or act as cosine prototypes:
  $$\text{logits}_c = \tau \cdot \frac{f_{\text{img}} \cdot T_c}{\|f_{\text{img}}\| \|T_c\|}$$
- **Global + Local Multi-Scale Fusion**:
  - Global branch: 224×224 whole-wound image $\to$ ViT encoder $\to$ 512-dim embedding.
  - Local branch: High-resolution center crop / wound detail crop (336×336 or 448×448 downsampled to 224×224) $\to$ ViT encoder (weight-shared) $\to$ 512-dim embedding.
  - Fused representation: Concatenation or gated projection $[f_{\text{global}}; f_{\text{local}}] \to 512$-dim, feeding into attribute heads.

#### 3. Loss & Imbalance Modernization (`v8/src/losses.py`)
- **Logit-Adjusted Loss**:
  $$\mathcal{L}_{\text{LA}}(x, y) = -\log \frac{e^{x_y + \tau \log \pi_y}}{\sum_j e^{x_j + \tau \log \pi_j}}$$
  where $\pi_y = n_y / N$ is the class prior probability. This shifts margin proportionally to class frequency without requiring scaling factor $s$, completely avoiding FP16 overflow under standard AMP.
- **Balanced Softmax Loss**:
  Numerically stable, native FP16/AMP compatible, directly targets balanced error rate across classes.

#### 4. Training Engine & Automated Failure Detection (`v8/src/train.py`)
- Real-time diagnostics: monitor gradient norms per head and backbone, detect exploding gradients ($>10.0$) or vanishing gradients ($<10^{-6}$).
- Automatic majority-class collapse detection: monitor validation confusion matrices during training; if any attribute predicts a single class across the entire validation set for 5 consecutive epochs, trigger an alert.
- Safe AMP operation: Logit Adjustment is fully compatible with native AMP without requiring manual scaler bypasses.

#### 5. Validation-Tuned Decision Thresholds (`v8/src/evaluate.py`)
- Implement Nelder-Mead / grid optimization on the validation set to find per-class decision thresholds $\theta_c$ that maximize Macro-F1.
- Apply the validation-learned thresholds strictly to the test set predictions.

---

## Verification & Execution Roadmap

### Stage 1: Baseline Verification & Sanity Check
- Verify that `v8/configs/v7_5_baseline.yaml` accurately maps all 21 parameters of v7.5.
- Run a 3-epoch pilot run with `v8/src/train.py` to verify data loading, GPU memory (<4.5 GB VRAM), gradient flow, and metric reporting.

### Stage 2: Experiment 1 — Loss Modernization (Logit Adjustment / Balanced Softmax)
- Train v8 with Logit-Adjusted Loss and compare training stability and validation Macro-F1 against v7.5.
- Verify minority class recall on `exudate_type`, `infection_risk`, `closure_method`, and `edema`.

### Stage 3: Experiment 2 — Semantic Text Prototypes
- Initialize classifier heads using PubMedBERT embeddings of clinical descriptions.
- Evaluate impact on zero-shot / few-shot generalization for rare classes.

### Stage 4: Experiment 3 — Multi-Scale Global + Local Fusion
- Implement dual-branch (global context + local crop) encoder.
- Benchmark VRAM usage on the RTX 3060 (verify VRAM remains $\le 5.2$ GB).
- Measure gains on fine-grained attributes (`closure_method`, `exudate_type`).

### Stage 5: Experiment 4 — Validation Threshold Calibration
- Optimize decision thresholds on validation set.
- Apply to test predictions and measure Macro-F1 delta.

### Stage 6: Experiment 5 — Multi-Seed Ensemble & Final Evaluation
- Train best pipeline across seeds 42, 123, 3407.
- Average ensemble probabilities with 7× medical-safe TTA.
- Generate full metrics report, confusion matrices, and base-paper comparative tables.
- Produce `v8/reports/V8_FINAL_REPORT.md` and `v8/README.md`.

---

## Success Criteria

| Milestone | Target Test Macro-F1 | Status |
|---|---|---|
| **v7.5 Baseline** | **51.10%** | Baseline to exceed |
| **v8 Minimum Success** | **> 51.10%** | Mandatory |
| **v8 Strong Success** | **> 55.00%** | Target |
| **v8 Breakthrough** | **> 60.00%** | Stretch |
