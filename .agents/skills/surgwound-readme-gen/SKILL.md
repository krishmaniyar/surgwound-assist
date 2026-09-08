---
name: surgwound-readme-gen
description: Protocol, standards, and automation guidelines for generating and maintaining the research-paper-grade README for SurgWound Assist across all model iterations.
---

# SurgWound Assist — Research Paper README Generation Skill

This skill defines the exact standards, section structures, metric schemas, diagram conventions, and verification checklists required to maintain and generate the **Root `README.md`** at the standard of a peer-reviewed machine learning publication (e.g., IEEE JBHI, Nature Scientific Reports, MICCAI).

---

## 1. Core Philosophy & Lead ML Engineer Persona

1. **Publication-Grade Rigor**: The `README.md` is not a cursory summary; it is designed to be the foundational draft of an entire research paper. Every claim must be backed by empirical numbers, confusion matrices, mathematical formulations, and literature citations.
2. **Brutal Scientific Honesty & Baseline Alignment**: Never hide regressions, zero-F1 minority collapse, or negative results. Detail the exact failure mode (e.g., small-sample logit adjustment under $\tau=1.0$, single-class annotation mismatches causing N/A ROC-AUC). Explicitly benchmark against the base paper (**SurgWound-Bench**, Xu et al., 2024, The Ohio State University Wexner Medical Center).
3. **Full Dataset Mandate (686 Images)**: All final benchmark specifications must reflect the complete official 686-image dataset (`480 train / 69 val / 137 test`), not partial subsets.
4. **General MLLMs vs. Domain-Specialized Architecture Analysis**:
   - Contrast commercial/general MLLMs (GPT-4o, Claude-3.5, Gemini-1.5, Qwen2.5-VL) tested in the base paper with SurgWound Assist's specialized domain approach.
   - Highlight why general MLLMs fail (0% F1 on high infection risk and emergency care due to web pre-training, visual downsampling of suture knots, and lack of long-tail loss adjustment).
   - Detail why SurgWound Assist's unified single-stage dual-stream BiomedCLIP model is superior to the base paper's 3-stage, 7-model chained pipeline (WoundQwen): predicts all 8 attributes end-to-end (including location, which the base paper assumes as known metadata), runs in 1.8s on consumer hardware instead of requiring multi-GPU clusters, and prevents multi-stage error compounding.
5. **Comprehensive Metrics Suite**: Always report the full suite aligned with the base benchmark paper (`base-paper.pdf` Tables 2, 3, 4):
   - Macro-F1 (primary metric)
   - Accuracy
   - Macro-Precision & Macro-Recall
   - Micro-F1 & Weighted-F1
   - One-vs-Rest ROC-AUC (per head and mean)
   - Cohen's Kappa (chance-adjusted agreement)
   - Minority-Heads Macro-F1 (`exudate_type`, `infection_risk`, `closure_method`, `edema`)
   - Exact Match Ratio (subset accuracy across all 8 attributes simultaneously)
6. **Multi-Audience Accessibility**: Combine deep mathematical and architectural specifications with a dedicated plain-language translation section for non-technical clinicians, healthcare professionals, and patients.

---

## 2. Standard Document Architecture (Mandatory Sections)

Every generated `README.md` must adhere to this 11-part canonical structure:

