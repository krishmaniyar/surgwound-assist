# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **54.29%**
- **Mean Accuracy**: 72.99%
- **Mean Macro-Precision**: 52.36%
- **Mean Macro-Recall**: 62.86%
- **Mean Weighted-F1**: 71.99%
- **Mean ROC-AUC**: 0.8172
- **Mean Cohen's Kappa**: 0.4262
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **47.11%**
- **Exact Match Ratio**: 27.74%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  64.23% |  65.93% |  75.47% |  66.45% |  64.23% |  61.11% | 0.9413 | 0.5742 |
| healing_status   |  80.29% |  79.64% |  79.05% |  79.30% |  80.29% |  80.19% | 0.8455 | 0.5862 |
| closure_method   |  53.28% |  35.36% |  37.85% |  33.04% |  53.28% |  51.56% | 0.7347 | 0.3013 |
| exudate_type     |  70.07% |  31.13% |  53.89% |  37.41% |  70.07% |  69.77% | 0.8018 | 0.2257 |
| erythema         |  77.37% |  50.91% |  52.37% |  51.63% |  77.37% |  76.55% | 0.7577 | 0.5118 |
| edema            |  74.45% |  48.03% |  57.13% |  52.17% |  74.45% |  68.83% | 0.7380 | 0.4010 |
| infection_risk   |  83.94% |  60.14% |  79.60% |  65.81% |  83.94% |  85.87% | 0.9174 | 0.5237 |
| urgency_level    |  80.29% |  47.77% |  67.54% |  48.50% |  80.29% |  82.04% | 0.8012 | 0.2856 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  48.5% |  84.2% |  61.5% | 19.0 |
| Patella                   |  42.9% | 100.0% |  60.0% | 3.0 |
| Ankle                     |  87.5% |  73.7% |  80.0% | 19.0 |
| Facial region             |  86.7% |  86.7% |  86.7% | 15.0 |
| Manus                     |  90.9% | 100.0% |  95.2% | 10.0 |
| Cervical region           |  50.0% |  75.0% |  60.0% | 4.0 |
| Other                     |  58.5% |  68.6% |  63.2% | 35.0 |
| Uncertain                 |  62.5% |  15.6% |  25.0% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  82.4% |  85.4% |  83.8% | 82.0 |
| Not Healed                |  76.9% |  72.7% |  74.8% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  37.8% |  73.7% |  50.0% | 19.0 |
| Sutures                   |  70.8% |  75.0% |  72.9% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |  14.3% |  25.0% |  18.2% | 4.0 |
| Uncertain                 |  53.8% |  15.6% |  24.1% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  85.6% |  81.7% |  83.6% | 109.0 |
| Serous                    |  14.3% |  25.0% |  18.2% | 8.0 |
| Sanguineous               |  28.6% |  50.0% |  36.4% | 4.0 |
| Purulent                  |  25.0% |  66.7% |  36.4% | 3.0 |
| Seropurulent              |  33.3% | 100.0% |  50.0% | 1.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  83.7% |  84.6% |  84.2% | 91.0 |
| Existent                  |  69.0% |  72.5% |  70.7% | 40.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  78.7% |  90.4% |  84.2% | 94.0 |
| Existent                  |  65.4% |  81.0% |  72.3% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  97.1% |  85.5% |  90.9% | 117.0 |
| Medium                    |  50.0% |  73.3% |  59.5% | 15.0 |
| High                      |  33.3% |  80.0% |  47.1% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  93.7% |  86.0% |  89.7% | 121.0 |
| Clinic Visit (Yellow, <48h) |  28.6% |  16.7% |  21.1% | 12.0 |
| Emergency Care (Red, immediate) |  21.1% | 100.0% |  34.8% | 4.0 |
