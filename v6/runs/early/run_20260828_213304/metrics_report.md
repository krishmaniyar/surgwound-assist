# SurgWound Assist — Metrics Report
*Generated: 2026-08-28 21:50:12*

## Aggregate Metrics

| Metric | Value |
|--------|-------|
| **Mean Macro-F1 (all heads)** | **38.81%** |
| Exact Match Ratio (all 8 correct) | 0.00% |
| Hamming Loss | 0.3500 |

## Target Tracking (≥ 85% Macro-F1)

| Attribute | Macro-F1 | Target | ✓? | Notes |
|-----------|----------|--------|-----|-------|
| Wound Location | **44.30%** | 85% | ❌ | Multi-class spatial distribution across body regions. |
| Healing Status | **63.89%** | 85% | ❌ | Binary epithelialization classification. |
| Closure Method | **29.28%** | 85% | ❌ | Extreme imbalance: staples/adhesives rare. |
| Exudate Type | **6.22%** | 85% | ❌ | Extreme 5-class imbalance (214:4 ratio). |
| Erythema | **46.55%** | 85% | ❌ | Perilesional erythema detection. |
| Edema | **37.19%** | 85% | ❌ | Tissue swelling assessment. |
| Infection Risk | **46.45%** | 85% | ❌ | Extreme imbalance: 207:5 (Low:High). |
| Urgency Level | **36.61%** | 85% | ❌ | Extreme imbalance: 216:3 (Home:Emergency). |

## Per-Attribute Detailed Metrics

### Wound Location
| Metric | Value |
|--------|-------|
| Accuracy | 67.14% |
| Macro Precision | 44.94% |
| Macro Recall | 45.58% |
| **Macro F1** | **44.30%** |
| Weighted F1 | 64.41% |
| ROC-AUC (OvR) | N/A |
| Cohen's Kappa | 0.5792 |
| ECE | 0.1261 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Abdomen | 14 | 92.9% | 94.6% |
| Patella | 13 | 38.5% | 96.5% |
| Ankle | 9 | 66.7% | 96.7% |
| Facial region | 9 | 100.0% | 96.7% |
| Manus | 2 | 0.0% | 100.0% |
| Cervical region | 2 | 0.0% | 100.0% |
| Other | 21 | 66.7% | 71.4% |
| Uncertain | 0 | 0.0% | 100.0% |

**Confusion Matrix:**
```
Classes: Abdomen, Patella, Ankle, Facial region, Manus, Cervical region, Other, Uncertain
[[13  0  0  0  0  0  1  0]
 [ 0  5  1  0  0  0  7  0]
 [ 0  0  6  0  0  0  3  0]
 [ 0  0  0  9  0  0  0  0]
 [ 0  0  0  0  0  0  2  0]
 [ 1  0  0  0  0  0  1  0]
 [ 2  2  1  2  0  0 14  0]
 [ 0  0  0  0  0  0  0  0]]
```

### Healing Status
| Metric | Value |
|--------|-------|
| Accuracy | 67.14% |
| Macro Precision | 64.96% |
| Macro Recall | 63.61% |
| **Macro F1** | **63.89%** |
| Weighted F1 | 66.37% |
| ROC-AUC (OvR) | 0.8122 |
| Cohen's Kappa | 0.2819 |
| ECE | 0.1279 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Healed | 43 | 79.1% | 48.1% |
| Not Healed | 27 | 48.1% | 79.1% |

**Confusion Matrix:**
```
Classes: Healed, Not Healed
[[34  9]
 [14 13]]
```

### Closure Method
| Metric | Value |
|--------|-------|
| Accuracy | 58.57% |
| Macro Precision | 30.81% |
| Macro Recall | 31.78% |
| **Macro F1** | **29.28%** |
| Weighted F1 | 59.58% |
| ROC-AUC (OvR) | N/A |
| Cohen's Kappa | 0.3098 |
| ECE | 0.1344 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Invisible | 18 | 83.3% | 61.5% |
| Sutures | 45 | 55.6% | 84.0% |
| Staples | 2 | 0.0% | 97.1% |
| Adhesives | 5 | 20.0% | 95.4% |
| Uncertain | 0 | 0.0% | 100.0% |

**Confusion Matrix:**
```
Classes: Invisible, Sutures, Staples, Adhesives, Uncertain
[[15  2  0  1  0]
 [16 25  2  2  0]
 [ 0  2  0  0  0]
 [ 4  0  0  1  0]
 [ 0  0  0  0  0]]
```

