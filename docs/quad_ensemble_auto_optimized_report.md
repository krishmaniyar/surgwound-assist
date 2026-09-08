# SurgWound Assist — SurgWound Assist v8 Deep Ensemble

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **52.62%**
- **Mean Accuracy**: 73.08%
- **Mean Macro-Precision**: 52.79%
- **Mean Macro-Recall**: 58.34%
- **Mean Weighted-F1**: 70.26%
- **Mean ROC-AUC**: 0.8299
- **Mean Cohen's Kappa**: 0.4117
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **45.34%**
- **Exact Match Ratio**: 29.93%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  60.58% |  54.23% |  74.12% |  59.13% |  60.58% |  54.26% | 0.9424 | 0.5394 |
| healing_status   |  77.37% |  76.66% |  75.71% |  76.07% |  77.37% |  77.17% | 0.8635 | 0.5220 |
| closure_method   |  54.74% |  30.70% |  38.14% |  31.67% |  54.74% |  45.72% | 0.7668 | 0.2974 |
| exudate_type     |  75.91% |  38.41% |  59.12% |  44.65% |  75.91% |  74.08% | 0.8284 | 0.3208 |
| erythema         |  77.37% |  49.65% |  51.44% |  50.51% |  77.37% |  75.53% | 0.7479 | 0.4909 |
| edema            |  72.26% |  43.45% |  56.06% |  48.60% |  72.26% |  66.48% | 0.7452 | 0.3728 |
| infection_risk   |  83.94% |  56.78% |  60.46% |  56.45% |  83.94% |  85.19% | 0.9328 | 0.4830 |
| urgency_level    |  82.48% |  72.41% |  51.70% |  53.85% |  82.48% |  83.66% | 0.8123 | 0.2675 |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  52.8% | 100.0% |  69.1% | 19.0 |
| Patella                   |  21.4% | 100.0% |  35.3% | 3.0 |
| Ankle                     |  86.7% |  68.4% |  76.5% | 19.0 |
| Facial region             |  86.7% |  86.7% |  86.7% | 15.0 |
| Manus                     |  90.9% | 100.0% |  95.2% | 10.0 |
| Cervical region           |  37.5% |  75.0% |  50.0% | 4.0 |
| Other                     |  57.9% |  62.9% |  60.3% | 35.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  79.3% |  84.1% |  81.7% | 82.0 |
| Not Healed                |  74.0% |  67.3% |  70.5% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  34.9% |  78.9% |  48.4% | 19.0 |
| Sutures                   |  68.6% |  86.8% |  76.6% | 68.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 1.0 |
| Adhesives                 |  50.0% |  25.0% |  33.3% | 4.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  87.3% |  88.1% |  87.7% | 109.0 |
| Serous                    |  25.0% |  25.0% |  25.0% | 8.0 |
| Sanguineous               |  50.0% |  75.0% |  60.0% | 4.0 |
| Purulent                  |  18.2% |  66.7% |  28.6% | 3.0 |
| Seropurulent              |  50.0% | 100.0% |  66.7% | 1.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  81.4% |  86.8% |  84.0% | 91.0 |
| Existent                  |  67.5% |  67.5% |  67.5% | 40.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  78.8% |  87.2% |  82.8% | 94.0 |
| Existent                  |  51.5% |  81.0% |  63.0% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  96.3% |  88.0% |  92.0% | 117.0 |
| Medium                    |  40.7% |  73.3% |  52.4% | 15.0 |
| High                      |  33.3% |  20.0% |  25.0% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         |  92.2% |  88.4% |  90.3% | 121.0 |
| Clinic Visit (Yellow, <48h) |  25.0% |  41.7% |  31.2% | 12.0 |
| Emergency Care (Red, immediate) | 100.0% |  25.0% |  40.0% | 4.0 |
