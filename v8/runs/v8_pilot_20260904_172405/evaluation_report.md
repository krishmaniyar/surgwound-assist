# SurgWound Assist — Experiment v8_pilot Test Results (7x TTA Enabled)

## Overall Summary (Aligned with Base Paper Tables 2, 3, 4)
- **Mean Macro-F1**: **47.21%**
- **Mean Accuracy**: 71.07%
- **Mean Macro-Precision**: 50.11%
- **Mean Macro-Recall**: 49.36%
- **Mean Weighted-F1**: 70.57%
- **Minority-Heads Macro-F1** (Exudate, Infection, Closure, Edema): **29.51%**
- **Exact Match Ratio**: 8.57%

## Per-Attribute Summary Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|---|---|---|---|---|---|---|---|---|
| location         |  45.71% |  48.33% |  45.74% |  37.04% |  45.71% |  45.35% | N/A | 0.3323 |
| healing_status   |  57.14% |  62.53% |  61.67% |  57.00% |  57.14% |  56.44% | 0.6736 | 0.2051 |
| closure_method   |  60.00% |  30.82% |  24.22% |  23.32% |  60.00% |  56.82% | N/A | 0.1489 |
| exudate_type     |  88.57% |  28.48% |  29.37% |  28.91% |  88.57% |  86.54% | N/A | 0.2371 |
| erythema         |  78.57% |  64.12% |  68.80% |  65.59% |  78.57% |  80.08% | N/A | 0.3173 |
| edema            |  65.71% |  31.79% |  30.86% |  31.32% |  65.71% |  66.84% | N/A | -0.0526 |
| infection_risk   |  72.86% |  34.83% |  34.21% |  34.47% |  72.86% |  72.51% | N/A | 0.0965 |
| urgency_level    | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | N/A | N/A |

## Per-Class Detailed Breakdown

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen                   |  75.0% |  42.9% |  54.5% | 14.0 |
| Patella                   | 100.0% |  15.4% |  26.7% | 13.0 |
| Ankle                     |  45.5% |  55.6% |  50.0% | 9.0 |
| Facial region             |  57.1% |  44.4% |  50.0% | 9.0 |
| Manus                     |   0.0% |   0.0% |   0.0% | 2.0 |
| Cervical region           |  14.3% | 100.0% |  25.0% | 2.0 |
| Other                     |  46.4% |  61.9% |  53.1% | 21.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed                    |  78.3% |  41.9% |  54.5% | 43.0 |
| Not Healed                |  46.8% |  81.5% |  59.5% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible                 |  75.0% |  16.7% |  27.3% | 18.0 |
| Sutures                   |  69.1% |  84.4% |  76.0% | 45.0 |
| Staples                   |   0.0% |   0.0% |   0.0% | 2.0 |
| Adhesives                 |  10.0% |  20.0% |  13.3% | 5.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  92.4% |  96.8% |  94.6% | 63.0 |
| Serous                    |   0.0% |   0.0% |   0.0% | 2.0 |
| Sanguineous               |   0.0% |   0.0% |   0.0% | 2.0 |
| Purulent                  |   0.0% |   0.0% |   0.0% | 1.0 |
| Seropurulent              |  50.0% |  50.0% |  50.0% | 2.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  90.7% |  83.1% |  86.7% | 59.0 |
| Existent                  |  37.5% |  54.5% |  44.4% | 11.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent              |  80.0% |  77.2% |  78.6% | 57.0 |
| Existent                  |  15.4% |  15.4% |  15.4% | 13.0 |
| Uncertain                 |   0.0% |   0.0% |   0.0% | 0.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low                       |  84.5% |  86.0% |  85.2% | 57.0 |
| Medium                    |  20.0% |  16.7% |  18.2% | 12.0 |
| High                      |   0.0% |   0.0% |   0.0% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green)         | 100.0% | 100.0% | 100.0% | 70.0 |
| Clinic Visit (Yellow, <48h) |   0.0% |   0.0% |   0.0% | 0 |
| Emergency Care (Red, immediate) |   0.0% |   0.0% |   0.0% | 0 |
