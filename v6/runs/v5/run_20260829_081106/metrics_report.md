# SurgWound Assist — v4.0 End-to-End Metrics Report

## Aggregate Metrics
- **Mean Macro-F1**: 51.95%
- **Exact Match Ratio**: 25.71%
- **Hamming Loss**: 0.1857

## Per-Attribute Breakdown
| Attribute | Macro-F1 | Accuracy | AUC | ECE | Kappa |
|-----------|----------|----------|-----|-----|-------|
| location | 54.37% | 71.43% | N/A | 0.1732 | 0.6379 |
| healing_status | 74.10% | 77.14% | 0.8010 | 0.1969 | 0.4895 |
| closure_method | 29.91% | 68.57% | N/A | 0.2107 | 0.2058 |
| exudate_type | 38.93% | 90.00% | N/A | 0.0701 | 0.2007 |
| erythema | 39.00% | 82.86% | N/A | 0.1315 | 0.1773 |
| edema | 44.00% | 78.57% | N/A | 0.1542 | -0.0521 |
| infection_risk | 35.29% | 82.86% | 0.7617 | 0.1525 | 0.1204 |
| urgency_level | 100.00% | 100.00% | N/A | 0.0020 | nan |