---
name: surgwound-research
description: Master ML research, experiment governance, evaluation protocols, and operational runbooks across all versions of SurgWound Assist (v6, v7, v8+).
---

# SurgWound Assist — Global Autonomous ML Research & Engineering Skill

## 1. System & Environment Specifications
- **Project Root**: `d:\Projects\surgwound-assist`
- **Conda Environment**: `surgwound-gpu`
- **Python Binary**: `C:\Users\krish\.conda\envs\surgwound-gpu\python.exe`
- **Target Hardware**: NVIDIA GeForce RTX 3060 Laptop GPU (6.4 GB VRAM), Windows 11
- **Domain**: Multi-task classification of 8 surgical wound attributes from post-operative photographs:
  `location`, `healing_status`, `closure_method`, `exudate_type`, `erythema`, `edema`, `infection_risk`, `urgency_level`.
- **Dataset**: Small-data long-tail medical regime (~349 to 686 images, extreme class imbalance up to 72:1).

---

## 2. Universal Operational Workflows

### A. Run Active Pipeline (Train + Evaluate)
```powershell
# Run v8 autonomous pipeline
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_experiment `
  --epochs 80 `
  --loss logit_adjusted `
  --lr 3e-5 `
  --seed 42
```

### B. Fast Sanity / Pilot Verification (Mandatory before full runs)
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_pilot `
  --epochs 3 `
  --loss logit_adjusted
```

### C. Multi-Scale Global + Local High-Resolution Inference
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\src\run_experiment.py `
  --exp_id v8_multiscale `
  --epochs 80 `
  --multiscale
```

---

## 3. Scientific Post-Run Protocol
Whenever a training or evaluation run finishes:
1. **Experiment Registry**: Verify entry in `v8/experiments/experiment_registry.csv`.
2. **Research Journal**: Record hypothesis, convergence dynamics, per-attribute metrics, confusion matrices, and takeaways in `v8/research_journal.md`.
3. **Failure Guardrails**: If an experiment failed or regressed, add root cause analysis to `v8/research/failure_catalog.md`.
4. **Benchmark & Architecture Updates**: If a new architectural change or state-of-the-art score is established:
   - Update `docs/architecture.md` with new parameters, benchmark F1, and design changes.
   - Update `CURRENT_VERSION.md`
   - Update `README.md`
   - Update `docs/CHANGELOG.md`
5. **Docs Centralization (MANDATORY)**:
   - Copy the latest best evaluation report to `docs/best_evaluation_report.md` and `docs/evaluation_report.md`.
   - Copy the latest best model checkpoint to `docs/best_model.pth`.

---

## 4. Diagnostics & Analysis Tooling

### A. Misclassification & Hard Sample Inspection
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\analysis\inspect_errors.py
```

### B. Feature Space Separability & Silhouette Analysis
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" d:\Projects\surgwound-assist\v8\analysis\feature_separability.py
```

### C. GPU Health & Memory Audit
```powershell
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" -c "import torch; print('Device:', torch.cuda.get_device_name(0), '| Allocated:', round(torch.cuda.memory_allocated()/1e9, 2), 'GB | Max:', round(torch.cuda.max_memory_allocated()/1e9, 2), 'GB')"
```
