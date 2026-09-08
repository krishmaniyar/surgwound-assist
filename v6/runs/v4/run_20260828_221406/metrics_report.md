# SurgWound Assist — v4.0 End-to-End Metrics Report

## Aggregate Metrics
- **Mean Macro-F1**: 55.31%
- **Exact Match Ratio**: 21.43%
- **Hamming Loss**: 0.2018

## Per-Attribute Breakdown
| Attribute | Macro-F1 | Accuracy | AUC | ECE | Kappa |
|-----------|----------|----------|-----|-----|-------|
| location | 55.56% | 62.86% | N/A | 0.1293 | 0.5329 |
| healing_status | 64.38% | 68.57% | 0.7709 | 0.1293 | 0.2981 |
| closure_method | 36.14% | 71.43% | N/A | 0.1054 | 0.4027 |
| exudate_type | 32.26% | 90.00% | N/A | 0.1130 | 0.2020 |
| erythema | 58.93% | 84.29% | N/A | 0.1096 | 0.1996 |
| edema | 61.75% | 82.86% | N/A | 0.0895 | 0.2566 |
| infection_risk | 33.43% | 78.57% | 0.6690 | 0.1277 | 0.0367 |
| urgency_level | 100.00% | 100.00% | N/A | 0.0320 | nan |