# SurgWound Assist — Experiment v8_e2_multiscale Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **57.63%**
- **Mean Accuracy**: 78.75%
- **Mean Macro-Precision**: 58.72%
- **Mean Macro-Recall**: 58.68%
- **Mean Weighted-F1**: 77.60%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **38.84%**
- **Exact Match Ratio**: 18.57%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  60.00% |  59.50% |  57.72% |  57.01% |  60.00% |  58.84% | N/A | 0.4924 |
| healing_status   |  75.71% |  74.55% |  73.34% |  73.78% |  75.71% |  75.41% | 0.8441 | 0.4767 |
| closure_method   |  65.71% |  44.87% |  40.28% |  41.85% |  65.71% |  64.22% | N/A | 0.2759 |
| exudate_type     |  85.71% |  21.16% |  32.28% |  23.94% |  85.71% |  85.00% | N/A | 0.2408 |
| erythema         |  85.71% |  73.41% |  76.73% |  74.86% |  85.71% |  86.19% | N/A | 0.4978 |
| edema            |  74.29% |  47.62% |  48.58% |  47.50% |  74.29% |  71.07% | N/A | -0.0345 |
| infection_risk   |  82.86% |  48.65% |  40.50% |  42.07% |  82.86% |  80.08% | N/A | 0.2947 |
| urgency_level    | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | N/A | N/A |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  75.0% |  85.7% |  80.0% | 14.0 |
| Patella                   |  42.9% |  23.1% |  30.0% | 13.0 |
| Ankle                     |  80.0% |  44.4% |  57.1% | 9.0 |
| Facial region             |  88.9% |  88.9% |  88.9% | 9.0 |
| Manus                     |  50.0% |  50.0% |  50.0% | 2.0 |
| Cervical region           |  33.3% |  50.0% |  40.0% | 2.0 |
| Other                     |  46.4% |  61.9% |  53.1% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  78.3% |  83.7% |  80.9% | 43.0 |
| Not Healed                |  70.8% |  63.0% |  66.7% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  58.3% |  38.9% |  46.7% | 18.0 |
| Sutures                   |  71.2% |  82.2% |  76.3% | 45.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 2.0 |
| Adhesives                 |  50.0% |  40.0% |  44.4% | 5.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  93.7% |  93.7% |  93.7% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 2.0 |
| Purulent                  |  33.3% | 100.0% |  50.0% | 1.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 2.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  93.0% |  89.8% |  91.4% | 59.0 |
| Existent                  |  53.8% |  63.6% |  58.3% | 11.0 |
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
| Low                       |  85.9% |  96.5% |  90.9% | 57.0 |
| Medium                    |  60.0% |  25.0% |  35.3% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% | 100.0% | 100.0% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0 |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0 |
