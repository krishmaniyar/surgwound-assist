# SurgWound Assist v8 — Test Error Analysis
**Run**: `v8_pilot_20260904_172405`
**Total Test Samples**: 70
**Samples with at least 1 error**: 68 / 70 (97.1%)
**Exact Match Samples**: 2 / 70 (2.9%)

## Most Frequent Misclassifications by Attribute
### LOCATION (F1: 42.06%, Acc: 45.71%)
| True Class | Misclassified As | Count |
|---|---|---|
| Other | Patella | 6 |
| Facial region | Cervical region | 5 |
| Other | Manus | 5 |
| Abdomen | Cervical region | 4 |
| Other | Ankle | 4 |
| Patella | Ankle | 2 |
| Ankle | Manus | 2 |
| Other | Abdomen | 2 |
| Other | Facial region | 2 |
| Patella | Abdomen | 1 |
| Patella | Manus | 1 |
| Patella | Cervical region | 1 |
| Ankle | Patella | 1 |
| Ankle | Cervical region | 1 |
| Manus | Ankle | 1 |

### HEALING_STATUS (F1: 60.45%, Acc: 61.43%)
| True Class | Misclassified As | Count |
|---|---|---|
| Healed | Not Healed | 16 |
| Not Healed | Healed | 11 |

### CLOSURE_METHOD (F1: 24.76%, Acc: 37.14%)
| True Class | Misclassified As | Count |
|---|---|---|
| Sutures | Adhesives | 13 |
| Sutures | Staples | 10 |
| Invisible | Staples | 4 |
| Invisible | Adhesives | 4 |
| Sutures | Invisible | 4 |
| Invisible | Sutures | 2 |
| Sutures | Uncertain | 2 |
| Invisible | Uncertain | 1 |
| Staples | Adhesives | 1 |
| Adhesives | Invisible | 1 |
| Adhesives | Sutures | 1 |
| Adhesives | Staples | 1 |

### EXUDATE_TYPE (F1: 24.10%, Acc: 48.57%)
| True Class | Misclassified As | Count |
|---|---|---|
| Non-existent | Serous | 20 |
| Non-existent | Purulent | 5 |
| Non-existent | Seropurulent | 4 |
| Non-existent | Sanguineous | 2 |
| Non-existent | Uncertain | 1 |
| Serous | Non-existent | 1 |
| Serous | Seropurulent | 1 |
| Sanguineous | Non-existent | 1 |
| Purulent | Seropurulent | 1 |

### ERYTHEMA (F1: 33.42%, Acc: 55.71%)
| True Class | Misclassified As | Count |
|---|---|---|
| Non-existent | Existent | 18 |
| Non-existent | Uncertain | 7 |
| Existent | Non-existent | 3 |
| Existent | Uncertain | 3 |

### EDEMA (F1: 25.57%, Acc: 50.00%)
| True Class | Misclassified As | Count |
|---|---|---|
| Non-existent | Uncertain | 14 |
| Non-existent | Existent | 9 |
| Existent | Non-existent | 9 |
| Existent | Uncertain | 3 |

### INFECTION_RISK (F1: 29.91%, Acc: 50.00%)
| True Class | Misclassified As | Count |
|---|---|---|
| Low | Medium | 25 |
| Medium | High | 4 |
| Medium | Low | 3 |
| Low | High | 2 |
| High | Low | 1 |

### URGENCY_LEVEL (F1: 13.64%, Acc: 25.71%)
| True Class | Misclassified As | Count |
|---|---|---|
| Home Care (Green) | Clinic Visit (Yellow, <48h) | 49 |
| Home Care (Green) | Emergency Care (Red, immediate) | 3 |

