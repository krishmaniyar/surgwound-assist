# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **53.66%**
- **Mean Accuracy**: 73.36%
- **Mean Macro-Precision**: 57.98%
- **Mean Macro-Recall**: 58.19%
- **Mean Weighted-F1**: 70.48%
- **Mean ROC-AUC**: 0.8412
- **Mean Cohen's Kappa**: 0.4074
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **47.66%**
- **Exact Match Ratio**: 28.47%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  61.31% |  53.50% |  75.38% |  59.50% |  61.31% |  54.60% | 0.9505 | 0.5506 |
| healing_status   |  77.37% |  76.54% |  76.01% |  76.23% |  77.37% |  77.26% | 0.8570 | 0.5249 |
| closure_method   |  54.74% |  41.46% |  38.14% |  33.75% |  54.74% |  46.25% | 0.7801 | 0.2989 |
| exudate_type     |  75.18% |  49.10% |  60.36% |  50.04% |  75.18% |  74.09% | 0.8300 | 0.3209 |
| erythema         |  78.10% |  50.29% |  51.80% |  51.00% |  78.10% |  76.19% | 0.7874 | 0.5043 |
| edema            |  72.99% |  44.38% |  56.42% |  49.46% |  72.99% |  66.97% | 0.7748 | 0.3783 |
| infection_risk   |  82.48% |  77.22% |  59.89% |  57.38% |  82.48% |  84.16% | 0.9362 | 0.4533 |
| urgency_level    |  84.67% |  71.38% |  47.52% |  51.93% |  84.67% |  84.35% | 0.8139 | 0.2279 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  52.8% | 100.0% |  69.1% | 19.0 |
| Patella                   |  21.4% | 100.0% |  35.3% | 3.0 |
| Ankle                     |  76.2% |  84.2% |  80.0% | 19.0 |
| Facial region             |  86.7% |  86.7% |  86.7% | 15.0 |
| Manus                     |  90.9% | 100.0% |  95.2% | 10.0 |
| Cervical region           |  37.5% |  75.0% |  50.0% | 4.0 |
| Other                     |  62.5% |  57.1% |  59.7% | 35.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  80.0% |  82.9% |  81.4% | 82.0 |
| Not Healed                |  73.1% |  69.1% |  71.0% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  39.5% |  78.9% |  52.6% | 19.0 |
| Sutures                   |  67.8% |  86.8% |  76.1% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 | 100.0% |  25.0% |  40.0% | 4.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  88.0% |  87.2% |  87.6% | 109.0 |
| Serous                    |  20.0% |  25.0% |  22.2% | 8.0 |
| Sanguineous               |  66.7% |  50.0% |  57.1% | 4.0 |
| Purulent                  |  20.0% | 100.0% |  33.3% | 3.0 |
| Seropurulent              | 100.0% | 100.0% | 100.0% | 1.0 |
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
| Non-existent              |  78.3% |  88.3% |  83.0% | 94.0 |
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
| Home Care (Green)         |  91.1% |  92.6% |  91.8% | 121.0 |
| Clinic Visit (Yellow, <48h) |  23.1% |  25.0% |  24.0% | 12.0 |
| Emergency Care (Red, immediate) | 100.0% |  25.0% |  40.0% | 4.0 |
