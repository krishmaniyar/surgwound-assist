# SurgWound Assist — Experiment v8_multiscale_pilot Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **33.97%**
- **Mean Accuracy**: 65.54%
- **Mean Macro-Precision**: 34.08%
- **Mean Macro-Recall**: 35.74%
- **Mean Weighted-F1**: 64.24%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **30.56%**
- **Exact Match Ratio**: 2.86%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  24.29% |   8.17% |  12.80% |   9.55% |  24.29% |  19.09% | N/A | 0.0586 |
| healing_status   |  58.57% |  56.03% |  55.94% |  55.97% |  58.57% |  58.42% | 0.6753 | 0.1197 |
| closure_method   |  62.86% |  12.75% |  19.56% |  15.44% |  62.86% |  49.62% | N/A | -0.0139 |
| exudate_type     |  78.57% |  20.53% |  27.14% |  21.34% |  78.57% |  80.19% | N/A | 0.0964 |
| erythema         |  71.43% |  35.63% |  35.64% |  35.49% |  71.43% |  73.27% | N/A | 0.0673 |
| edema            |  77.14% |  55.56% |  53.31% |  53.33% |  77.14% |  74.29% | N/A | 0.0805 |
| infection_risk   |  57.14% |  33.95% |  34.36% |  32.12% |  57.14% |  61.97% | N/A | 0.0371 |
| urgency_level    |  94.29% |  50.00% |  47.14% |  48.53% |  94.29% |  97.06% | N/A | 0.0000 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  27.3% |  64.3% |  38.3% | 14.0 |
| Patella                   |   0.0% |   0.0% |   0.0% | 13.0 |
| Ankle                     |   0.0% |   0.0% |   0.0% | 9.0 |
| Facial region             |   0.0% |   0.0% |   0.0% | 9.0 |
| Manus                     |   0.0% |   0.0% |   0.0% | 2.0 |
| Cervical region           |   0.0% |   0.0% |   0.0% | 2.0 |
| Other                     |  38.1% |  38.1% |  38.1% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  65.9% |  67.4% |  66.7% | 43.0 |
| Not Healed                |  46.2% |  44.4% |  45.3% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |   0.0% |   0.0% |   0.0% | 18.0 |
| Sutures                   |  63.8% |  97.8% |  77.2% | 45.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 2.0 |
| Adhesives                 |   0.0% |   0.0% |   0.0% | 5.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  91.5% |  85.7% |  88.5% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 2.0 |
| Purulent                  |   0.0% |   0.0% |   0.0% | 1.0 |
| Seropurulent              |  11.1% |  50.0% |  18.2% | 2.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  85.5% |  79.7% |  82.5% | 59.0 |
| Existent                  |  21.4% |  27.3% |  24.0% | 11.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  82.5% |  91.2% |  86.7% | 57.0 |
| Existent                  |  28.6% |  15.4% |  20.0% | 13.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  83.3% |  61.4% |  70.7% | 57.0 |
| Medium                    |  18.5% |  41.7% |  25.6% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% |  94.3% |  97.1% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0.0 |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0 |
