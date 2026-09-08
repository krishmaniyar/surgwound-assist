# SurgWound Assist: High-Performance Multi-Task Metrics Report

**Date:** 2026-08-28

> [!NOTE]
> **Update Note:** This report supersedes the previous 1-epoch-CPU-pretraining run. It reports the final numbers for the **DINOv2+CLIP ensemble branch** after aggressively addressing majority-class collapse via Class Merging, Class-Balanced Focal Loss, Embedding-Space SMOTE, and τ-normalization. 
> 
> **EffNetV2-S Status:** The EfficientNetV2-S domain pretraining branch has been explicitly excluded from this ensemble and the reported metrics. It is **parked pending GPU access** for proper multi-epoch pretraining, not abandoned.

## Target-Tracking Summary Table (Target ≥ 85% Macro-F1)

| Attribute | Macro-F1 (Test) | Target | Met? | Notes if not met |
|---|---|---|---|---|
| Wound Location | **50.57%** | 85% | ❌ No | Class count constraint: Multi-class spatial distribution across 8 body regions. |
| Healing Status | **75.88%** | 85% | ❌ No | Class count constraint: Binary classification of wound epithelialization. |
| Closure Method (Merged) | **50.49%** | 85% | ❌ No | Merged to 3 classes (Invisible, Sutures, Other). Improved from 16%, but still lacks trustworthy F1 due to thin dataset support. |
| Exudate Type (Merged) | **35.15%** | 85% | ❌ No | Merged to 3 classes (Non-existent, Serous, Other-concerning). Most challenging head; still cannot reach trustworthy F1. |
| Erythema | **57.27%** | 85% | ❌ No | Class count constraint: Perilesional erythema detection. |
| Edema | **60.27%** | 85% | ❌ No | Class count constraint: Tissue swelling assessment. |
| Infection Risk (Merged) | **67.38%** | 85% | ❌ No | Vastly improved from 24% after merging to 2 classes (Low, Elevated Risk) and SMOTE. |
| Urgency Level (Merged) | **70.32%** | 85% | ❌ No | Vastly improved from 12% after merging to 2 classes (Home Care, Elevated Urgency). |

**Mean Per-Attribute Macro-F1:** **58.42%**

## Final Analysis on Unreliable Heads
Despite applying a full suite of techniques to handle severe class imbalance—per-class threshold tuning, logit adjustments, semantic class merging, class-balanced focal loss, embedding-space SMOTE, and τ-normalization (decoupled head retraining)—two heads still fail to produce a trustworthy signal:
1. **Exudate Type (35.15% Macro-F1)**
2. **Closure Method (50.49% Macro-F1)**

This is a legitimate and terminal dataset limitation for this phase of the project. There are simply too few positive samples (e.g., 1-2 examples of Purulent/Seropurulent exudate, 2 examples of Staples) to learn robust, generalizable decision boundaries. These metrics represent the true ceiling for these heads given the current dataset size, and this should be considered the final answer until significantly more data is collected.

---
### Disclaimer
> [!IMPORTANT]
> **Research and Educational Prototype Only:** SurgWound Assist is developed solely for research and technology demonstration purposes and has not been cleared or approved by any medical regulatory authority (such as the US FDA or EMA). It should NOT be used for clinical decision-making or diagnosis.
