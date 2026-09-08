# SurgWound Assist — Experiment v8_e6_mixup_smoothing_s7 Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **24.83%**
- **Mean Accuracy**: 25.36%
- **Mean Macro-Precision**: 36.08%
- **Mean Macro-Recall**: 42.37%
- **Mean Weighted-F1**: 25.93%
- **Mean ROC-AUC**: 0.6979
- **Mean Cohen's Kappa**: 0.1321
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **15.35%**
- **Exact Match Ratio**: 0.00%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  52.55% |  51.82% |  59.68% |  51.10% |  52.55% |  54.26% | 0.9111 | 0.4430 |
| healing_status   |  63.50% |  62.79% |  63.23% |  62.79% |  63.50% |  63.81% | 0.7268 | 0.2583 |
| closure_method   |   3.65% |  27.69% |  27.55% |   6.44% |   3.65% |   4.23% | 0.6174 | 0.0167 |
| exudate_type     |   1.46% |   1.83% |  20.83% |   2.71% |   1.46% |   0.43% | 0.6178 | 0.0027 |
| erythema         |  18.25% |  60.07% |  44.50% |  21.44% |  18.25% |  23.69% | 0.6998 | 0.0806 |
| edema            |  55.47% |  48.86% |  55.96% |  48.75% |  55.47% |  57.74% | 0.7236 | 0.2535 |
| infection_risk   |   5.11% |  34.57% |  33.90% |   3.50% |   5.11% |   3.13% | 0.6969 | 0.0028 |
| urgency_level    |   2.92% |   0.99% |  33.33% |   1.92% |   2.92% |   0.17% | 0.5897 | -0.0009 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  66.7% |  52.6% |  58.8% | 19.0 |
| Patella                   |  16.7% |  66.7% |  26.7% | 3.0 |
| Ankle                     |  76.9% |  52.6% |  62.5% | 19.0 |
| Facial region             |  78.6% |  73.3% |  75.9% | 15.0 |
| Manus                     |  41.2% |  70.0% |  51.9% | 10.0 |
| Cervical region           |  23.1% |  75.0% |  35.3% | 4.0 |
| Other                     |  44.8% |  37.1% |  40.6% | 35.0 |
| Uncertain                 |  66.7% |  50.0% |  57.1% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  71.6% |  64.6% |  67.9% | 82.0 |
| Not Healed                |  54.0% |  61.8% |  57.6% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 | 100.0% |  10.5% |  19.0% | 19.0 |
| Sutures                   |   0.0% |   0.0% |   0.0% | 68.0 |
| Staples                   |   0.9% | 100.0% |   1.8% | 1.0 |
| Adhesives                 |   4.2% |  25.0% |   7.1% | 4.0 |
| Uncertain                 |  33.3% |   2.2% |   4.2% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |   0.0% |   0.0% |   0.0% | 109.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 8.0 |
| Sanguineous               |  10.0% |  25.0% |  14.3% | 4.0 |
| Purulent                  |   0.0% |   0.0% |   0.0% | 3.0 |
| Seropurulent              |   1.0% | 100.0% |   2.0% | 1.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              | 100.0% |  11.0% |  19.8% | 91.0 |
| Existent                  |  75.0% |  22.5% |  34.6% | 40.0 |
| Uncertain                 |   5.2% | 100.0% |   9.9% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  81.2% |  55.3% |  65.8% | 94.0 |
| Existent                  |  33.3% |  76.2% |  46.4% | 21.0 |
| Uncertain                 |  32.0% |  36.4% |  34.0% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       | 100.0% |   1.7% |   3.4% | 117.0 |
| Medium                    |   0.0% |   0.0% |   0.0% | 15.0 |
| High                      |   3.7% | 100.0% |   7.1% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |   0.0% |   0.0% |   0.0% | 121.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 12.0 |
| Emergency Care (Red, immediate) |   3.0% | 100.0% |   5.8% | 4.0 |
