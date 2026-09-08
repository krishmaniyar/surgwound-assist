# Domain-Adaptive Pretraining Ablation

| Config | Exudate Type | Infection Risk | Urgency Level | Closure Method | Mean Macro-F1 (all heads) |
|---|---|---|---|---|---|
| DINOv2+CLIP baseline (reported) | 3.83% | 24.09% | 12.92% | 16.10% | 37.62% |
| + per-class threshold tuning (no retrain) | 3.83% | 36.54% | 10.93% | 8.64% | 38.99% |
| + logit adjustment | 0.00% | 29.87% | 29.57% | 0.00% | 15.55% |
| + class merging (documented per §2) | 31.58% | 59.77% | 52.38% | 49.16% | 54.61% |
| + class-balanced loss + focal | 11.32% | 63.81% | 53.33% | 51.11% | 52.95% |
| + embedding-space SMOTE | 23.50% | 61.82% | 65.00% | 50.15% | 55.56% |
| + τ-normalization / decoupled head retrain | 35.15% | 67.38% | 70.32% | 50.49% | 58.42% |
| **Full stack (final, this pass)** | **35.15%** | **67.38%** | **70.32%** | **50.49%** | **58.42%** |
