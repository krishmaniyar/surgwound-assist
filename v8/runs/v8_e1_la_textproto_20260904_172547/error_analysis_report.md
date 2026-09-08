# SurgWound Assist v8 — Test Error Analysis
**Run**: `v8_e1_la_textproto_20260904_172547`
**Total Test Samples**: 70
**Samples with at least 1 error**: 57 / 70 (81.4%)
**Exact Match Samples**: 13 / 70 (18.6%)

## Most Frequent Misclassifications by Attribute
### LOCATION (F1: 62.71%, Acc: 65.71%)
| True Class | Misclassified As | Count |
|---|---|---|
| Patella | Other | 4 |
| Other | Patella | 3 |
| Ankle | Other | 2 |
| Other | Abdomen | 2 |
| Other | Facial region | 2 |
| Other | Manus | 2 |
| Abdomen | Ankle | 1 |
| Abdomen | Cervical region | 1 |
| Patella | Abdomen | 1 |
| Patella | Ankle | 1 |
| Patella | Cervical region | 1 |
| Ankle | Abdomen | 1 |
| Facial region | Cervical region | 1 |
| Manus | Other | 1 |
| Other | Ankle | 1 |

### HEALING_STATUS (F1: 64.38%, Acc: 68.57%)
| True Class | Misclassified As | Count |
|---|---|---|
| Not Healed | Healed | 15 |
| Healed | Not Healed | 7 |

### CLOSURE_METHOD (F1: 38.96%, Acc: 65.71%)
| True Class | Misclassified As | Count |
|---|---|---|
| Sutures | Invisible | 7 |
| Invisible | Sutures | 6 |
| Adhesives | Sutures | 4 |
| Sutures | Adhesives | 3 |
| Staples | Sutures | 2 |
| Invisible | Adhesives | 1 |
| Sutures | Staples | 1 |

### EXUDATE_TYPE (F1: 18.77%, Acc: 87.14%)
| True Class | Misclassified As | Count |
|---|---|---|
| Non-existent | Serous | 2 |
| Serous | Non-existent | 2 |
| Sanguineous | Non-existent | 2 |
| Purulent | Non-existent | 1 |
| Seropurulent | Non-existent | 1 |
| Seropurulent | Purulent | 1 |

### ERYTHEMA (F1: 62.25%, Acc: 80.00%)
| True Class | Misclassified As | Count |
|---|---|---|
| Non-existent | Existent | 7 |
| Existent | Non-existent | 7 |

### EDEMA (F1: 30.86%, Acc: 71.43%)
| True Class | Misclassified As | Count |
|---|---|---|
| Existent | Non-existent | 12 |
| Non-existent | Existent | 7 |
| Non-existent | Uncertain | 1 |

### INFECTION_RISK (F1: 34.87%, Acc: 81.43%)
| True Class | Misclassified As | Count |
|---|---|---|
| Medium | Low | 10 |
| Low | Medium | 1 |
| Medium | High | 1 |
| High | Low | 1 |

### URGENCY_LEVEL (F1: 100.00%, Acc: 100.00%)
*(No errors for this attribute)*

## Top Hardest Test Images (Most Errors)
| Image | Error Count | Details |
|---|---|---|
| `237.jpg` | 6 / 8 | **location**: True: Other -> Pred: Ankle (conf=62.3%)<br/>**healing_status**: True: Not Healed -> Pred: Healed (conf=89.1%)<br/>**closure_method**: True: Sutures -> Pred: Invisible (conf=63.0%)<br/>**exudate_type**: True: Serous -> Pred: Non-existent (conf=76.0%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=97.3%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=90.0%) |
| `271.jpg` | 5 / 8 | **healing_status**: True: Not Healed -> Pred: Healed (conf=88.9%)<br/>**closure_method**: True: Invisible -> Pred: Sutures (conf=92.4%)<br/>**exudate_type**: True: Seropurulent -> Pred: Non-existent (conf=86.0%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=54.4%)<br/>**infection_risk**: True: High -> Pred: Low (conf=95.3%) |
| `66.jpg` | 5 / 8 | **healing_status**: True: Not Healed -> Pred: Healed (conf=94.7%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=73.3%)<br/>**erythema**: True: Existent -> Pred: Non-existent (conf=50.7%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=98.0%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=65.5%) |
| `658.jpg` | 5 / 8 | **closure_method**: True: Invisible -> Pred: Sutures (conf=67.7%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=45.1%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=86.8%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=95.7%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=85.6%) |
| `897.jpg` | 5 / 8 | **location**: True: Other -> Pred: Abdomen (conf=89.8%)<br/>**healing_status**: True: Not Healed -> Pred: Healed (conf=94.2%)<br/>**closure_method**: True: Staples -> Pred: Sutures (conf=79.8%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=80.1%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=73.8%) |
| `95.jpg` | 4 / 8 | **location**: True: Ankle -> Pred: Other (conf=46.9%)<br/>**closure_method**: True: Sutures -> Pred: Adhesives (conf=48.8%)<br/>**edema**: True: Non-existent -> Pred: Uncertain (conf=50.4%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=96.4%) |
| `282.jpg` | 4 / 8 | **closure_method**: True: Adhesives -> Pred: Sutures (conf=47.1%)<br/>**exudate_type**: True: Purulent -> Pred: Non-existent (conf=59.7%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=57.4%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=48.3%) |
| `157.jpg` | 4 / 8 | **healing_status**: True: Not Healed -> Pred: Healed (conf=60.1%)<br/>**erythema**: True: Existent -> Pred: Non-existent (conf=58.1%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=67.5%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=98.4%) |
| `90.jpg` | 4 / 8 | **healing_status**: True: Not Healed -> Pred: Healed (conf=80.2%)<br/>**erythema**: True: Existent -> Pred: Non-existent (conf=63.1%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=53.0%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=97.0%) |
| `893.jpg` | 4 / 8 | **location**: True: Other -> Pred: Manus (conf=45.6%)<br/>**healing_status**: True: Healed -> Pred: Not Healed (conf=73.9%)<br/>**closure_method**: True: Invisible -> Pred: Adhesives (conf=73.2%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=41.6%) |
| `996.jpg` | 4 / 8 | **exudate_type**: True: Serous -> Pred: Non-existent (conf=55.7%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=50.3%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=67.8%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=63.0%) |
| `147.jpg` | 4 / 8 | **location**: True: Other -> Pred: Abdomen (conf=96.4%)<br/>**healing_status**: True: Healed -> Pred: Not Healed (conf=90.8%)<br/>**erythema**: True: Existent -> Pred: Non-existent (conf=98.7%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=89.1%) |
| `22.jpg` | 3 / 8 | **location**: True: Other -> Pred: Patella (conf=34.5%)<br/>**closure_method**: True: Invisible -> Pred: Sutures (conf=98.3%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=99.7%) |
| `352.jpg` | 3 / 8 | **exudate_type**: True: Sanguineous -> Pred: Non-existent (conf=84.7%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=59.6%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=97.5%) |
| `940.jpg` | 3 / 8 | **location**: True: Patella -> Pred: Cervical region (conf=37.6%)<br/>**closure_method**: True: Sutures -> Pred: Invisible (conf=96.3%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=78.8%) |