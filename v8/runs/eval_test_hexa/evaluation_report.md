# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **54.23%**
- **Mean Accuracy**: 70.26%
- **Mean Macro-Precision**: 52.88%
- **Mean Macro-Recall**: 61.64%
- **Mean Weighted-F1**: 70.95%
- **Mean ROC-AUC**: 0.8288
- **Mean Cohen's Kappa**: 0.3924
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **43.99%**
- **Exact Match Ratio**: 20.44%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  64.96% |  66.45% |  74.85% |  66.35% |  64.96% |  66.41% | 0.9437 | 0.5869 |
| healing_status   |  75.18% |  74.18% |  74.18% |  74.18% |  75.18% |  75.18% | 0.8159 | 0.4836 |
| closure_method   |  43.07% |  31.65% |  28.70% |  28.63% |  43.07% |  47.36% | 0.7324 | 0.2158 |
| exudate_type     |  70.80% |  34.76% |  54.04% |  37.03% |  70.80% |  70.99% | 0.8232 | 0.2465 |
| erythema         |  69.34% |  56.17% |  64.84% |  58.12% |  69.34% |  70.85% | 0.7844 | 0.4318 |
| edema            |  70.07% |  49.74% |  54.93% |  51.32% |  70.07% |  66.60% | 0.7330 | 0.3343 |
| infection_risk   |  82.48% |  55.11% |  69.34% |  58.97% |  82.48% |  83.80% | 0.9201 | 0.4248 |
| urgency_level    |  86.13% |  54.96% |  72.25% |  59.23% |  86.13% |  86.44% | 0.8774 | 0.4153 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  60.9% |  73.7% |  66.7% | 19.0 |
| Patella                   |  17.6% | 100.0% |  30.0% | 3.0 |
| Ankle                     |  86.7% |  68.4% |  76.5% | 19.0 |
| Facial region             |  92.3% |  80.0% |  85.7% | 15.0 |
| Manus                     |  83.3% | 100.0% |  90.9% | 10.0 |
| Cervical region           |  60.0% |  75.0% |  66.7% | 4.0 |
| Other                     |  65.4% |  48.6% |  55.7% | 35.0 |
| Uncertain                 |  65.4% |  53.1% |  58.6% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  79.3% |  79.3% |  79.3% | 82.0 |
| Not Healed                |  69.1% |  69.1% |  69.1% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  37.9% |  57.9% |  45.8% | 19.0 |
| Sutures                   |  77.8% |  41.2% |  53.8% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |   0.0% |   0.0% |   0.0% | 4.0 |
| Uncertain                 |  42.6% |  44.4% |  43.5% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  86.5% |  82.6% |  84.5% | 109.0 |
| Serous                    |  20.0% |  25.0% |  22.2% | 8.0 |
| Sanguineous               |  66.7% |  50.0% |  57.1% | 4.0 |
| Purulent                  |  15.4% |  66.7% |  25.0% | 3.0 |
| Seropurulent              |  20.0% | 100.0% |  33.3% | 1.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  87.1% |  67.0% |  75.8% | 91.0 |
| Existent                  |  56.4% |  77.5% |  65.3% | 40.0 |
| Uncertain                 |  25.0% |  50.0% |  33.3% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  77.5% |  84.0% |  80.6% | 94.0 |
| Existent                  |  59.3% |  76.2% |  66.7% | 21.0 |
| Uncertain                 |  12.5% |   4.5% |   6.7% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  94.5% |  88.0% |  91.2% | 117.0 |
| Medium                    |  37.5% |  40.0% |  38.7% | 15.0 |
| High                      |  33.3% |  80.0% |  47.1% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  94.9% |  91.7% |  93.3% | 121.0 |
| Clinic Visit (Yellow, <48h) |  30.0% |  25.0% |  27.3% | 12.0 |
| Emergency Care (Red, immediate) |  40.0% | 100.0% |  57.1% | 4.0 |
