# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **57.09%**
- **Mean Accuracy**: 79.29%
- **Mean Macro-Precision**: 60.60%
- **Mean Macro-Recall**: 57.95%
- **Mean Weighted-F1**: 77.72%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **38.57%**
- **Exact Match Ratio**: 17.14%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  64.29% |  69.17% |  61.50% |  62.41% |  64.29% |  64.28% | N/A | N/A |
| healing_status   |  74.29% |  75.03% |  69.42% |  70.17% |  74.29% |  72.70% | N/A | N/A |
| closure_method   |  67.14% |  41.79% |  38.89% |  39.89% |  67.14% |  66.25% | N/A | N/A |
| exudate_type     |  90.00% |  28.79% |  39.68% |  32.56% |  90.00% |  87.46% | N/A | N/A |
| erythema         |  82.86% |  68.69% |  71.34% |  69.83% |  82.86% |  83.42% | N/A | N/A |
| edema            |  71.43% |  39.68% |  43.86% |  41.67% |  71.43% |  67.86% | N/A | N/A |
| infection_risk   |  84.29% |  61.69% |  38.89% |  40.17% |  84.29% |  79.76% | N/A | N/A |
| urgency_level    | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | N/A | N/A |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  75.0% |  85.7% |  80.0% | 14.0 |
| Patella                   |  50.0% |  38.5% |  43.5% | 13.0 |
| Ankle                     | 100.0% |  55.6% |  71.4% | 9.0 |
| Facial region             |  80.0% |  88.9% |  84.2% | 9.0 |
| Manus                     | 100.0% |  50.0% |  66.7% | 2.0 |
| Cervical region           |  25.0% |  50.0% |  33.3% | 2.0 |
| Other                     |  54.2% |  61.9% |  57.8% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  73.6% |  90.7% |  81.2% | 43.0 |
| Not Healed                |  76.5% |  48.1% |  59.1% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  58.8% |  55.6% |  57.1% | 18.0 |
| Sutures                   |  75.0% |  80.0% |  77.4% | 45.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 2.0 |
| Adhesives                 |  33.3% |  20.0% |  25.0% | 5.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  93.9% |  98.4% |  96.1% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 2.0 |
| Purulent                  |  50.0% | 100.0% |  66.7% | 1.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 2.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  91.2% |  88.1% |  89.7% | 59.0 |
| Existent                  |  46.2% |  54.5% |  50.0% | 11.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  79.4% |  87.7% |  83.3% | 57.0 |
| Existent                  |   0.0% |   0.0% |   0.0% | 13.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  85.1% | 100.0% |  91.9% | 57.0 |
| Medium                    | 100.0% |  16.7% |  28.6% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% | 100.0% | 100.0% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0 |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0 |
