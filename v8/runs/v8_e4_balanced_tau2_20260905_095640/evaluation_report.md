# SurgWound Assist — Experiment v8_e4_balanced_tau2 Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **35.74%**
- **Mean Accuracy**: 55.18%
- **Mean Macro-Precision**: 40.90%
- **Mean Macro-Recall**: 36.95%
- **Mean Weighted-F1**: 61.60%
- **Mean ROC-AUC**: 0.7942
- **Mean Cohen's Kappa**: 0.2421
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **30.04%**
- **Exact Match Ratio**: 0.00%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  50.00% |  44.28% |  45.49% |  41.63% |  50.00% |  51.29% | 0.8603 | 0.4019 |
| healing_status   |  74.29% |  72.89% |  72.18% |  72.47% |  74.29% |  74.08% | 0.8269 | 0.4498 |
| closure_method   |  48.57% |  30.59% |  34.89% |  29.02% |  48.57% |  54.35% | 0.6554 | 0.2205 |
| exudate_type     |  47.14% |  19.05% |  16.80% |  14.93% |  47.14% |  61.27% | 0.8437 | 0.0806 |
| erythema         |  68.57% |  42.41% |  46.84% |  41.22% |  68.57% |  73.75% | 0.8706 | 0.2827 |
| edema            |  65.71% |  41.56% |  40.76% |  39.60% |  65.71% |  71.58% | 0.7301 | 0.2432 |
| infection_risk   |  68.57% |  43.06% |  32.46% |  36.61% |  68.57% |  75.16% | 0.7724 | 0.2582 |
| urgency_level    |  18.57% |  33.33% |   6.19% |  10.44% |  18.57% |  31.33% | N/A | 0.0000 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  78.6% |  78.6% |  78.6% | 14.0 |
| Patella                   |  42.1% |  61.5% |  50.0% | 13.0 |
| Ankle                     |  80.0% |  44.4% |  57.1% | 9.0 |
| Facial region             |  71.4% |  55.6% |  62.5% | 9.0 |
| Manus                     |  16.7% |  50.0% |  25.0% | 2.0 |
| Cervical region           |  20.0% |  50.0% |  28.6% | 2.0 |
| Other                     |  45.5% |  23.8% |  31.2% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 (0 samples) |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  77.8% |  81.4% |  79.5% | 43.0 |
| Not Healed                |  68.0% |  63.0% |  65.4% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  55.6% |  55.6% |  55.6% | 18.0 |
| Sutures                   |  78.6% |  48.9% |  60.3% | 45.0 |
| Staples                   |  11.1% |  50.0% |  18.2% | 2.0 |
| Adhesives                 |   7.7% |  20.0% |  11.1% | 5.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 (0 samples) |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              | 100.0% |  50.8% |  67.4% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |  14.3% |  50.0% |  22.2% | 2.0 |
| Purulent                  |   0.0% |   0.0% |   0.0% | 1.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 2.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 (0 samples) |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  95.2% |  67.8% |  79.2% | 59.0 |
| Existent                  |  32.0% |  72.7% |  44.4% | 11.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 (0 samples) |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  92.9% |  68.4% |  78.8% | 57.0 |
| Existent                  |  31.8% |  53.8% |  40.0% | 13.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 (0 samples) |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  95.8% |  80.7% |  87.6% | 57.0 |
| Medium                    |  33.3% |  16.7% |  22.2% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% |  18.6% |  31.3% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0 (0 samples) |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0 (0 samples) |
