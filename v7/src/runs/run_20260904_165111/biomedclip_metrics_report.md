# SurgWound Assist — v7.5 BiomedCLIP Metrics (with 7x TTA)

## Overall Summary (Aligned with Base Paper Table 2/3/4)
- **Mean Macro-F1**: 44.74%
- **Mean Accuracy**: 64.69%
- **Mean Macro-Precision**: 46.75%
- **Mean Macro-Recall**: 45.94%
- **Mean Weighted-F1**: 65.92%
- **Exact Match Ratio**: 8.76%

## Per-Attribute Comparison Table
| Attribute | Accuracy | Precision (Macro) | Recall (Macro) | Macro-F1 | Micro-F1 | Weighted-F1 | AUC | Kappa |
|-----------|----------|-------------------|----------------|----------|----------|-------------|-----|-------|
| location | 58.39% | 67.02% | 60.37% | 60.09% | 58.39% | 57.90% | N/A | 0.4827 |
| healing_status | 68.61% | 67.51% | 67.79% | 67.62% | 68.61% | 68.74% | 0.7271 | 0.3527 |
| closure_method | 59.12% | 33.06% | 33.03% | 32.53% | 59.12% | 58.84% | N/A | 0.3508 |
| exudate_type | 64.23% | 38.70% | 33.91% | 31.07% | 64.23% | 68.29% | N/A | 0.2114 |
| erythema | 59.12% | 38.00% | 40.41% | 38.53% | 59.12% | 59.30% | N/A | 0.1790 |
| edema | 52.55% | 43.69% | 44.82% | 43.54% | 52.55% | 55.07% | N/A | 0.1299 |
| infection_risk | 79.56% | 51.59% | 51.00% | 50.15% | 79.56% | 80.61% | N/A | 0.2925 |
| urgency_level | 75.91% | 34.45% | 36.16% | 34.41% | 75.91% | 78.62% | N/A | 0.1209 |

## Per-Class Detailed Breakdown (Base Paper Alignment)

### Location
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Abdomen | 71.43% | 26.32% | 38.46% | 19.0 |
| Patella | 75.00% | 100.00% | 85.71% | 3.0 |
| Ankle | 76.92% | 52.63% | 62.50% | 19.0 |
| Facial region | 100.00% | 46.67% | 63.64% | 15.0 |
| Manus | 77.78% | 70.00% | 73.68% | 10.0 |
| Cervical region | 33.33% | 50.00% | 40.00% | 4.0 |
| Other | 48.00% | 68.57% | 56.47% | 35.0 |
| Uncertain | 53.66% | 68.75% | 60.27% | 32.0 |

### Healing status
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Healed | 74.68% | 71.95% | 73.29% | 82.0 |
| Not Healed | 60.34% | 63.64% | 61.95% | 55.0 |

### Closure method
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Invisible | 37.50% | 31.58% | 34.29% | 19.0 |
| Sutures | 78.57% | 64.71% | 70.97% | 68.0 |
| Staples | 0.00% | 0.00% | 0.00% | 1.0 |
| Adhesives | 0.00% | 0.00% | 0.00% | 4.0 |
| Uncertain | 49.21% | 68.89% | 57.41% | 45.0 |

### Exudate type
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent | 89.01% | 74.31% | 81.00% | 109.0 |
| Serous | 12.50% | 37.50% | 18.75% | 8.0 |
| Sanguineous | 18.18% | 50.00% | 26.67% | 4.0 |
| Purulent | 100.00% | 33.33% | 50.00% | 3.0 |
| Seropurulent | 0.00% | 0.00% | 0.00% | 1.0 |
| Uncertain | 12.50% | 8.33% | 10.00% | 12.0 |

### Erythema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent | 74.36% | 63.74% | 68.64% | 91.0 |
| Existent | 39.66% | 57.50% | 46.94% | 40.0 |
| Uncertain | 0.00% | 0.00% | 0.00% | 6.0 |

### Edema
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Non-existent | 72.73% | 59.57% | 65.50% | 94.0 |
| Existent | 41.67% | 47.62% | 44.44% | 21.0 |
| Uncertain | 16.67% | 27.27% | 20.69% | 22.0 |

### Infection risk
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low | 90.99% | 86.32% | 88.60% | 117.0 |
| Medium | 30.43% | 46.67% | 36.84% | 15.0 |
| High | 33.33% | 20.00% | 25.00% | 5.0 |

### Urgency level
| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Home Care (Green) | 91.82% | 83.47% | 87.45% | 121.0 |
| Clinic Visit (Yellow, <48h) | 11.54% | 25.00% | 15.79% | 12.0 |
| Emergency Care (Red, immediate) | 0.00% | 0.00% | 0.00% | 4.0 |
