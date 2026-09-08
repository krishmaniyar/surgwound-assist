# SurgWound Assist — Experiment v8_e5_full686_adaptive_multiscale Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **43.04%**
- **Mean Accuracy**: 58.39%
- **Mean Macro-Precision**: 44.42%
- **Mean Macro-Recall**: 49.58%
- **Mean Weighted-F1**: 62.40%
- **Mean ROC-AUC**: 0.7568
- **Mean Cohen's Kappa**: 0.2568
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **32.29%**
- **Exact Match Ratio**: 5.11%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  54.74% |  52.69% |  57.96% |  53.60% |  54.74% |  55.51% | 0.9178 | 0.4597 |
| healing_status   |  72.26% |  71.17% |  70.24% |  70.55% |  72.26% |  71.95% | 0.7787 | 0.4123 |
| closure_method   |  31.39% |  29.98% |  23.40% |  22.73% |  31.39% |  38.71% | 0.6553 | 0.1257 |
| exudate_type     |  44.53% |  20.78% |  19.98% |  16.38% |  44.53% |  55.46% | 0.6511 | 0.1086 |
| erythema         |  67.15% |  51.01% |  54.82% |  51.43% |  67.15% |  68.99% | 0.7310 | 0.3555 |
| edema            |  60.58% |  48.18% |  51.19% |  49.29% |  60.58% |  61.34% | 0.6628 | 0.2287 |
| infection_risk   |  69.34% |  40.90% |  56.47% |  40.74% |  69.34% |  73.54% | 0.8313 | 0.1896 |
| urgency_level    |  67.15% |  40.67% |  62.58% |  39.58% |  67.15% |  73.69% | 0.8267 | 0.1747 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  45.0% |  47.4% |  46.2% | 19.0 |
| Patella                   |  12.5% |  33.3% |  18.2% | 3.0 |
| Ankle                     |  76.5% |  68.4% |  72.2% | 19.0 |
| Facial region             |  83.3% |  66.7% |  74.1% | 15.0 |
| Manus                     |  61.5% |  80.0% |  69.6% | 10.0 |
| Cervical region           |  37.5% |  75.0% |  50.0% | 4.0 |
| Other                     |  50.0% |  42.9% |  46.2% | 35.0 |
| Uncertain                 |  55.2% |  50.0% |  52.5% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  75.0% |  80.5% |  77.6% | 82.0 |
| Not Healed                |  67.3% |  60.0% |  63.5% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  25.0% |  26.3% |  25.6% | 19.0 |
| Sutures                   |  81.5% |  32.4% |  46.3% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |   2.9% |  25.0% |   5.1% | 4.0 |
| Uncertain                 |  40.5% |  33.3% |  36.6% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  93.5% |  53.2% |  67.8% | 109.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 8.0 |
| Sanguineous               |   4.0% |  25.0% |   6.9% | 4.0 |
| Purulent                  |   7.1% |  33.3% |  11.8% | 3.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 1.0 |
| Uncertain                 |  20.0% |   8.3% |  11.8% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  80.7% |  73.6% |  77.0% | 91.0 |
| Existent                  |  59.0% |  57.5% |  58.2% | 40.0 |
| Uncertain                 |  13.3% |  33.3% |  19.0% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  75.6% |  69.1% |  72.2% | 94.0 |
| Existent                  |  42.9% |  57.1% |  49.0% | 21.0 |
| Uncertain                 |  26.1% |  27.3% |  26.7% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  91.8% |  76.1% |  83.2% | 117.0 |
| Medium                    |  16.7% |  13.3% |  14.8% | 15.0 |
| High                      |  14.3% |  80.0% |  24.2% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  94.5% |  71.1% |  81.1% | 121.0 |
| Clinic Visit (Yellow, <48h) |  15.4% |  16.7% |  16.0% | 12.0 |
| Emergency Care (Red, immediate) |  12.1% | 100.0% |  21.6% | 4.0 |
