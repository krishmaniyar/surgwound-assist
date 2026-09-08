# SurgWound Assist — Experiment v8_e2_full686_multiscale Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **44.47%**
- **Mean Accuracy**: 60.40%
- **Mean Macro-Precision**: 44.85%
- **Mean Macro-Recall**: 51.52%
- **Mean Weighted-F1**: 63.92%
- **Mean ROC-AUC**: 0.7587
- **Mean Cohen's Kappa**: 0.2796
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **34.71%**
- **Exact Match Ratio**: 4.38%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  56.20% |  53.69% |  64.11% |  54.01% |  56.20% |  56.21% | 0.8868 | 0.4887 |
| healing_status   |  69.34% |  68.67% |  69.30% |  68.74% |  69.34% |  69.60% | 0.7684 | 0.3770 |
| closure_method   |  39.42% |  32.06% |  28.60% |  26.98% |  39.42% |  45.75% | 0.5702 | 0.1908 |
| exudate_type     |  57.66% |  22.66% |  30.06% |  22.83% |  57.66% |  64.32% | 0.7752 | 0.1736 |
| erythema         |  64.23% |  50.82% |  59.01% |  52.09% |  64.23% |  66.35% | 0.7112 | 0.3281 |
| edema            |  48.91% |  41.50% |  44.28% |  40.19% |  48.91% |  52.59% | 0.6292 | 0.1486 |
| infection_risk   |  73.72% |  47.48% |  68.43% |  48.83% |  73.72% |  77.32% | 0.8724 | 0.2922 |
| urgency_level    |  73.72% |  41.88% |  48.39% |  42.06% |  73.72% |  79.21% | 0.8562 | 0.2377 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  62.5% |  78.9% |  69.8% | 19.0 |
| Patella                   |  18.8% | 100.0% |  31.6% | 3.0 |
| Ankle                     |  55.6% |  52.6% |  54.1% | 19.0 |
| Facial region             |  78.6% |  73.3% |  75.9% | 15.0 |
| Manus                     |  43.8% |  70.0% |  53.8% | 10.0 |
| Cervical region           |  40.0% |  50.0% |  44.4% | 4.0 |
| Other                     |  62.5% |  28.6% |  39.2% | 35.0 |
| Uncertain                 |  67.9% |  59.4% |  63.3% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  77.0% |  69.5% |  73.1% | 82.0 |
| Not Healed                |  60.3% |  69.1% |  64.4% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  26.9% |  36.8% |  31.1% | 19.0 |
| Sutures                   |  87.5% |  41.2% |  56.0% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |   4.0% |  25.0% |   6.9% | 4.0 |
| Uncertain                 |  41.9% |  40.0% |  40.9% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  91.4% |  67.9% |  77.9% | 109.0 |
| Serous                    |  12.5% |  12.5% |  12.5% | 8.0 |
| Sanguineous               |   6.2% |  25.0% |  10.0% | 4.0 |
| Purulent                  |  18.2% |  66.7% |  28.6% | 3.0 |
| Seropurulent              |   0.0% |   0.0% |   0.0% | 1.0 |
| Uncertain                 |   7.7% |   8.3% |   8.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  80.3% |  67.0% |  73.1% | 91.0 |
| Existent                  |  54.5% |  60.0% |  57.1% | 40.0 |
| Uncertain                 |  17.6% |  50.0% |  26.1% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  79.4% |  53.2% |  63.7% | 94.0 |
| Existent                  |  24.4% |  52.4% |  33.3% | 21.0 |
| Uncertain                 |  20.7% |  27.3% |  23.5% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  93.9% |  78.6% |  85.6% | 117.0 |
| Medium                    |  28.6% |  26.7% |  27.6% | 15.0 |
| High                      |  20.0% | 100.0% |  33.3% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  96.0% |  78.5% |  86.4% | 121.0 |
| Clinic Visit (Yellow, <48h) |  23.8% |  41.7% |  30.3% | 12.0 |
| Emergency Care (Red, immediate) |   5.9% |  25.0% |   9.5% | 4.0 |
