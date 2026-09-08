# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **46.27%**
- **Mean Accuracy**: 67.15%
- **Mean Macro-Precision**: 45.88%
- **Mean Macro-Recall**: 49.21%
- **Mean Weighted-F1**: 67.83%
- **Mean ROC-AUC**: 0.7738
- **Mean Cohen's Kappa**: 0.3014
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **37.61%**
- **Exact Match Ratio**: 9.49%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  59.85% |  55.54% |  61.64% |  55.51% |  59.85% |  60.31% | 0.9263 | 0.5263 |
| healing_status   |  67.88% |  66.41% |  65.39% |  65.64% |  67.88% |  67.37% | 0.7572 | 0.3153 |
| closure_method   |  54.74% |  31.27% |  31.73% |  31.15% |  54.74% |  56.00% | 0.6528 | 0.3036 |
| exudate_type     |  67.88% |  25.07% |  28.73% |  26.23% |  67.88% |  70.11% | 0.7217 | 0.2060 |
| erythema         |  67.88% |  43.95% |  43.87% |  43.89% |  67.88% |  67.42% | 0.7306 | 0.3043 |
| edema            |  59.85% |  39.50% |  37.49% |  37.85% |  59.85% |  57.28% | 0.6758 | 0.0656 |
| infection_risk   |  75.91% |  54.54% |  61.77% |  55.20% |  75.91% |  79.53% | 0.8582 | 0.3515 |
| urgency_level    |  83.21% |  50.75% |  63.09% |  54.71% |  83.21% |  84.59% | 0.8679 | 0.3384 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  50.0% |  63.2% |  55.8% | 19.0 |
| Patella                   |  18.2% |  66.7% |  28.6% | 3.0 |
| Ankle                     |  75.0% |  78.9% |  76.9% | 19.0 |
| Facial region             |  84.6% |  73.3% |  78.6% | 15.0 |
| Manus                     |  50.0% |  90.0% |  64.3% | 10.0 |
| Cervical region           |  33.3% |  25.0% |  28.6% | 4.0 |
| Other                     |  65.2% |  42.9% |  51.7% | 35.0 |
| Uncertain                 |  68.0% |  53.1% |  59.6% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  71.1% |  78.0% |  74.4% | 82.0 |
| Not Healed                |  61.7% |  52.7% |  56.9% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  32.0% |  42.1% |  36.4% | 19.0 |
| Sutures                   |  78.2% |  63.2% |  69.9% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |   0.0% |   0.0% |   0.0% | 4.0 |
| Uncertain                 |  46.2% |  53.3% |  49.5% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  88.0% |  80.7% |  84.2% | 109.0 |
| Serous                    |  22.2% |  25.0% |  23.5% | 8.0 |
| Sanguineous               |  12.5% |  25.0% |  16.7% | 4.0 |
| Purulent                  |  20.0% |  33.3% |  25.0% | 3.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 1.0 |
| Uncertain                 |   7.7% |   8.3% |   8.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  76.6% |  79.1% |  77.8% | 91.0 |
| Existent                  |  55.3% |  52.5% |  53.8% | 40.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  70.1% |  79.8% |  74.6% | 94.0 |
| Existent                  |  30.8% |  19.0% |  23.5% | 21.0 |
| Uncertain                 |  17.6% |  13.6% |  15.4% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  95.8% |  78.6% |  86.4% | 117.0 |
| Medium                    |  27.8% |  66.7% |  39.2% | 15.0 |
| High                      |  40.0% |  40.0% |  40.0% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  94.7% |  89.3% |  91.9% | 121.0 |
| Clinic Visit (Yellow, <48h) |  20.0% |  25.0% |  22.2% | 12.0 |
| Emergency Care (Red, immediate) |  37.5% |  75.0% |  50.0% | 4.0 |
