# v7 - BiomedCLIP Medical Domain (CURRENT)

**Status**: Active - this is the current best model

## Why BiomedCLIP
- Pretrained on 15M PubMed medical image-text pairs
- Natively understands surgical wounds, erythema, exudate types
- Domain-aligned pretraining > raw model size for tiny datasets
- Smaller (86M params) but smarter - larger batch_size (16), faster training
- See `docs/model_research.md` for full analysis

## Architecture
- Backbone: `microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224`
- Visual Encoder: ViT-B/16 (86M params), output_dim=512
- Heads: `LayerNorm - Linear(512-256) - GELU - Dropout - Linear`
- Loss: FocalLoss - LDAM+DRW (switches at 50% of epochs)
- Eval: 7- Test-Time Augmentation (TTA)

## Running
```bash
cd v7/src
python run_pipeline.py
```

## Runs
All runs are saved to `v7/runs/` automatically.
