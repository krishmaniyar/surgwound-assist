# SurgWound Assist — Experiment v8_e1_full686_textproto Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **46.73%**
- **Mean Accuracy**: 66.97%
- **Mean Macro-Precision**: 45.97%
- **Mean Macro-Recall**: 49.73%
- **Mean Weighted-F1**: 67.93%
- **Mean ROC-AUC**: 0.7753
- **Mean Cohen's Kappa**: 0.2992
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **37.31%**
- **Exact Match Ratio**: 10.22%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  62.04% |  60.02% |  65.48% |  59.70% |  62.04% |  63.41% | 0.9199 | 0.5516 |
| healing_status   |  68.61% |  67.51% |  67.79% |  67.62% |  68.61% |  68.74% | 0.7436 | 0.3527 |
| closure_method   |  48.91% |  30.75% |  28.17% |  29.21% |  48.91% |  52.08% | 0.7274 | 0.2417 |
| exudate_type     |  67.15% |  23.84% |  30.66% |  24.98% |  67.15% |  69.63% | 0.7530 | 0.2149 |
| erythema         |  68.61% |  43.35% |  43.31% |  43.20% |  68.61% |  67.23% | 0.7187 | 0.2938 |
| edema            |  56.20% |  39.13% |  39.42% |  39.26% |  56.20% |  56.14% | 0.6499 | 0.0876 |
| infection_risk   |  81.02% |  52.67% |  62.39% |  55.79% |  81.02% |  82.31% | 0.8682 | 0.3632 |
| urgency_level    |  83.21% |  50.47% |  60.58% |  54.05% |  83.21% |  83.89% | 0.8219 | 0.2884 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  48.1% |  68.4% |  56.5% | 19.0 |
| Patella                   |  16.7% |  66.7% |  26.7% | 3.0 |
| Ankle                     |  87.5% |  73.7% |  80.0% | 19.0 |
| Facial region             |  91.7% |  73.3% |  81.5% | 15.0 |
| Manus                     |  60.0% |  90.0% |  72.0% | 10.0 |
| Cervical region           |  40.0% |  50.0% |  44.4% | 4.0 |
| Other                     |  65.4% |  48.6% |  55.7% | 35.0 |
| Uncertain                 |  70.8% |  53.1% |  60.7% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  74.7% |  72.0% |  73.3% | 82.0 |
| Not Healed                |  60.3% |  63.6% |  61.9% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  35.0% |  36.8% |  35.9% | 19.0 |
| Sutures                   |  75.0% |  57.4% |  65.0% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |   0.0% |   0.0% |   0.0% | 4.0 |
| Uncertain                 |  43.8% |  46.7% |  45.2% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  88.8% |  79.8% |  84.1% | 109.0 |
| Serous                    |  12.5% |  12.5% |  12.5% | 8.0 |
| Sanguineous               |  18.2% |  50.0% |  26.7% | 4.0 |
| Purulent                  |  11.1% |  33.3% |  16.7% | 3.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 1.0 |
| Uncertain                 |  12.5% |   8.3% |  10.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  75.8% |  82.4% |  78.9% | 91.0 |
| Existent                  |  54.3% |  47.5% |  50.7% | 40.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  71.3% |  71.3% |  71.3% | 94.0 |
| Existent                  |  31.8% |  33.3% |  32.6% | 21.0 |
| Uncertain                 |  14.3% |  13.6% |  14.0% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  92.7% |  87.2% |  89.9% | 117.0 |
| Medium                    |  35.3% |  40.0% |  37.5% | 15.0 |
| High                      |  30.0% |  60.0% |  40.0% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  93.2% |  90.1% |  91.6% | 121.0 |
| Clinic Visit (Yellow, <48h) |  15.4% |  16.7% |  16.0% | 12.0 |
| Emergency Care (Red, immediate) |  42.9% |  75.0% |  54.5% | 4.0 |
