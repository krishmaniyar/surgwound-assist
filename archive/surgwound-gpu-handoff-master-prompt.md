# MASTER PROMPT — Complete SurgWound Assist End-to-End on GPU
*(Paste this into Antigravity on the GPU machine. This consolidates every prior prompt for this project into one handoff document. It picks up exactly where the CPU-only work left off and carries the project through GPU training, full imbalance resolution, the API, the React app, and packaging.)*

---

## 0. HANDOFF CONTEXT

You are receiving an existing project folder, not starting from scratch. Read the existing code, configs, checkpoints, logs, and any `metrics_report.md` / ablation tables already in the repo **before writing anything new** — the goal is to complete and correct this project, not rebuild it. If any part of this prompt conflicts with what you find already implemented, trust the actual code/results in the repo and adapt accordingly, but flag the discrepancy in your final write-up.

**State of the project as handed off:**
- Dataset (SurgWound, 686 images, 8 attributes) has been re-aggregated and split.
- A DINOv2 + CLIP frozen-embedding ensemble with per-attribute MLP heads has been trained successfully on CPU and shows real (if weak on several heads) signal.
- An EfficientNetV2-S domain-adaptive pretraining track (using two local AZH datasets — a segmentation dataset and a wound-type/location classification dataset) was attempted but **constrained to 1 CPU epoch** and produced a failed/near-random result (~0-1% macro-F1) — this branch is currently excluded from the ensemble and marked as parked.
- Class-imbalance diagnosis found **majority-class collapse** on several heads (Exudate Type, Infection Risk, Urgency Level, Closure Method scoring near-zero macro-F1 despite likely-fine overall accuracy) — an imbalance-handling stack (stratified split, class-balanced/focal/LDAM loss, decoupled classifier retraining, embedding-space SMOTE, logit adjustment, per-class threshold tuning) was specified and partially run on CPU.
- The React frontend and FastAPI backend have **not** been built yet — model work was the priority first.

**What this prompt exists to finish, now that GPU is available:**
1. Properly re-run the EfficientNetV2-S domain-adaptive pretraining track with real epoch counts and correct hyperparameters (§2-§3).
2. Complete and finalize the imbalance-handling stack at full scale (§4).
3. Re-integrate EfficientNetV2-S into the ensemble only if it earns its place (§5).
4. Optionally fine-tune DINOv2/CLIP's last layers, now feasible on GPU (§6).
5. Produce a final, honest, complete metrics report (§7).
6. Build the FastAPI backend and React frontend (§8).
7. Package the whole thing so it runs with minimal setup (§9).

---

## 1. HARDWARE ENVIRONMENT

| Component | Specification | Notes |
|---|---|---|
| GPU | 1x NVIDIA CUDA-capable GPU | Unlocks the parked EfficientNetV2-S track and makes full-scale imbalance experiments and hyperparameter search practical. |
| VRAM | ≥16GB (e.g. RTX 3080/4080, T4, A10G) | Needed for batch sizes large enough to stabilize BatchNorm during CNN fine-tuning. |
| Estimated time | ~2-4 hours per full pretraining pass | vs. days on CPU for the same run — this is why the 1-epoch CPU result was uninformative, not a real signal about the technique. |

Verify CUDA is actually being used (not silently falling back to CPU) before starting any run — log the device, GPU name, and available VRAM at the start of every training script as a sanity check.

Use mixed precision (`torch.cuda.amp`) throughout — it roughly halves memory use and speeds up training substantially on this VRAM tier, and should comfortably fit the batch sizes specified below.

---

## 2. CONCRETE HYPERPARAMETERS — USE THESE AS DEFAULTS, TUNE FROM HERE

### 2a. Stage 0 — Wound segmentation model (from the local AZH segmentation dataset)
- Backbone: U-Net (as in the source repo) — batch size 16, image size 256×256, ~50-80 epochs, Adam, LR 1e-4 with cosine decay, early stopping on validation Dice/IoU with patience 10.

