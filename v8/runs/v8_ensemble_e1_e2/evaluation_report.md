# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **58.73%**
- **Mean Accuracy**: 80.36%
- **Mean Macro-Precision**: 61.74%
- **Mean Macro-Recall**: 59.65%
- **Mean Weighted-F1**: 78.77%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **41.25%**
- **Exact Match Ratio**: 20.00%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  67.14% |  68.46% |  63.13% |  63.84% |  67.14% |  66.48% | N/A | N/A |
| healing_status   |  74.29% |  74.10% |  70.11% |  70.86% |  74.29% |  73.14% | N/A | N/A |
| closure_method   |  67.14% |  41.83% |  38.06% |  39.36% |  67.14% |  65.89% | N/A | N/A |
| exudate_type     |  90.00% |  28.51% |  39.68% |  32.41% |  90.00% |  86.80% | N/A | N/A |
| erythema         |  81.43% |  68.17% |  74.19% |  70.17% |  81.43% |  82.74% | N/A | N/A |
| edema            |  77.14% |  50.77% |  50.34% |  49.00% |  77.14% |  72.81% | N/A | N/A |
| infection_risk   |  85.71% |  62.12% |  41.67% |  44.23% |  85.71% |  82.33% | N/A | N/A |
| urgency_level    | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | N/A | N/A |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  76.5% |  92.9% |  83.9% | 14.0 |
| Patella                   |  63.6% |  53.8% |  58.3% | 13.0 |
| Ankle                     |  66.7% |  44.4% |  53.3% | 9.0 |
| Facial region             |  80.0% |  88.9% |  84.2% | 9.0 |
| Manus                     | 100.0% |  50.0% |  66.7% | 2.0 |
| Cervical region           |  33.3% |  50.0% |  40.0% | 2.0 |
| Other                     |  59.1% |  61.9% |  60.5% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  74.5% |  88.4% |  80.9% | 43.0 |
| Not Healed                |  73.7% |  51.9% |  60.9% | 27.0 |

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
| Non-existent              |  92.5% |  98.4% |  95.4% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 2.0 |
| Purulent                  |  50.0% | 100.0% |  66.7% | 1.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 2.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  92.6% |  84.7% |  88.5% | 59.0 |
| Existent                  |  43.8% |  63.6% |  51.9% | 11.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  81.5% |  93.0% |  86.9% | 57.0 |
| Existent                  |  20.0% |   7.7% |  11.1% | 13.0 |
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
