# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **53.03%**
- **Mean Accuracy**: 73.45%
- **Mean Macro-Precision**: 53.44%
- **Mean Macro-Recall**: 58.21%
- **Mean Weighted-F1**: 72.78%
- **Mean ROC-AUC**: 0.8331
- **Mean Cohen's Kappa**: 0.4027
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **45.86%**
- **Exact Match Ratio**: 26.28%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  66.42% |  65.45% |  76.58% |  66.50% |  66.42% |  67.04% | 0.9493 | 0.6061 |
| healing_status   |  78.83% |  78.09% |  77.53% |  77.77% |  78.83% |  78.73% | 0.8401 | 0.5555 |
| closure_method   |  56.20% |  42.45% |  41.14% |  38.54% |  56.20% |  55.57% | 0.7316 | 0.3435 |
| exudate_type     |  75.91% |  47.34% |  55.11% |  40.21% |  75.91% |  75.22% | 0.8181 | 0.3245 |
| erythema         |  72.26% |  48.03% |  51.21% |  48.89% |  72.26% |  72.34% | 0.8048 | 0.4489 |
| edema            |  67.15% |  47.11% |  54.74% |  49.50% |  67.15% |  64.32% | 0.7671 | 0.3054 |
| infection_risk   |  83.94% |  52.61% |  60.46% |  55.19% |  83.94% |  85.58% | 0.9238 | 0.4945 |
| urgency_level    |  86.86% |  46.44% |  48.90% |  47.62% |  86.86% |  83.47% | 0.8299 | 0.1432 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  60.0% |  78.9% |  68.2% | 19.0 |
| Patella                   |  20.0% | 100.0% |  33.3% | 3.0 |
| Ankle                     |  87.5% |  73.7% |  80.0% | 19.0 |
| Facial region             |  81.2% |  86.7% |  83.9% | 15.0 |
| Manus                     |  71.4% | 100.0% |  83.3% | 10.0 |
| Cervical region           |  60.0% |  75.0% |  66.7% | 4.0 |
| Other                     |  72.0% |  51.4% |  60.0% | 35.0 |
| Uncertain                 |  71.4% |  46.9% |  56.6% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  81.2% |  84.1% |  82.6% | 82.0 |
| Not Healed                |  75.0% |  70.9% |  72.9% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  39.0% |  84.2% |  53.3% | 19.0 |
| Sutures                   |  75.4% |  72.1% |  73.7% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |  50.0% |  25.0% |  33.3% | 4.0 |
| Uncertain                 |  47.8% |  24.4% |  32.4% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  88.2% |  89.0% |  88.6% | 109.0 |
| Serous                    |  66.7% |  25.0% |  36.4% | 8.0 |
| Sanguineous               | 100.0% |  50.0% |  66.7% | 4.0 |
| Purulent                  |  12.5% |  66.7% |  21.1% | 3.0 |
| Seropurulent              |  16.7% | 100.0% |  28.6% | 1.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  85.9% |  73.6% |  79.3% | 91.0 |
| Existent                  |  58.2% |  80.0% |  67.4% | 40.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  77.1% |  78.7% |  77.9% | 94.0 |
| Existent                  |  53.1% |  81.0% |  64.2% | 21.0 |
| Uncertain                 |  11.1% |   4.5% |   6.5% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  97.2% |  88.0% |  92.4% | 117.0 |
| Medium                    |  44.0% |  73.3% |  55.0% | 15.0 |
| High                      |  16.7% |  20.0% |  18.2% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  89.3% |  96.7% |  92.9% | 121.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 12.0 |
| Emergency Care (Red, immediate) |  50.0% |  50.0% |  50.0% | 4.0 |