```text
Title & Header
├── Abstract (350–450 words, structured narrative)
├── 1. INTRODUCTION
│   ├── 1.1 Clinical Background & Surgical Site Infection (SSI) Burden
│   ├── 1.2 Telemedicine & Remote Post-Operative Visual Assessment Gap
│   ├── 1.3 Motivations: Multi-Task Dense Medical Representation
│   └── 1.4 Project Scope: Explicit In-Scope vs. Out-of-Scope Boundaries
├── 2. RELATED WORK & RESEARCH GAP
│   ├── 2.1 Literature Review (Annotated Analysis of Prior Approaches)
│   ├── 2.2 Foundation Models in Medical Computer Vision
│   ├── 2.3 Long-Tailed Learning & Decoupled Representation Formulations
│   └── 2.4 Research Gap (Comparative Markdown Matrix)
├── 3. PROBLEM FORMULATION & DATASET CHARACTERISTICS
│   ├── 3.1 Mathematical Formulation of Multi-Task Attribute Prediction
│   ├── 3.2 The SurgWound Dataset: Structure, Labels & 8 Attributes
│   ├── 3.3 Severe Long-Tail Class Imbalance Audit (3x to 63x Ratios)
│   └── 3.4 Data Integrity, Split Isolation (Train/Val/Test), and Leakage Prevention
├── 4. ARCHITECTURAL DESIGN & METHODOLOGY
│   ├── 4.1 Backbone Evolution: From CNNs to Multi-Scale BiomedCLIP
│   ├── 4.2 Multi-Scale Dual-Stream Visual Encoding (Global + Detail Crop)
│   ├── 4.3 Semantic Prior Grounding via PubMedBERT Clinical Text Prototypes
│   ├── 4.4 Decoupled Loss Strategies: LDAM vs. Logit Adjustment vs. Balanced Softmax
│   ├── 4.5 Multi-Task Class-Balanced Mini-Batch Sampling (WeightedRandomSampler)
│   ├── 4.6 Optimization Dynamics: LLRD, Cosine Warmup & GradScaler Stability
│   └── 4.7 Inference Pipeline: 7x Test-Time Augmentation & Decision Thresholding
├── 5. SYSTEM & ARCHITECTURAL DIAGRAMS (Mermaid)
│   ├── 5.1 End-to-End Multi-Scale Visual Processing Pipeline (Flowchart)
│   ├── 5.2 Multi-Task Attribute Classification Heads & Loss Flow
│   ├── 5.3 System Data Flow Diagram (DFD)
│   ├── 5.4 Use Case Diagram (Patient Triage & Clinical Escalation)
│   ├── 5.5 Software Class Diagram (Core Modules & Signatures)
│   └── 5.6 Execution Sequence Diagram (Happy Path & Fallback Logic)
├── 6. COMPREHENSIVE BENCHMARK RESULTS & ABLATION STUDY
│   ├── 6.1 Head-to-Head Evolution Table (v1.0 to Current SOTA)
│   ├── 6.2 Per-Attribute Benchmark Matrix (Aligned with Base Paper Tables)
│   ├── 6.3 Deep Multi-Model Ensembling Ablation (Single vs Dual vs Tri-Ensemble)
│   └── 6.4 Key Empirical Takeaways & Hypothesis Testing
├── 7. PER-ATTRIBUTE & PER-CLASS ERROR ANALYSIS
│   ├── 7.1 Detailed Attribute Breakdowns (Precision, Recall, F1, Support)
│   ├── 7.2 Root Cause Diagnosis of Zero-F1 Minority Classes (Staples, Seropurulent, High Risk)
│   └── 7.3 Mathematical Diagnosis & Resolution of N/A ROC-AUC and Cohen's Kappa
├── 8. TECHNICAL SPECIFICATIONS & REPRODUCIBILITY
│   ├── 8.1 Hardware Specifications (Development vs Production Profiles)
│   ├── 8.2 Software Environment & Pinned Dependency Manifest
│   └── 8.3 Determinism & Seed Protocol
├── 9. CLINICAL GOVERNANCE, LIMITATIONS & ETHICAL GUARDRAILS
│   ├── 9.1 Non-Diagnostic Decision Support Disclaimer
│   ├── 9.2 Conservative Urgency Triage Escalation Strategy
│   └── 9.3 Data Privacy, Ephemeral Processing & Bias Considerations
├── 10. REFERENCES (Formal Academic Bibliography)
└── 11. TECH STACK AND PIPELINE — EXPLAINED SIMPLY
    ├── 11.1 What the Application Does in One Paragraph
    ├── 11.2 The Tech Stack Explained with Analogies
    ├── 11.3 The Pipeline Step-by-Step in Plain Language
    └── 11.4 Why It Is Engineered This Way
```

---

## 3. Data Sources for Metrics & Figures

When generating or updating the README, NEVER fabricate numbers. Extract directly from:
1. `v8/experiments/experiment_registry.csv`: Run IDs, test macro-F1, minority F1, validation peak, date, parameters.
2. `v8/runs/<latest_best_run>/evaluation_report.md`: Granular per-head Accuracy, Precision, Recall, Macro-F1, Micro-F1, Weighted-F1, ROC-AUC, Cohen's Kappa, and per-class support.
3. `v8/runs/<latest_best_run>/metrics.json`: Machine-readable raw metrics dictionary.
4. `docs/best_evaluation_report.md`: Current all-time champion evaluation document.
5. `archive/dataset_backup_v7/annotations.csv`: Ground truth label counts, class distributions, and split numbers.

---

## 4. Mermaid Diagram Style Standards

To ensure Mermaid renders cleanly on GitHub and Markdown viewers:
1. **Quote node text** containing parentheses, brackets, or math symbols: `id["Linear(1024 -> 512)"]`.
2. **Avoid HTML tags** (`<br>`, `<b>`) inside node labels.
3. **Use consistent structural flows**:
   - `graph TD` or `flowchart TD` for pipelines
   - Clear edge labels: `A -->|Tensor [B, 512]| B`
   - Explicit subgraphs grouping Backbone, Multi-Task Heads, and Loss Computation.

---

## 5. Automation Workflow Checklist

When updating `README.md` after a major experiment:
- [ ] Pull latest metrics from `docs/best_evaluation_report.md` or latest run directory.
- [ ] Verify test macro-F1, ROC-AUC, Cohen's Kappa, and minority-heads F1 match the latest logs.
- [ ] Update the Architecture Evolution Table in §6.1 with new version rows.
- [ ] Check that all 8 attributes are documented in §6.2 and §7.1.
- [ ] Ensure all Mermaid diagrams compile without syntax errors.
- [ ] Confirm the clinical disclaimer and ethical guardrails in §9 are intact.
- [ ] Validate that Section 11 (Plain-Language Guide) is updated with any new architectural metaphors.
