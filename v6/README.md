# v6 - DINOv2-Large + LLRD + Warmup + Fixed Seed

**Status**: Completed (superseded by v7 BiomedCLIP)

## Architecture
- Backbone: `facebook/dinov2-large` (300M params, 1024-dim hidden)
- Pretraining: Generic web photos (ImageNet-21k style)
- Heads: 2-layer MLP - `Linear(1024-512) - GELU - Dropout - Linear`
- Loss: FocalLoss (epochs 0-36) - LDAM+DRW (epochs 36-60)
- Scheduler: Linear warmup (10%) + Cosine decay
- LLRD: Each transformer layer gets `LR - 0.85^depth`

## Results (Best Run: v6/run_20260829_092857)
- Validation Mean Macro-F1: ~62%
- Test Mean Macro-F1: TBD (run in progress at time of archive)

## Why Superseded
DINOv2 was pretrained on web photos, not medical images.
BiomedCLIP (v7) is pretrained on 15M PubMed medical image-text pairs,
providing far better domain alignment for surgical wound assessment.
See `docs/model_research.md`.

## Running (for reference)
```bash
cd v6/src
python run_pipeline.py
```
