# SurgWound Assist — Experiment v8_e4_full686_balanced_tau12 Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **43.72%**
- **Mean Accuracy**: 59.67%
- **Mean Macro-Precision**: 44.57%
- **Mean Macro-Recall**: 52.84%
- **Mean Weighted-F1**: 63.20%
- **Mean ROC-AUC**: 0.7584
- **Mean Cohen's Kappa**: 0.2670
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **36.13%**
- **Exact Match Ratio**: 3.65%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  45.99% |  51.55% |  57.48% |  46.06% |  45.99% |  46.78% | 0.8788 | 0.3910 |
| healing_status   |  69.34% |  68.20% |  68.40% |  68.29% |  69.34% |  69.43% | 0.7616 | 0.3659 |
| closure_method   |  48.18% |  33.70% |  33.80% |  31.46% |  48.18% |  52.89% | 0.6010 | 0.2713 |
| exudate_type     |  56.93% |  21.04% |  39.09% |  21.03% |  56.93% |  63.51% | 0.7477 | 0.1659 |
| erythema         |  62.77% |  50.97% |  56.41% |  49.37% |  62.77% |  66.34% | 0.7301 | 0.3147 |
| edema            |  50.36% |  39.53% |  42.67% |  39.25% |  50.36% |  52.85% | 0.6467 | 0.1222 |
| infection_risk   |  73.72% |  49.26% |  72.31% |  52.80% |  73.72% |  77.05% | 0.8652 | 0.2974 |
| urgency_level    |  70.07% |  42.32% |  52.57% |  41.55% |  70.07% |  76.75% | 0.8356 | 0.2074 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  56.0% |  73.7% |  63.6% | 19.0 |
| Patella                   |   8.3% | 100.0% |  15.4% | 3.0 |
| Ankle                     |  60.0% |  47.4% |  52.9% | 19.0 |
| Facial region             |  91.7% |  73.3% |  81.5% | 15.0 |
| Manus                     |  46.2% |  60.0% |  52.2% | 10.0 |
| Cervical region           |  25.0% |  50.0% |  33.3% | 4.0 |
| Other                     |  60.0% |   8.6% |  15.0% | 35.0 |
| Uncertain                 |  65.2% |  46.9% |  54.5% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  75.0% |  73.2% |  74.1% | 82.0 |
| Not Healed                |  61.4% |  63.6% |  62.5% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  25.7% |  47.4% |  33.3% | 19.0 |
| Sutures                   |  88.1% |  54.4% |  67.3% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |   8.3% |  25.0% |  12.5% | 4.0 |
| Uncertain                 |  46.3% |  42.2% |  44.2% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  91.4% |  67.9% |  77.9% | 109.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 8.0 |
| Sanguineous               |   4.3% |  25.0% |   7.4% | 4.0 |
| Purulent                  |  14.3% |  33.3% |  20.0% | 3.0 |
| Seropurulent              |   6.2% | 100.0% |  11.8% | 1.0 |
| Uncertain                 |  10.0% |   8.3% |   9.1% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  80.8% |  69.2% |  74.6% | 91.0 |
| Existent                  |  60.6% |  50.0% |  54.8% | 40.0 |
| Uncertain                 |  11.5% |  50.0% |  18.8% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  75.0% |  57.4% |  65.1% | 94.0 |
| Existent                  |  26.2% |  52.4% |  34.9% | 21.0 |
| Uncertain                 |  17.4% |  18.2% |  17.8% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  92.8% |  76.9% |  84.1% | 117.0 |
| Medium                    |  30.0% |  40.0% |  34.3% | 15.0 |
| High                      |  25.0% | 100.0% |  40.0% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  95.7% |  74.4% |  83.7% | 121.0 |
| Clinic Visit (Yellow, <48h) |  23.5% |  33.3% |  27.6% | 12.0 |
| Emergency Care (Red, immediate) |   7.7% |  50.0% |  13.3% | 4.0 |