### Exudate Type
| Metric | Value |
|--------|-------|
| Accuracy | 10.00% |
| Macro Precision | 18.93% |
| Macro Recall | 34.39% |
| **Macro F1** | **6.22%** |
| Weighted F1 | 11.33% |
| ROC-AUC (OvR) | N/A |
| Cohen's Kappa | 0.0276 |
| ECE | 0.3803 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Non-existent | 63 | 6.3% | 100.0% |
| Serous | 2 | 100.0% | 67.6% |
| Sanguineous | 2 | 0.0% | 75.0% |
| Purulent | 1 | 100.0% | 73.9% |
| Seropurulent | 2 | 0.0% | 91.2% |
| Uncertain | 0 | 0.0% | 100.0% |

**Confusion Matrix:**
```
Classes: Non-existent, Serous, Sanguineous, Purulent, Seropurulent, Uncertain
[[ 4 20 17 17  5  0]
 [ 0  2  0  0  0  0]
 [ 0  1  0  0  1  0]
 [ 0  0  0  1  0  0]
 [ 0  1  0  1  0  0]
 [ 0  0  0  0  0  0]]
```

### Erythema
| Metric | Value |
|--------|-------|
| Accuracy | 82.86% |
| Macro Precision | 45.79% |
| Macro Recall | 47.56% |
| **Macro F1** | **46.55%** |
| Weighted F1 | 83.42% |
| ROC-AUC (OvR) | N/A |
| Cohen's Kappa | 0.3974 |
| ECE | 0.0646 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Non-existent | 59 | 88.1% | 54.5% |
| Existent | 11 | 54.5% | 88.1% |
| Uncertain | 0 | 0.0% | 100.0% |

**Confusion Matrix:**
```
Classes: Non-existent, Existent, Uncertain
[[52  7  0]
 [ 5  6  0]
 [ 0  0  0]]
```

### Edema
| Metric | Value |
|--------|-------|
| Accuracy | 75.71% |
| Macro Precision | 37.78% |
| Macro Recall | 36.93% |
| **Macro F1** | **37.19%** |
| Weighted F1 | 74.44% |
| ROC-AUC (OvR) | N/A |
| Cohen's Kappa | 0.1185 |
| ECE | 0.1547 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Non-existent | 57 | 87.7% | 23.1% |
| Existent | 13 | 23.1% | 87.7% |
| Uncertain | 0 | 0.0% | 100.0% |

**Confusion Matrix:**
```
Classes: Non-existent, Existent, Uncertain
[[50  7  0]
 [10  3  0]
 [ 0  0  0]]
```

### Infection Risk
| Metric | Value |
|--------|-------|
| Accuracy | 80.00% |
| Macro Precision | 45.25% |
| Macro Recall | 48.10% |
| **Macro F1** | **46.45%** |
| Weighted F1 | 80.14% |
| ROC-AUC (OvR) | 0.6354 |
| Cohen's Kappa | 0.3817 |
| ECE | 0.0943 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Low | 57 | 86.0% | 53.8% |
| Medium | 12 | 58.3% | 86.2% |
| High | 1 | 0.0% | 100.0% |

**Confusion Matrix:**
```
Classes: Low, Medium, High
[[49  8  0]
 [ 5  7  0]
 [ 1  0  0]]
```

### Urgency Level
| Metric | Value |
|--------|-------|
| Accuracy | 78.57% |
| Macro Precision | 36.00% |
| Macro Recall | 38.02% |
| **Macro F1** | **36.61%** |
| Weighted F1 | 79.81% |
| ROC-AUC (OvR) | 0.6113 |
| Cohen's Kappa | 0.0987 |
| ECE | 0.1204 |

**Per-Class Sensitivity & Specificity:**
| Class | Support | Sensitivity | Specificity |
|-------|---------|-------------|-------------|
| Home Care (Green) | 62 | 85.5% | 25.0% |
| Clinic Visit (Yellow, <48h) | 7 | 28.6% | 85.7% |
| Emergency Care (Red, immediate) | 1 | 0.0% | 100.0% |

**Confusion Matrix:**
```
Classes: Home Care (Green), Clinic Visit (Yellow, <48h), Emergency Care (Red, immediate)
[[53  9  0]
 [ 5  2  0]
 [ 1  0  0]]
```

---
> [!IMPORTANT]
> **Research prototype only.** Not cleared for clinical use.