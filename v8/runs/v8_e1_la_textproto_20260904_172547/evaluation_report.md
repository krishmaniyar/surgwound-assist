# SurgWound Assist — Experiment v8_e1_la_textproto Final Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **54.44%**
- **Mean Accuracy**: 78.04%
- **Mean Macro-Precision**: 55.66%
- **Mean Macro-Recall**: 54.88%
- **Mean Weighted-F1**: 76.37%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **34.16%**
- **Exact Match Ratio**: 21.43%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  65.71% |  66.71% |  63.02% |  62.73% |  65.71% |  65.70% | N/A | 0.5752 |
| healing_status   |  70.00% |  68.50% |  65.93% |  66.37% |  70.00% |  68.89% | 0.7873 | 0.3348 |
| closure_method   |  62.86% |  36.61% |  35.56% |  35.94% |  62.86% |  61.56% | N/A | 0.2369 |
| exudate_type     |  88.57% |  18.24% |  19.68% |  18.93% |  88.57% |  85.19% | N/A | 0.0865 |
| erythema         |  82.86% |  68.69% |  71.34% |  69.83% |  82.86% |  83.42% | N/A | 0.3974 |
| edema            |  74.29% |  47.62% |  48.58% |  47.50% |  74.29% |  71.07% | N/A | -0.0345 |
| infection_risk   |  80.00% |  38.89% |  34.94% |  34.25% |  80.00% |  75.11% | N/A | 0.1099 |
| urgency_level    | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | N/A | N/A |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  66.7% |  85.7% |  75.0% | 14.0 |
| Patella                   |  63.6% |  53.8% |  58.3% | 13.0 |
| Ankle                     |  75.0% |  66.7% |  70.6% | 9.0 |
| Facial region             |  70.0% |  77.8% |  73.7% | 9.0 |
| Manus                     | 100.0% |  50.0% |  66.7% | 2.0 |
| Cervical region           |  25.0% |  50.0% |  33.3% | 2.0 |
| Other                     |  66.7% |  57.1% |  61.5% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  72.0% |  83.7% |  77.4% | 43.0 |
| Not Healed                |  65.0% |  48.1% |  55.3% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  50.0% |  44.4% |  47.1% | 18.0 |
| Sutures                   |  71.4% |  77.8% |  74.5% | 45.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 2.0 |
| Adhesives                 |  25.0% |  20.0% |  22.2% | 5.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  91.2% |  98.4% |  94.7% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 2.0 |
| Purulent                  |   0.0% |   0.0% |   0.0% | 1.0 |
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
| Non-existent              |  81.0% |  89.5% |  85.0% | 57.0 |
| Existent                  |  14.3% |   7.7% |  10.0% | 13.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  83.3% |  96.5% |  89.4% | 57.0 |
| Medium                    |  33.3% |   8.3% |  13.3% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% | 100.0% | 100.0% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0 |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0 |
