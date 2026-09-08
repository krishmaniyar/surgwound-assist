---
name: surgwound-v8-research
description: Operational runbooks, experiment workflows, metric standards, and diagnostic procedures for SurgWound Assist v8 autonomous ML research.
---

# SurgWound Assist v8 — Research & Engineering Runbook

## 1. Environment & Architecture Specifications
- **Python Binary**: `C:\Users\krish\.conda\envs\surgwound-gpu\python.exe`
- **Root Directory**: `d:\Projects\surgwound-assist`
- **Source Directory**: `d:\Projects\surgwound-assist\v8\src`
- **Target GPU**: NVIDIA GeForce RTX 3060 Laptop GPU (6.4 GB VRAM)
- **Primary Target Metric**: Mean Test Macro-F1 across 8 attributes (Baseline v7.5 = **51.10%**)
- **Critical Minority Attributes**: `exudate_type`, `infection_risk`, `closure_method`, `edema`

---

## 2. Standard Autonomous Execution Commands

### A. Run an Experiment
Always run from the project root using the designated conda Python binary:
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_experiment_name `
  --epochs 80 `
  --loss logit_adjusted `
  --lr 3e-5 `
  --seed 42
```

### B. Fast Pilot / Sanity Check (Mandatory before full runs)
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_pilot_check `
  --epochs 3 `
  --loss logit_adjusted
```

### C. Multi-Scale Global + Local Crop Experiment
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_multiscale `
  --epochs 80 `
  --loss logit_adjusted `
  --multiscale
```

---

## 3. Post-Experiment Scientific Workflow Checklist
Every time an experiment completes:
1. **Ledger Update**: Verify entry in `v8/experiments/experiment_registry.csv`.
2. **Research Journal**: Append a detailed entry to `v8/research_journal.md`:
   - Hypothesis and theoretical justification
   - Configuration (backbone, loss, LR, batch size, seed)
   - Results: Test Macro-F1, Minority-Heads Macro-F1, Exact Match Ratio
   - Head-to-head comparison with v7.5 baseline (+/- Delta)
   - Per-attribute gains/losses and confusion matrix analysis
   - Root cause failure analysis (if regressed) or takeaway (if improved)
   - Scientific next step
3. **Ablation Tree**: Update `v8/experiments/ablation_tree.md` with the branch outcome.
4. **Failure Catalog**: If the hypothesis failed, document in `v8/research/failure_catalog.md` to prevent duplicate attempts.
5. **State-of-the-Art & Architecture Updates**: If a new benchmark or architectural change is made:
   - **Update Architecture**: ALWAYS update `docs/architecture.md` whenever new modules, loss formulations, or hyperparameters are introduced.
   - **Sync Docs (MANDATORY)**: Copy the latest best `evaluation_report.md` to `docs/best_evaluation_report.md` and `docs/evaluation_report.md`.
   - **Sync Best Model (MANDATORY)**: Copy the best model checkpoint (`best_model.pt`) to `docs/best_model.pth`.
   - Update `README.md` and `CURRENT_VERSION.md`.

---

## 4. Diagnostic & Analysis Runbooks

### Run Misclassification Analysis on Latest Run:
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\analysis\inspect_errors.py
```

### Run Feature Space Separability Analysis (t-SNE / Centroid Distances):
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\analysis\feature_separability.py
```
