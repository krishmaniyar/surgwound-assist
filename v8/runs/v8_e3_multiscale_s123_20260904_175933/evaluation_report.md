# SurgWound Assist — Experiment v8_e3_multiscale_s123 Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **49.64%**
- **Mean Accuracy**: 77.50%
- **Mean Macro-Precision**: 50.91%
- **Mean Macro-Recall**: 51.38%
- **Mean Weighted-F1**: 77.24%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **37.59%**
- **Exact Match Ratio**: 17.14%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  57.14% |  54.13% |  49.49% |  50.58% |  57.14% |  58.81% | N/A | 0.4635 |
| healing_status   |  75.71% |  76.39% |  71.27% |  72.16% |  75.71% |  74.44% | 0.8467 | 0.4536 |
| closure_method   |  68.57% |  34.94% |  36.67% |  35.78% |  68.57% |  66.99% | N/A | 0.3676 |
| exudate_type     |  80.00% |  23.97% |  37.46% |  26.18% |  80.00% |  82.39% | N/A | 0.2007 |
| erythema         |  84.29% |  72.22% |  79.58% |  74.76% |  84.29% |  85.39% | N/A | 0.4993 |
| edema            |  72.86% |  39.84% |  44.74% |  42.15% |  72.86% |  68.64% | N/A | -0.1329 |
| infection_risk   |  84.29% |  55.77% |  43.27% |  46.24% |  84.29% |  82.71% | N/A | 0.3825 |
| urgency_level    |  97.14% |  50.00% |  48.57% |  49.28% |  97.14% |  98.55% | N/A | 0.0000 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  91.7% |  78.6% |  84.6% | 14.0 |
| Patella                   |  50.0% |  38.5% |  43.5% | 13.0 |
| Ankle                     |  80.0% |  44.4% |  57.1% | 9.0 |
| Facial region             |  77.8% |  77.8% |  77.8% | 9.0 |
| Manus                     |   0.0% |   0.0% |   0.0% | 2.0 |
| Cervical region           |  33.3% |  50.0% |  40.0% | 2.0 |
| Other                     |  46.2% |  57.1% |  51.1% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  75.0% |  90.7% |  82.1% | 43.0 |
| Not Healed                |  77.8% |  51.9% |  62.2% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  63.2% |  66.7% |  64.9% | 18.0 |
| Sutures                   |  76.6% |  80.0% |  78.3% | 45.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 2.0 |
| Adhesives                 |   0.0% |   0.0% |   0.0% | 5.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  94.8% |  87.3% |  90.9% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 2.0 |
| Purulent                  |  25.0% | 100.0% |  40.0% | 1.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 2.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  94.4% |  86.4% |  90.3% | 59.0 |
| Existent                  |  50.0% |  72.7% |  59.3% | 11.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  79.7% |  89.5% |  84.3% | 57.0 |
| Existent                  |   0.0% |   0.0% |   0.0% | 13.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  87.3% |  96.5% |  91.7% | 57.0 |
| Medium                    |  80.0% |  33.3% |  47.1% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% |  97.1% |  98.6% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0 |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0.0 |
