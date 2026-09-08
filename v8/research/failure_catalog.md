# SurgWound Assist — Failure Modes & Preventative Catalog

This living document archives every documented engineering and scientific failure across project history (v1 through v8), its root cause, and the permanent architectural guardrail installed to prevent regression.

---

## 1. FP16 GradScaler Overflow in Scaled Margin Losses (v7.0 – v7.3)
- **Symptom**: `loss=nan` starting at the exact epoch when LDAM was activated; parameters froze; predictions collapsed.
- **Root Cause**: LDAM applies a scaling factor $s=15$ or $s=30$. PyTorch `GradScaler` multiplies gradients by $\approx 65536$. Combined, $65536 \times 15 \times \text{grad} > 65504$ (the maximum finite value in FP16), overflowing to `+Inf` during backpropagation.
- **Failed Attempts**: Casting loss inputs `x.float()` inside `forward()` was insufficient because the overflow occurred during gradient backprop through the scaler.
- **Permanent Solution**:
  1. For LDAM: disable AMP and run pure FP32 during the LDAM phase.
  2. For v8: replace LDAM with **Logit-Adjusted Loss** ($\tau \log \pi$). Logit adjustment applies additive offsets directly to logits without scale multiplication, rendering it inherently stable under native FP16/AMP without requiring scaler bypasses.

---

## 2. Incomplete Label Mapping & Silent Normalization Collapse (v7.5)
- **Symptom**: `urgency_level` scored an artificial 100% Macro-F1 with Cohen's Kappa `NaN`.
- **Root Cause**: The raw CSV contained descriptive strings (`"Home Care (Green): Manage with routine care"`), while `CLASS_MAPPINGS` had short names (`"Home Care (Green)"`). `normalize_label()` fell back to `return 0` whenever an exact match was not found. Consequently, every single sample in train, val, and test was labeled `0`.
- **Permanent Solution**:
  1. Implement semantic substring parsing in `v8/src/dataset.py`.
  2. Explicitly support both `legacy_mode=True` (for strict parity with v7.5) and `legacy_mode=False` (for clean medical evaluation).
  3. Emit diagnostic alerts when any attribute exhibits single-class collapse in the dataset.

---

## 3. Catastrophic Forgetting from Homogeneous Learning Rates (v5.0)
- **Symptom**: Scaling from DINOv2-Base (86M) to DINOv2-Large (300M) resulted in performance regression (55.31% down to 51.95%).
- **Root Cause**: Sending full learning rate (`2e-5`) into pretrained early transformer layers overwrote low-level visual edge filters before the randomly initialized classifier heads could stabilize.
- **Permanent Solution**:
  - Always enforce **Layer-Wise Learning Rate Decay (LLRD)** with decay rate $0.85$.
  - Enforce linear learning rate warmup for the first 10% of training steps.

---

## 4. Frozen Backbone Feature Inadequacy (v2.0)
- **Symptom**: Static embeddings (DINOv2 + CLIP) plateaued at 38.81% Macro-F1 despite 30 Optuna trials per head.
- **Root Cause**: Features pretrained on generic web photography (ImageNet / LAION) lack domain calibration for subtle surgical attributes (purulent vs serous fluid, subtle erythema).
- **Permanent Solution**: End-to-end fine-tuning on a medically pretrained vision backbone (BiomedCLIP) is mandatory.

---

## 5. Decision Boundary Suppression of Minority Classes (v7.5)
- **Symptom**: In v7.5, minority classes in `exudate_type` (Purulent, Sanguineous, Seropurulent) and `infection_risk` (Medium, High) had 0.0% recall under standard argmax prediction.
- **Root Cause**: Posterior probabilities for rare classes rarely exceed 0.5 or beat the majority class probability when sample imbalance exceeds 20:1.
- **Permanent Solution**: In v8, optimize per-class decision thresholds on the validation set (`v8/src/evaluate.py`), boosting minority recall while preserving precision.
