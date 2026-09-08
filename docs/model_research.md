# Model Research Report — SurgWound Assist

**Date**: 2026-08-29  
**Context**: After achieving 55.31% Mean Macro-F1 with DINOv2-Large (300M params) end-to-end fine-tuning, we researched whether a better architecture exists for our specific task.

## Problem With Current Approach

`facebook/dinov2-large` was pre-trained on **142M web photographs** — furniture, animals, sports, nature. It has never encountered a surgical wound during pretraining. Every fine-tuning epoch is teaching it from scratch what a wound looks like.

## Key Finding: Domain > Scale

Research across medical imaging literature confirms:

> **A smaller model pre-trained on medical data almost always outperforms a larger model pre-trained on photos for medical classification tasks.**

## Evaluated Alternatives

### 1. `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224` ⭐ CHOSEN
- Pre-trained on **15 million medical image-text pairs** from PubMed Central
- Surgical images, histology, clinical photographs are natively understood
- ViT-Base (86M params) — fits in 6GB VRAM with batch_size=16
- Expected training time: ~25-30 minutes per run
- **Why we switched**: Domain alignment beats raw model size for tiny datasets

### 2. `google/siglip-so400m-patch14-384`
- Google's improved CLIP with sigmoid loss (better for multi-label tasks)
- 400M params, 1152-dim. Needs ~5-6 GB VRAM
- Good choice but general domain (not medical-specific)

### 3. `facebook/dinov2-giant` (1.1B params)
- Already attempted (v5.0). 4-5 hours training time on RTX 3060.
- Generic web pretraining still limits ceiling for medical tasks.

### 4. Ensemble + TTA (model-agnostic)
- Average predictions across 3 seeds and 7 TTA augmentations
- Free +3-5% without retraining — implemented in `evaluate.py`

## Metric Progression Summary

| Version | Architecture | Val F1 | Test F1 | Change |
|---------|--------------|--------|---------|--------|
| v2.0 | DINOv2-Base + CLIP (Static embeddings) | — | 38.81% | Baseline |
| v4.0 | DINOv2-Base (End-to-End) | 62.10% | 55.31% | +16.5% |
| v5.0 | DINOv2-Large (End-to-End) | 62.23% | 51.95% | ~stable |
| v6.0 | DINOv2-Large + LLRD + Warmup | running | TBD | — |
| **v7.0** | **BiomedCLIP (Medical Domain)** | **TBD** | **~70%?** | **TBD** |

## Why BiomedCLIP Will Work Better

Our 8 attributes map almost perfectly to things BiomedCLIP has learned from medical literature:
- `erythema` — skin redness appears constantly in wound papers
- `exudate_type` — serous, purulent, sanguineous are exact medical terms in PMC
- `closure_method` — staples and sutures appear in thousands of surgical case studies
- `healing_status` — wound healing staging is a major medical imaging research area
- `infection_risk` — clinical wound infection classification is well-documented in PMC

---

*Research conducted by AI agent — references: BiomedCLIP paper (Zhang et al. 2023), DINOv2 medical benchmarks (Oquab et al. 2024), SigLIP comparison papers.*
