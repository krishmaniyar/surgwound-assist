# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **52.63%**
- **Mean Accuracy**: 73.36%
- **Mean Macro-Precision**: 56.45%
- **Mean Macro-Recall**: 57.93%
- **Mean Weighted-F1**: 70.43%
- **Mean ROC-AUC**: 0.8408
- **Mean Cohen's Kappa**: 0.4028
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **46.08%**
- **Exact Match Ratio**: 29.20%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  61.31% |  53.57% |  75.38% |  59.46% |  61.31% |  54.66% | 0.9487 | 0.5510 |
| healing_status   |  78.10% |  77.37% |  76.62% |  76.92% |  78.10% |  77.95% | 0.8555 | 0.5388 |
| closure_method   |  54.01% |  40.96% |  37.85% |  33.16% |  54.01% |  45.73% | 0.7744 | 0.2923 |
| exudate_type     |  75.18% |  38.51% |  60.36% |  43.99% |  75.18% |  73.73% | 0.8268 | 0.3210 |
| erythema         |  78.10% |  50.29% |  51.80% |  51.00% |  78.10% |  76.19% | 0.7952 | 0.5043 |
| edema            |  73.72% |  44.69% |  56.77% |  49.79% |  73.72% |  67.66% | 0.7715 | 0.3951 |
| infection_risk   |  82.48% |  77.22% |  59.89% |  57.38% |  82.48% |  84.16% | 0.9356 | 0.4533 |
| urgency_level    |  83.94% |  69.00% |  44.74% |  49.37% |  83.94% |  83.38% | 0.8184 | 0.1667 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  51.4% | 100.0% |  67.9% | 19.0 |
| Patella                   |  21.4% | 100.0% |  35.3% | 3.0 |
| Ankle                     |  76.2% |  84.2% |  80.0% | 19.0 |
| Facial region             |  86.7% |  86.7% |  86.7% | 15.0 |
| Manus                     |  90.9% | 100.0% |  95.2% | 10.0 |
| Cervical region           |  37.5% |  75.0% |  50.0% | 4.0 |
| Other                     |  64.5% |  57.1% |  60.6% | 35.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  80.2% |  84.1% |  82.1% | 82.0 |
| Not Healed                |  74.5% |  69.1% |  71.7% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  36.6% |  78.9% |  50.0% | 19.0 |
| Sutures                   |  68.2% |  85.3% |  75.8% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 | 100.0% |  25.0% |  40.0% | 4.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  88.0% |  87.2% |  87.6% | 109.0 |
| Serous                    |  20.0% |  25.0% |  22.2% | 8.0 |
| Sanguineous               |  50.0% |  50.0% |  50.0% | 4.0 |
| Purulent                  |  23.1% | 100.0% |  37.5% | 3.0 |
| Seropurulent              |  50.0% | 100.0% |  66.7% | 1.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  81.6% |  87.9% |  84.7% | 91.0 |
| Existent                  |  69.2% |  67.5% |  68.4% | 40.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  79.2% |  89.4% |  84.0% | 94.0 |
| Existent                  |  54.8% |  81.0% |  65.4% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  96.2% |  86.3% |  91.0% | 117.0 |
| Medium                    |  35.5% |  73.3% |  47.8% | 15.0 |
| High                      | 100.0% |  20.0% |  33.3% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  90.3% |  92.6% |  91.4% | 121.0 |
| Clinic Visit (Yellow, <48h) |  16.7% |  16.7% |  16.7% | 12.0 |
| Emergency Care (Red, immediate) | 100.0% |  25.0% |  40.0% | 4.0 |
