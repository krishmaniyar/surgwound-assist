---
name: surgwound-workflows
description: Standard commands, environment specifications, and procedures for running the SurgWound pipeline, training, evaluation, and documentation updates across all versions (v7, v8).
---

# SurgWound Project Workflows & Runbooks

## Environment
- **Conda Environment**: `surgwound-gpu`
- **Python Binary**: `C:\Users\krish\.conda\envs\surgwound-gpu\python.exe`
- **Root Directory**: `d:\Projects\surgwound-assist`

Always use `C:\Users\krish\.conda\envs\surgwound-gpu\python.exe` or `conda run -n surgwound-gpu python ...` when executing any scripts in this project.

---

## Frequent Repetitive Commands

### 1. Run SurgWound v8 Pipeline (Train + Threshold Opt + 7x TTA)
```powershell
# From project root
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_experiment `
  --epochs 80 `
  --loss logit_adjusted `
  --lr 3e-5 `
  --seed 42
```

### 2. Run Fast Pilot Sanity Check (3 Epochs)
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_pilot `
  --epochs 3 `
  --loss logit_adjusted
```

### 3. Run Multi-Scale (Global + Local Wound Crop) Training
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_multiscale `
  --epochs 80 `
  --loss logit_adjusted `
  --multiscale
```

### 4. Run Legacy v7 Pipeline (Baseline Parity)
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v7\src\run_pipeline.py
```

### 5. Diagnostics & Error Inspection
```powershell
# Inspect latest test misclassifications
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\analysis\inspect_errors.py

# Compute feature space intra/inter-class distances & silhouette scores
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\analysis\feature_separability.py
```

### 6. Check GPU Availability and VRAM in Python Environment
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" -c "import torch; print('CUDA Available:', torch.cuda.is_available(), '| Device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU', '| VRAM Allocated:', round(torch.cuda.memory_allocated()/1e9, 2), 'GB')"
```

---

## Post-Run Checklist
Every time a training run finishes:
1. Update `v8/experiments/experiment_registry.csv` with final metrics, VRAM, and conclusion.
2. Update `v8/research_journal.md` with experiment hypothesis, per-attribute metrics, confusion matrix takeaways, and next actions.
3. Update `v8/experiments/ablation_tree.md` with the branch outcome.
4. Update `v8/research/failure_catalog.md` if any unexpected failure mode occurred.
5. If the score established a new state-of-the-art benchmark or introduced architectural changes:
   - Update `docs/architecture.md` with parameters, test F1, and architecture diagram.
   - Update `CURRENT_VERSION.md`
   - Update `docs/CHANGELOG.md`
   - Update `README.md`
6. **Docs Centralization (MANDATORY)**:
   - Copy the latest best evaluation report to `docs/best_evaluation_report.md` and `docs/evaluation_report.md`.
   - Copy the latest best model checkpoint to `docs/best_model.pth`.
