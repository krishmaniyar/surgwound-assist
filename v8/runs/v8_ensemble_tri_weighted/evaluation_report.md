# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **57.35%**
- **Mean Accuracy**: 80.00%
- **Mean Macro-Precision**: 59.52%
- **Mean Macro-Recall**: 58.57%
- **Mean Weighted-F1**: 78.15%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **39.92%**
- **Exact Match Ratio**: 21.43%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  64.29% |  61.10% |  61.84% |  60.58% |  64.29% |  63.56% | N/A | N/A |
| healing_status   |  74.29% |  75.03% |  69.42% |  70.17% |  74.29% |  72.70% | N/A | N/A |
| closure_method   |  67.14% |  41.83% |  38.06% |  39.36% |  67.14% |  65.89% | N/A | N/A |
| exudate_type     |  90.00% |  28.79% |  39.68% |  32.56% |  90.00% |  87.46% | N/A | N/A |
| erythema         |  81.43% |  66.96% |  70.49% |  68.35% |  81.43% |  82.30% | N/A | N/A |
| edema            |  77.14% |  40.30% |  47.37% |  43.55% |  77.14% |  70.92% | N/A | N/A |
| infection_risk   |  85.71% |  62.12% |  41.67% |  44.23% |  85.71% |  82.33% | N/A | N/A |
| urgency_level    | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | N/A | N/A |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  76.5% |  92.9% |  83.9% | 14.0 |
| Patella                   |  50.0% |  38.5% |  43.5% | 13.0 |
| Ankle                     |  83.3% |  55.6% |  66.7% | 9.0 |
| Facial region             |  80.0% |  88.9% |  84.2% | 9.0 |
| Manus                     |  50.0% |  50.0% |  50.0% | 2.0 |
| Cervical region           |  33.3% |  50.0% |  40.0% | 2.0 |
| Other                     |  54.5% |  57.1% |  55.8% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  73.6% |  90.7% |  81.2% | 43.0 |
| Not Healed                |  76.5% |  48.1% |  59.1% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  60.0% |  50.0% |  54.5% | 18.0 |
| Sutures                   |  74.0% |  82.2% |  77.9% | 45.0 |
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
| Non-existent              |  91.1% |  86.4% |  88.7% | 59.0 |
| Existent                  |  42.9% |  54.5% |  48.0% | 11.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  80.6% |  94.7% |  87.1% | 57.0 |
| Existent                  |   0.0% |   0.0% |   0.0% | 13.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  86.4% | 100.0% |  92.7% | 57.0 |
| Medium                    | 100.0% |  25.0% |  40.0% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% | 100.0% | 100.0% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0 |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0 |