### 2b. Stage 1 — Domain-adaptive pretraining (EfficientNetV2-S on local AZH classification dataset)
This is the step that only got 1 epoch before — now run it properly:
- Batch size: **32-64** (start at 64 if VRAM allows at 224×224 input; drop to 32 if you hit OOM).
- Epochs: **80-120**, with early stopping on validation macro-F1, patience 15.
- Optimizer: AdamW, weight decay 1e-4.
- Learning rate: 3e-4 for randomly-initialized layers (the classification head), 3e-5 for the ImageNet-pretrained backbone layers (discriminative LR) — cosine annealing schedule with a 5-epoch linear warmup.
- Mixed precision: on. Gradient clipping: max norm 1.0.
- Label smoothing: 0.1.
- Run this once on the full 4-wound-type dataset, and once more on the surgical-only subset, exactly as specified in the earlier external-data prompt — compare both before deciding which pretrained checkpoint to carry forward.
- Confirm this run alone (evaluated on the AZH dataset's own held-out split) reaches a *reasonable* macro-F1 (a sanity floor — e.g. meaningfully above random-chance for 4 classes, so notably above 25%) before using its weights for anything downstream. If it doesn't, something is wrong with the setup and needs debugging before proceeding, not just accepting a low number and moving on.

### 2c. Stage 2 — EfficientNetV2-S fine-tuning on SurgWound (fed from Stage 1's weights)
- Batch size: 32 (SurgWound is small — larger batches than this won't meaningfully help and reduce the number of gradient updates per epoch further).
- Two-phase training: (1) freeze backbone, train heads only, 15-20 epochs, head LR 1e-3; (2) unfreeze last 2-3 blocks, fine-tune end-to-end, 60-100 epochs, backbone LR 1e-5, head LR 1e-4, cosine schedule, early stopping on validation mean macro-F1, patience 15-20 given how noisy small-dataset validation curves can be.
- Mixed precision on, gradient clipping 1.0, label smoothing 0.1, weight decay 1e-4.

### 2d. DINOv2 / CLIP MLP heads (already working on CPU — now just faster and searchable)
- Batch size can go much higher now (128-256) since these are frozen embeddings feeding small MLPs — training is cheap.
- Epochs: 100-200 is affordable now; early stopping on validation macro-F1, patience 20.
- Run the Optuna hyperparameter search specified in the earlier high-performance prompt for real this time (30-50 trials per head is now affordable in minutes, not hours) — search LR, dropout, hidden layer width, and focal-loss γ.

### 2e. If fine-tuning DINOv2/CLIP's last layers (§6, optional)
- Batch size 16-32 (foundation models are large — watch VRAM), LR 1e-6 to 1e-5 on unfrozen layers only, 10-20 epochs, early stopping — these are large models, only a light touch is needed and appropriate here.

All of the above are starting defaults grounded in standard practice for this data/hardware scale, not guesses to accept blindly — run a short (5-10 epoch) sanity pass first on each stage to confirm loss is decreasing and nothing is misconfigured (wrong LR causing divergence, batch size causing OOM) before committing to a full run.

---

## 3. RE-RUN STAGE 0/1/2 PROPERLY

Follow the exact structure from the earlier external-data master prompt (`crop_to_roi.py`, domain pretraining variants, taxonomy mapping for the Wound Location head) — that design doesn't change, only the epoch counts, batch sizes, and hardware do. Re-run:
1. Stage 0 segmentation training and ROI cropping (§2a).
2. Stage 1 domain pretraining, both variants (§2b), with the sanity-floor check before proceeding.
3. Stage 2 SurgWound fine-tuning fed from the better Stage 1 checkpoint (§2c).
4. Re-run the domain-pretraining ablation row from the imbalance-fix prompt (§4/§5 there) with these real results, replacing the 1-epoch placeholder numbers — this time it's a legitimate experiment, not a hardware-constrained placeholder.

---

## 4. COMPLETE THE IMBALANCE-HANDLING STACK AT FULL SCALE

Everything specified in the class-imbalance master prompt and the majority-class-collapse fix prompt still applies — now run it completely rather than partially, since GPU speed removes the main reason to shortcut it:
1. Multi-label iterative stratified split (if not already fully applied) — confirm minority-class counts land correctly in every split and every CV fold.
2. Per-class support audit and merge decisions (Infection Risk Medium/High, Exudate Type subclasses, etc.) — finalize this decision now rather than leaving it open; document the final chosen label scheme clearly in the repo.
3. Class-balanced (effective number of samples) + focal loss, LDAM + DRW schedule, on both the MLP heads and the EfficientNetV2-S branch.
4. Decoupled two-stage training / τ-normalization on all branches.
5. Embedding-space SMOTE for the smallest surviving classes.
6. Per-class threshold tuning + logit adjustment at inference, tuned on validation, applied to the final ensemble.
7. Complete the full ablation table from the imbalance-fix prompt with every row filled from real GPU-scale runs — this table, filled in completely, is a required deliverable, not optional documentation.

---

## 5. ENSEMBLE RE-INTEGRATION — EARN THE SLOT, DON'T ASSUME IT

- Only fold the EfficientNetV2-S branch back into the ensemble if its **standalone validation macro-F1** (per head) is within a reasonable range of the DINOv2+CLIP branch's — if it's still dramatically worse on a given head, exclude it from that head's ensemble weighting specifically (per-head ensemble composition is fine — you don't need all three branches contributing to every head equally).
- Tune per-head ensemble weights on the validation set (not a flat average) as originally specified.
- Re-verify, as a sanity check, that no branch with near-random performance is silently pulling weight in the final ensemble — this was flagged as worth double-checking in the earlier collapse-fix conversation and applies even more once a newly retrained branch is added back in.

---

## 6. OPTIONAL — FINE-TUNE DINOV2/CLIP'S LAST LAYERS

Now that GPU is available, this was flagged as worth trying: unfreeze just the last 1-2 transformer blocks of DINOv2 and/or CLIP (not the whole backbone) and fine-tune lightly per §2e. Compare against the frozen-embedding version in the ablation table — this is a genuine experiment, include it whether it helps or not, and only keep it in the final model if it actually improves validation macro-F1 without overfitting (watch the train/val gap closely given how small SurgWound is).

---

## 7. FINAL METRICS REPORT

Produce a single, complete, final `metrics_report.md` that supersedes every partial version produced during CPU-only work:
- Full per-head metrics (accuracy, macro/weighted precision/recall/F1, confusion matrices, sensitivity/specificity on Infection-Risk-High and Urgency-Emergency specifically, ROC-AUC, PR-AUC, Cohen's Kappa, ECE) on val and test.
- Aggregate metrics (exact match ratio, Hamming loss, mean macro-F1).
- Bootstrap confidence intervals on minority-class F1.
- The complete ablation table (imbalance techniques + domain-pretraining variants) with every row filled from real runs.
- The target-tracking table against the 85% macro-F1 goal, per head, with honest notes on any head that still doesn't reach it and why (including if it's a genuine data-scarcity ceiling rather than a fixable modeling issue).
- 5-fold CV results (mean ± std) for the final configuration.

---

## 8. BUILD THE API AND REACT FRONTEND

Now that the model is finalized, build the application layer per the original full-app master prompt:
- **FastAPI backend**: `/predict` endpoint, ONNX Runtime inference (export the final ensemble/best model to ONNX, verify numerical parity against the PyTorch version), Pydantic response schemas, preprocessing pipeline matching training exactly (including the ROI-crop step from Stage 0).
- **React frontend** (Vite + TypeScript + Tailwind): drag-and-drop/camera photo upload, results screen with the color-coded urgency banner (Green/Yellow/Red) as the dominant visual element, infection-risk chip, per-attribute cards with confidence bars, auto-generated plain-language report paragraph, persistent non-diagnostic disclaimer.
- Keep the visual design clean and trustworthy — a normal-looking, uncluttered medical-app aesthetic, not a flashy AI-product look.

---

## 9. PACKAGING

- Docker Compose with two services (`api`, `web`), so the whole system runs with a single command on a new machine without manual environment setup.
- `.env` for configuration (API URL, model path, any secrets).
- Document GPU-vs-CPU inference: confirm the exported ONNX model runs correctly on CPU-only machines for deployment even though training required GPU — inference should not require the same hardware as training.

---

## 10. EXECUTION INSTRUCTIONS FOR THE AGENT

1. Read the existing repo fully before writing anything — confirm what's actually there matches the "state of the project" summary in §0, and note any differences.
2. Verify CUDA/GPU is actually active before starting any training run.
3. Run Stage 0/1/2 (§2-§3) with the specified hyperparameters, sanity-checking each stage before moving to the next.
4. Complete the full imbalance-handling stack (§4) and fill in every ablation table row with real results.
5. Re-integrate the ensemble per §5, and optionally attempt §6.
6. Produce the final, complete `metrics_report.md` (§7) — this is the single source of truth for how well the project actually performs; every number elsewhere (README, app copy) should trace back to it.
7. Build the API and frontend (§8), verify end-to-end locally (upload a real test image, confirm the full response renders correctly in the UI).
8. Package with Docker Compose (§9) and confirm a clean `docker compose up` works from a fresh clone.
9. Update the project README (use the earlier README master prompt, re-run it now that real final numbers, a working app, and a completed GPU training story exist to report — the "domain-adaptive pretraining" section of that README should now describe the real, GPU-scale result instead of the 1-epoch placeholder).
10. Do not report any number in the README, app, or final report that isn't traceable to an actual saved metrics file from this run — no estimates, no numbers carried over from the earlier CPU-constrained experiments once GPU-scale results supersede them.
