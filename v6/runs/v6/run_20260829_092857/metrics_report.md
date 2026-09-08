# SurgWound Assist — v4.0 End-to-End Metrics Report

## Aggregate Metrics
- **Mean Macro-F1**: 54.66%
- **Exact Match Ratio**: 28.57%
- **Hamming Loss**: 0.1768

## Per-Attribute Breakdown
| Attribute | Macro-F1 | Accuracy | AUC | ECE | Kappa |
|-----------|----------|----------|-----|-----|-------|
| location | 62.83% | 74.29% | N/A | 0.1114 | 0.6750 |
| healing_status | 72.16% | 75.71% | 0.7890 | 0.1132 | 0.4536 |
| closure_method | 34.02% | 72.86% | N/A | 0.2154 | 0.3235 |
| exudate_type | 18.95% | 90.00% | N/A | 0.2500 | 0.0000 |
| erythema | 60.32% | 85.71% | N/A | 0.1129 | 0.2341 |
| edema | 54.33% | 78.57% | N/A | 0.1260 | 0.1056 |
| infection_risk | 34.63% | 81.43% | 0.7389 | 0.1875 | 0.0900 |
| urgency_level | 100.00% | 100.00% | N/A | 0.0373 | nan |