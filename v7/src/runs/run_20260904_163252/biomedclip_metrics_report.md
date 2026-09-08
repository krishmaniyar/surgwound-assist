# SurgWound Assist — v7.5 BiomedCLIP Metrics (with 7x TTA)

## Overall Summary (Aligned with Base Paper Table 2/3/4)
- **Mean Macro-F1**: 51.10%
- **Mean Accuracy**: 77.50%
- **Mean Macro-Precision**: 50.65%
- **Mean Macro-Recall**: 52.12%
- **Mean Weighted-F1**: 75.04%
- **Exact Match Ratio**: 14.29%

## Per-Attribute Comparison Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|-----------|----------|-------------------|----------------|----------|----------|-------------|-----|-------|
| location | 54.29% | 41.44% | 42.22% | 40.76% | 54.29% | 51.77% | N/A | 0.4159 |
| healing_status | 77.14% | 75.88% | 75.88% | 75.88% | 77.14% | 77.14% | 0.8234 | 0.5177 |
| closure_method | 67.14% | 32.01% | 32.78% | 32.00% | 67.14% | 63.00% | N/A | 0.2574 |
| exudate_type | 88.57% | 18.24% | 19.68% | 18.93% | 88.57% | 85.19% | N/A | 0.0865 |
| erythema | 80.00% | 63.97% | 65.95% | 64.80% | 80.00% | 80.66% | N/A | 0.2970 |
| edema | 72.86% | 46.57% | 47.71% | 46.78% | 72.86% | 70.20% | N/A | -0.0539 |
| infection_risk | 80.00% | 27.05% | 32.75% | 29.63% | 80.00% | 72.38% | N/A | -0.0262 |
| urgency_level | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% | N/A | N/A |

## Per-Class Detailed Breakdown (Base Paper Alignment)

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen | 84.62% | 78.57% | 81.48% | 14.0 |
| Patella | 33.33% | 15.38% | 21.05% | 13.0 |
| Ankle | 57.14% | 44.44% | 50.00% | 9.0 |
| Facial region | 75.00% | 100.00% | 85.71% | 9.0 |
| Manus | 0.00% | 0.00% | 0.00% | 2.0 |
| Cervical region | 0.00% | 0.00% | 0.00% | 2.0 |
| Other | 40.00% | 57.14% | 47.06% | 21.0 |
| Uncertain | 0.00% | 0.00% | 0.00% | 0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed | 81.40% | 81.40% | 81.40% | 43.0 |
| Not Healed | 70.37% | 70.37% | 70.37% | 27.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible | 57.14% | 44.44% | 50.00% | 18.0 |
| Sutures | 70.91% | 86.67% | 78.00% | 45.0 |
| Staples | 0.00% | 0.00% | 0.00% | 2.0 |
| Adhesives | 0.00% | 0.00% | 0.00% | 5.0 |
| Uncertain | 0.00% | 0.00% | 0.00% | 0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent | 91.18% | 98.41% | 94.66% | 63.0 |
| Serous | 0.00% | 0.00% | 0.00% | 2.0 |
| Sanguineous | 0.00% | 0.00% | 0.00% | 2.0 |
| Purulent | 0.00% | 0.00% | 0.00% | 1.0 |
| Seropurulent | 0.00% | 0.00% | 0.00% | 2.0 |
| Uncertain | 0.00% | 0.00% | 0.00% | 0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent | 89.47% | 86.44% | 87.93% | 59.0 |
| Existent | 38.46% | 45.45% | 41.67% | 11.0 |
| Uncertain | 0.00% | 0.00% | 0.00% | 0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent | 80.65% | 87.72% | 84.03% | 57.0 |
| Existent | 12.50% | 7.69% | 9.52% | 13.0 |
| Uncertain | 0.00% | 0.00% | 0.00% | 0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low | 81.16% | 98.25% | 88.89% | 57.0 |
| Medium | 0.00% | 0.00% | 0.00% | 12.0 |
| High | 0.00% | 0.00% | 0.00% | 1.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green) | 100.00% | 100.00% | 100.00% | 70.0 |
| Clinic Visit (Yellow, <48h) | 0.00% | 0.00% | 0.00% | 0 |
| Emergency Care (Red, immediate) | 0.00% | 0.00% | 0.00% | 0 |
