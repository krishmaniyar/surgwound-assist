# SurgWound Assist v8 — Research Matrix

Comprehensive literature evaluation and ranking of candidate techniques for multi-task surgical wound attribute classification under small-data (349 images), extreme long-tailed class imbalance, and 6 GB VRAM constraints.

## Research Prioritization Matrix

| ID | Candidate Technique | Theoretical Basis / Literature | Relevance to SurgWound Assist | Cost (VRAM / Time) | Risk | Expected Gain (Macro-F1) | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| **E1** | **Logit Adjustment (LA) & Balanced Softmax** | Menon et al. (ICLR 2021), Ren et al. (NeurIPS 2020) | Solves minority class collapse directly without LDAM margin/gradient scaling instability (`s*scale` overflow). Fully AMP-safe. | Zero extra VRAM; fast training (~8 min) | Very Low | +3.0% to +5.0% | **P0** | **Ready to test** |
| **E2** | **BiomedCLIP Semantic Text-Prototype Classifier Heads** | Zhang et al. (2023), Radford et al. (2021) | Instead of random linear weights, initializes head weights from PubMedBERT embeddings of clinical descriptors ("purulent exudate", "surgical staples"). | Zero training VRAM (offline encoding) | Low | +2.0% to +4.0% | **P0** | **Ready to test** |
| **E3** | **Validation-Tuned Decision Thresholds** | Provost (2000), Macro-F1 threshold search | Argmax prediction inherently suppresses rare classes. Optimizing per-class decision thresholds on validation set restores recall. | Zero training cost; seconds at eval | Zero | +2.0% to +4.0% | **P1** | **Scheduled** |
| **E4** | **Global + Local Multi-Scale Feature Fusion** | Multi-crop ViT, Wang et al. (2023) | 224×224 downsampling erases fine suture threads and fluid drops. Fusing whole image (global context) + high-res wound crop (local detail). | +1.2 GB VRAM (~4.0 GB total, fits 6GB); +30% time | Low | +3.0% to +6.0% | **P1** | **Scheduled** |
| **E5** | **Task-Specific Feature Adapters & Loss Balancing** | Houlsby et al. (2019), Kendall et al. (CVPR 2018) | Decouples representation learning for dominant vs rare tasks (e.g. healing status vs exudate type) to prevent gradient conflict. | +0.2 GB VRAM; +5% time | Low | +1.5% to +3.0% | **P2** | **Scheduled** |
| **E6** | **Multi-Seed Deep Ensemble (Seeds 42, 123, 3407) + Medical TTA** | Lakshminarayanan et al. (NeurIPS 2017) | Mitigates seed variance and complements error profiles across multiple initializations. | Zero extra training VRAM; linear training time | Zero | +2.0% to +3.5% | **P2** | **Scheduled** |

---

## Detailed Literature Analysis

### 1. Foundation Models
- **BiomedCLIP** (ViT-B/16, 86M params): Pretrained on 15 million figure-caption pairs from PubMed Central. Natively encodes wound concepts. Fits within 6 GB VRAM with batch size 16.
- **DINOv2** (Base/Large): Strong self-supervised representations on web photos, but lacks medical terminology and domain calibration.
- **Decision**: Retain BiomedCLIP as the primary vision-language backbone.

### 2. Imbalance Objectives
- **LDAM + DRW (v7.5 baseline)**: Imposes class-dependent margins. Requires scale $s=15$ or $30$, which fatally interacted with `GradScaler` in FP16, requiring disabling AMP.
- **Logit Adjustment (LA)**: Directly adds $\tau \cdot \log(\pi_y)$ to logits. Statistically Fisher-consistent for balanced error rate. Completely avoids scale multiplications during backpropagation and runs stably in native FP16/AMP.
- **Balanced Softmax**: Incorporates label distribution into softmax denominator. Mathematically equivalent to maximizing balanced accuracy.

### 3. Multi-Scale Global + Local Representation
- Post-operative photographs have resolutions between 640×853 and 2048×2048. Downsampling to 224×224 obliterates critical diagnostic visual features (e.g., staple prongs vs suture thread, slight purulent discharge).
- Encoding both the global context (224×224) and a localized high-resolution crop (224×224 sampled from native resolution) through weight-shared BiomedCLIP ViT yields a rich 1024-dim representation before task heads.
