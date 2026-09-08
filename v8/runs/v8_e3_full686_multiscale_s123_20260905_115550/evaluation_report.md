# SurgWound Assist — Experiment v8_e3_full686_multiscale_s123 Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **43.25%**
- **Mean Accuracy**: 62.59%
- **Mean Macro-Precision**: 43.69%
- **Mean Macro-Recall**: 48.24%
- **Mean Weighted-F1**: 64.74%
- **Mean ROC-AUC**: 0.7330
- **Mean Cohen's Kappa**: 0.2697
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **32.87%**
- **Exact Match Ratio**: 5.84%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  55.47% |  55.72% |  50.59% |  49.11% |  55.47% |  54.67% | 0.8657 | 0.4656 |
| healing_status   |  66.42% |  64.88% |  64.47% |  64.61% |  66.42% |  66.19% | 0.7303 | 0.2929 |
| closure_method   |  53.28% |  28.43% |  29.02% |  28.51% |  53.28% |  53.86% | 0.5103 | 0.2679 |
| exudate_type     |  62.77% |  18.39% |  15.62% |  16.89% |  62.77% |  67.76% | 0.6952 | 0.1747 |
| erythema         |  66.42% |  51.44% |  57.77% |  53.19% |  66.42% |  67.18% | 0.7093 | 0.3194 |
| edema            |  52.55% |  43.61% |  47.14% |  43.70% |  52.55% |  55.41% | 0.6492 | 0.1718 |
| infection_risk   |  72.26% |  41.89% |  57.61% |  42.40% |  72.26% |  75.80% | 0.8324 | 0.2303 |
| urgency_level    |  71.53% |  45.16% |  63.68% |  47.61% |  71.53% |  77.06% | 0.8717 | 0.2349 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  56.0% |  73.7% |  63.6% | 19.0 |
| Patella                   |   0.0% |   0.0% |   0.0% | 3.0 |
| Ankle                     |  45.5% |  52.6% |  48.8% | 19.0 |
| Facial region             |  92.3% |  80.0% |  85.7% | 15.0 |
| Manus                     |  40.0% |  80.0% |  53.3% | 10.0 |
| Cervical region           | 100.0% |  25.0% |  40.0% | 4.0 |
| Other                     |  52.0% |  37.1% |  43.3% | 35.0 |
| Uncertain                 |  60.0% |  56.2% |  58.1% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  70.9% |  74.4% |  72.6% | 82.0 |
| Not Healed                |  58.8% |  54.5% |  56.6% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  20.8% |  26.3% |  23.3% | 19.0 |
| Sutures                   |  74.1% |  63.2% |  68.3% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |   0.0% |   0.0% |   0.0% | 4.0 |
| Uncertain                 |  47.2% |  55.6% |  51.0% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  90.3% |  77.1% |  83.2% | 109.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 8.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 4.0 |
| Purulent                  |   0.0% |   0.0% |   0.0% | 3.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 1.0 |
| Uncertain                 |  20.0% |  16.7% |  18.2% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  79.3% |  75.8% |  77.5% | 91.0 |
| Existent                  |  50.0% |  47.5% |  48.7% | 40.0 |
| Uncertain                 |  25.0% |  50.0% |  33.3% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  77.1% |  57.4% |  65.9% | 94.0 |
| Existent                  |  27.0% |  47.6% |  34.5% | 21.0 |
| Uncertain                 |  26.7% |  36.4% |  30.8% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  93.0% |  79.5% |  85.7% | 117.0 |
| Medium                    |  16.7% |  13.3% |  14.8% | 15.0 |
| High                      |  16.0% |  80.0% |  26.7% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  95.7% |  74.4% |  83.7% | 121.0 |
| Clinic Visit (Yellow, <48h) |  16.7% |  41.7% |  23.8% | 12.0 |
| Emergency Care (Red, immediate) |  23.1% |  75.0% |  35.3% | 4.0 |