## Top Hardest Test Images (Most Errors)
| Image | Error Count | Details |
|---|---|---|
| `147.jpg` | 8 / 8 | **location**: True: Other -> Pred: Abdomen (conf=47.2%)<br/>**healing_status**: True: Healed -> Pred: Not Healed (conf=56.1%)<br/>**closure_method**: True: Sutures -> Pred: Invisible (conf=49.8%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=38.4%)<br/>**erythema**: True: Existent -> Pred: Non-existent (conf=48.5%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=63.6%)<br/>**infection_risk**: True: Low -> Pred: Medium (conf=67.0%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=82.0%) |
| `356.jpg` | 7 / 8 | **location**: True: Facial region -> Pred: Cervical region (conf=66.0%)<br/>**closure_method**: True: Sutures -> Pred: Invisible (conf=60.6%)<br/>**exudate_type**: True: Non-existent -> Pred: Seropurulent (conf=37.8%)<br/>**erythema**: True: Non-existent -> Pred: Uncertain (conf=54.1%)<br/>**edema**: True: Non-existent -> Pred: Uncertain (conf=53.7%)<br/>**infection_risk**: True: Low -> Pred: Medium (conf=43.5%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=49.2%) |
| `90.jpg` | 7 / 8 | **location**: True: Other -> Pred: Patella (conf=36.4%)<br/>**healing_status**: True: Not Healed -> Pred: Healed (conf=54.2%)<br/>**closure_method**: True: Sutures -> Pred: Staples (conf=41.2%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=28.6%)<br/>**erythema**: True: Existent -> Pred: Non-existent (conf=48.9%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=39.6%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Emergency Care (Red, immediate) (conf=41.8%) |
| `684.jpg` | 7 / 8 | **location**: True: Patella -> Pred: Ankle (conf=27.9%)<br/>**closure_method**: True: Sutures -> Pred: Uncertain (conf=47.5%)<br/>**exudate_type**: True: Non-existent -> Pred: Purulent (conf=32.9%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=37.2%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=46.5%)<br/>**infection_risk**: True: Low -> Pred: High (conf=45.2%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=66.1%) |
| `123.jpg` | 6 / 8 | **location**: True: Other -> Pred: Facial region (conf=28.2%)<br/>**healing_status**: True: Healed -> Pred: Not Healed (conf=59.9%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=31.5%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=36.8%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=49.9%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=63.1%) |
| `22.jpg` | 6 / 8 | **location**: True: Other -> Pred: Ankle (conf=41.4%)<br/>**closure_method**: True: Invisible -> Pred: Sutures (conf=36.6%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=65.1%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=57.4%)<br/>**infection_risk**: True: Low -> Pred: Medium (conf=40.6%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=57.6%) |
| `36.jpg` | 6 / 8 | **location**: True: Other -> Pred: Patella (conf=38.2%)<br/>**healing_status**: True: Healed -> Pred: Not Healed (conf=85.4%)<br/>**closure_method**: True: Sutures -> Pred: Staples (conf=34.3%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=41.7%)<br/>**infection_risk**: True: Low -> Pred: Medium (conf=50.8%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=55.4%) |
| `237.jpg` | 6 / 8 | **location**: True: Other -> Pred: Ankle (conf=39.1%)<br/>**healing_status**: True: Not Healed -> Pred: Healed (conf=52.3%)<br/>**exudate_type**: True: Serous -> Pred: Seropurulent (conf=37.5%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=59.1%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=40.5%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=71.2%) |
| `245.jpg` | 6 / 8 | **closure_method**: True: Sutures -> Pred: Uncertain (conf=47.0%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=40.9%)<br/>**erythema**: True: Existent -> Pred: Uncertain (conf=62.2%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=45.8%)<br/>**infection_risk**: True: Low -> Pred: Medium (conf=38.0%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=77.5%) |
| `95.jpg` | 6 / 8 | **location**: True: Ankle -> Pred: Manus (conf=29.3%)<br/>**closure_method**: True: Sutures -> Pred: Adhesives (conf=46.9%)<br/>**exudate_type**: True: Non-existent -> Pred: Uncertain (conf=29.3%)<br/>**erythema**: True: Existent -> Pred: Uncertain (conf=50.0%)<br/>**edema**: True: Non-existent -> Pred: Uncertain (conf=90.9%)<br/>**infection_risk**: True: Medium -> Pred: High (conf=48.9%) |
| `904.jpg` | 6 / 8 | **healing_status**: True: Not Healed -> Pred: Healed (conf=50.8%)<br/>**closure_method**: True: Adhesives -> Pred: Staples (conf=48.2%)<br/>**erythema**: True: Non-existent -> Pred: Uncertain (conf=44.2%)<br/>**edema**: True: Non-existent -> Pred: Uncertain (conf=56.2%)<br/>**infection_risk**: True: Low -> Pred: Medium (conf=59.9%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=59.3%) |
| `420.jpg` | 6 / 8 | **location**: True: Facial region -> Pred: Cervical region (conf=26.5%)<br/>**closure_method**: True: Sutures -> Pred: Staples (conf=37.6%)<br/>**exudate_type**: True: Non-existent -> Pred: Serous (conf=34.8%)<br/>**edema**: True: Existent -> Pred: Non-existent (conf=45.4%)<br/>**infection_risk**: True: Low -> Pred: Medium (conf=48.6%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=59.0%) |
| `282.jpg` | 6 / 8 | **location**: True: Abdomen -> Pred: Cervical region (conf=24.9%)<br/>**exudate_type**: True: Purulent -> Pred: Seropurulent (conf=52.8%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=63.6%)<br/>**edema**: True: Non-existent -> Pred: Existent (conf=52.4%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=37.8%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=55.4%) |
| `157.jpg` | 6 / 8 | **closure_method**: True: Invisible -> Pred: Staples (conf=45.9%)<br/>**exudate_type**: True: Non-existent -> Pred: Purulent (conf=22.9%)<br/>**erythema**: True: Existent -> Pred: Uncertain (conf=42.6%)<br/>**edema**: True: Existent -> Pred: Uncertain (conf=60.8%)<br/>**infection_risk**: True: Medium -> Pred: Low (conf=49.9%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=47.2%) |
| `996.jpg` | 6 / 8 | **closure_method**: True: Sutures -> Pred: Adhesives (conf=34.9%)<br/>**exudate_type**: True: Serous -> Pred: Non-existent (conf=28.2%)<br/>**erythema**: True: Non-existent -> Pred: Existent (conf=41.6%)<br/>**edema**: True: Non-existent -> Pred: Uncertain (conf=40.0%)<br/>**infection_risk**: True: Medium -> Pred: High (conf=61.7%)<br/>**urgency_level**: True: Home Care (Green) -> Pred: Clinic Visit (Yellow, <48h) (conf=65.5%) |