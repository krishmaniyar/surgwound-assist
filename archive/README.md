# Experiment Archive

This folder preserves all experimental code from the research process.
**Do not delete.** These files are needed for the research paper to document
the full experimental timeline and justify each architectural decision.

## Contents

| Folder | What it Contains | Why Superseded |
|--------|-----------------|----------------|
| `v2_static_embeddings/` | DINOv2+CLIP frozen feature extraction + MLP heads | End-to-end fine-tuning proved far superior (+16.5% F1) |
| `cnn_finetune_experiment/` | ResNet/EfficientNet fine-tuning | ViT-based DINOv2 outperformed CNNs on this task |
| `ensemble_experiment/` | Multi-model ensemble averaging | Replaced by Test-Time Augmentation in BiomedCLIP pipeline |
| `hyperparameter_tuning/` | Optuna HPO + ablation studies | Served its purpose; results documented in research journal |
| `data_imbalance_experiments/` | SMOTE, resampling, imbalance analysis | LDAM+DRW loss proved superior to resampling approaches |
| `inference_fixes/` | Post-hoc calibration attempts | Temperature scaling showed marginal gains vs. better pretraining |
| `v2_onnx_model/` | First exported ONNX model (v2) | Replaced by v7 BiomedCLIP ONNX |

## Research Paper Reference
See `docs/research_journal.md` for the full experimental narrative
with academic-quality justification for every decision.
