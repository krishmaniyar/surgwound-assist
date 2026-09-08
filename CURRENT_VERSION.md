# SurgWound Assist - Current Version: v8.0 (BiomedCLIP Multi-Scale + Semantic Prototypes)

## Quick Start
```powershell
# Run v8 autonomous pipeline
& "C:\Users\krish\.conda\envs\surgwound-gpu\python.exe" v8/src/run_experiment.py --exp_id v8_run --epochs 80 --loss logit_adjusted --multiscale
```

## Version Map
| Folder | Architecture | Test F1 (Macro) | Dataset | Status |
|--------|-------------|-----------------|---------|--------|
| `v6/`  | DINOv2-Large + LLRD | 54.66% | 349 imgs | Archived |
| `v7/`  | BiomedCLIP Medical (v7.5) | 51.10% | 349 imgs | Archived Baseline |
| `v7/`  | BiomedCLIP Medical (v7.6) | 44.74% (137 Test Benchmark) | 686 imgs | Archived |
| `v8/`  | **BiomedCLIP MultiScale + Text Prototypes (v8.0)** | **58.73%** | **349 imgs** | **ACTIVE SOTA** |

## Shared Resources
- `data/` - SurgWound Dataset images and annotations
- `archive/` - Baseline datasets and archived experiments
- `docs/` - Research journal, architecture history, changelog
- `v8/` - Active v8 pipeline, checkpoints, experiment registry, research matrix, and reports
