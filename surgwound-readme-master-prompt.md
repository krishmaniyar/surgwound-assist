# MASTER PROMPT — Generate the Full Project Report README (SurgWound Assist)
*(Paste into Antigravity. Supersedes the prior README master prompt — every section now has deeper, more specific content requirements, and a new final section explains the tech stack, pipeline, and architecture in plain language for a non-technical reader. Length is not a constraint: depth and completeness are the priority throughout.)*

---

## 0. ROLE & GOAL

You are a technical writer with complete, accurate familiarity with this project's actual work: the SurgWound dataset, the multi-task foundation-model ensemble (DINOv2 + CLIP + EfficientNetV2-S), the class-imbalance diagnosis and treatment, the domain-adaptive pretraining experiment (including its honest negative result), and the planned React frontend and FastAPI backend. Write a **single, long, formally structured `README.md`** that reads as a thorough capstone/technical project report. Every section below must be written with real depth — multiple paragraphs per subsection where indicated, specific numbers pulled from actual project artifacts, and no placeholder or generic filler text. Where a section asks for detail, that means genuinely elaborate: explain reasoning, alternatives considered, and outcomes, not just a one-line summary per bullet.

---

## 1. STRUCTURE AND FORMATTING (follow exactly, unchanged from prior spec)

- **Abstract** — capitalize each word, bold, no heading number.
- **1. INTRODUCTION** — uppercase, bold, H1.
  - **1.1 Background**, **1.2 Motivations**, **1.3 Scope of the Project** — capitalize each word, normal weight, H2.
- **2. PROJECT DESCRIPTION AND GOALS** — uppercase, bold, H1.
  - **2.1 Literature Review**, **2.2 Research Gap**, **2.3 Objectives**, **2.4 Problem Statement**, **2.5 Project Plan** — H2, capitalize each word, normal weight.
- **3. TECHNICAL SPECIFICATION** — uppercase, bold, H1.
  - **3.1 Requirements** (H2) → **3.1.1 Functional**, **3.1.2 Non-Functional** (H3)
  - **3.2 Feasibility Study** (H2) → **3.2.1 Technical Feasibility**, **3.2.2 Economic Feasibility**, **3.2.3 Social Feasibility** (H3 — corrected numbering from the source outline's duplicate "3.2.2"; note the correction in an HTML comment at the top of the file)
  - **3.3 System Specification** (H2) → **3.3.1 Hardware Specification**, **3.3.2 Software Specification** (H3)
- **4. DESIGN APPROACH AND DETAILS** — uppercase, bold, H1.
  - **4.1 System Architecture** (H2)
  - **4.2 Design** (H2) → **4.2.1 Data Flow Diagram**, **4.2.2 Use Case Diagram**, **4.2.3 Class Diagram**, **4.2.4 Sequence Diagram** (H3)
- **5. REFERENCES** — uppercase, bold, H1.
- **6. TECH STACK AND PIPELINE — EXPLAINED SIMPLY** — uppercase, bold, H1. *(new — see §3 below)*

Page numbers from the original outline (`i`, `1`, `7`) don't apply to Markdown — omit them, keep the section numbering.

---

## 2. EXPANDED CONTENT REQUIREMENTS — SECTIONS 1 THROUGH 5

Write each of these as **multiple substantial paragraphs**, not single-sentence bullets. Where a list is natural (objectives, requirements), give each list item its own explanatory sentence or two, not just a label.

### Abstract
350-450 words. Cover, in order: the clinical problem, the dataset and its scale/constraints, the technical approach and *why* that approach was chosen over simpler alternatives, the honest headline results (both what worked and the imbalance/pretraining findings), and the intended real-world use and its explicit limitations.

### 1. Introduction
- **1.1 Background** — expand into: the nature of post-operative wound complications (infection, dehiscence, delayed healing) and why early visual signs matter clinically; the current gap between scheduled in-clinic follow-ups and what happens to a wound in between; how smartphone photography has changed what's technically possible for remote/asynchronous assessment; a short grounding paragraph on why AI-based wound image analysis has become an active research area (reference the CFP special issue context from the source datasets' READMEs as evidence this is a recognized active field, not a novel unprompted idea).
- **1.2 Motivations** — expand into: why this specific dataset (SurgWound) was chosen over larger but less clinically detailed alternatives; the appeal and difficulty of a *multi-attribute* task versus a simpler single-label classifier; personal/academic motivation — treating this as a genuine small-data, real-world-imbalanced ML problem rather than a toy dataset exercise; the value of building something patient-facing rather than only a research notebook.
- **1.3 Scope of the Project** — expand into explicit in-scope vs. out-of-scope subsections: **In scope** (8-attribute image classification, a reference web app, an honestly reported evaluation methodology, a documented imbalance-handling investigation); **Out of scope** (no clinical validation or regulatory clearance, no integration with EHR/clinical systems, no claim of diagnostic accuracy, no continuous/video monitoring, no multi-modal input beyond a single photo at this stage).

### 2. Project Description and Goals
- **2.1 Literature Review** — for each cited work (SurgWound-Bench; Wang et al. 2020 segmentation; Patel et al. 2024 and Anisuzzaman et al. 2022 classification-with-location; DINOv2; CLIP; Focal Loss; Class-Balanced Loss; LDAM-DRW; decoupled long-tail training; GradNorm; uncertainty task weighting; logit adjustment) — write a full paragraph: what the work did, what it found, and **specifically how it informed a decision in this project** (e.g. "Cui et al.'s effective-number-of-samples weighting was adopted directly for the per-head loss because plain inverse-frequency weighting was found to overcorrect on the smallest classes during the imbalance investigation, see §2.2 of the ablation history").
- **2.2 Research Gap** — expand with a comparison table (Markdown table) contrasting this project's problem framing against typical published wound-image work: dataset size, single-vs-multi-attribute labeling, class balance, and evaluation metric commonly used (accuracy vs. macro-F1) — then a paragraph stating the gap precisely.
- **2.3 Objectives** — expand each objective into a short paragraph covering what "done" looks like for it and how it was actually measured in this project (e.g. the macro-F1 target and per-class support threshold used to decide when a result is trustworthy vs. statistically meaningless).
- **2.4 Problem Statement** — expand into a two-part statement: the general ML problem (multi-task, multi-class, severely imbalanced, small-sample image classification) and the specific instantiation for this dataset (the 8 attributes, their class counts, and which ones proved hardest and why).
- **2.5 Project Plan** — rewrite as a full phase-by-phase narrative (not a table) covering: dataset acquisition and re-aggregation; baseline architecture selection and why (transfer learning necessity given 686 images); initial ensemble construction; metrics framework definition and why macro-F1/PR-AUC/bootstrap CIs were chosen over accuracy; the imbalance diagnosis process (majority-class collapse identified via per-class recall, not just aggregate scores); the imbalance-treatment stack applied; the domain-adaptive pretraining experiment, run at reduced scale due to CPU-only hardware, and its negative/inconclusive result, reported honestly rather than omitted; current status and near-term next steps (frontend/API integration, planned GPU retraining pass).

### 3. Technical Specification
- **3.1.1 Functional Requirements** — expand each requirement with a short user-story-style elaboration (e.g. "As a patient, I upload a photo of my incision site and receive, within a few seconds, a color-coded urgency indicator so I know whether to seek care immediately, within two days, or continue routine home care").
- **3.1.2 Non-Functional Requirements** — expand into explicit sub-points with target values where the project has them: inference latency target on CPU (state the actual target, e.g. under a few seconds via ONNX Runtime), reproducibility (fixed seeds, versioned configs, experiment tracking via Weights & Biases), data privacy handling of uploaded images (not persisted beyond the inference request unless explicitly stated otherwise), and the mandatory non-diagnostic disclaimer as a hard non-functional constraint on every result screen.
- **3.2.1 Technical Feasibility** — expand with the concrete evidence already gathered: frozen foundation-model embedding extraction proven feasible on modest hardware; the 1-epoch CPU-only EfficientNetV2-S pretraining run as a direct, honest data point on what is *not* yet feasible without GPU access; a clear statement of what compute tier is required for the next phase.
- **3.2.2 Economic Feasibility** — expand with an actual cost breakdown structure: one-time development cost (time, optional cloud GPU hours), zero licensing cost for the open-source stack, near-zero marginal inference cost once deployed via ONNX on CPU, and a note on dataset cost (freely available for research use, with attribution obligations).
- **3.2.3 Social Feasibility** — expand into: accessibility benefits (no special hardware beyond a smartphone camera), the ethical responsibility that comes with health-adjacent predictions (the disclaimer and urgency-escalation design exist specifically because of this), and data provenance/consent considerations for the underlying datasets (research-use annotated data, not proprietary patient data collected by this project).
- **3.3.1 Hardware Specification** — expand with two explicit sub-tables: (a) hardware actually used during this project's development so far, and (b) recommended hardware for the next training phase (GPU tier, approximate VRAM, estimated training time at that tier vs. the CPU baseline already observed).
- **3.3.2 Software Specification** — expand into a full version-pinned table: language/runtime versions, core ML libraries (PyTorch, timm, Albumentations, scikit-learn, ONNX Runtime), experiment tracking (Weights & Biases), API framework (FastAPI, Pydantic, Uvicorn), frontend stack (React, Vite, TypeScript, Tailwind CSS, react-dropzone), and any diagram/report tooling used to produce this README's own diagrams.

### 4. Design Approach and Details
- **4.1 System Architecture** — expand into a full walkthrough paragraph per stage of the pipeline (ingestion, preprocessing/ROI cropping, embedding extraction, per-attribute classification heads, ensemble combination, calibration/threshold tuning, report generation, API layer, frontend rendering), each paragraph explaining not just *what* the stage does but *why* it's designed that way given the project's specific constraints (small dataset, class imbalance, need for trustworthy confidence scores). Include the architecture diagram (Mermaid `flowchart`) after this narrative, not instead of it.
- **4.2.1 Data Flow Diagram** — Mermaid flowchart, labeled at every edge with the actual data object/type moving between stages (e.g. `raw JPEG` → `cropped ROI (PIL Image)` → `DINOv2/CLIP embedding (tensor)` → `per-head logits` → `calibrated probabilities` → `JSON response` → `rendered React UI`).
- **4.2.2 Use Case Diagram** — expand the actor/use-case list into full descriptions per use case (primary actor, trigger, main flow, alternate flow for low-confidence or failed uploads), plus the Mermaid representation.
- **4.2.3 Class Diagram** — expand to include attributes and method signatures (not just class names) for each core class (`WoundImage`, `PreprocessingPipeline`, `EmbeddingExtractor`, `AttributeClassifierHead`, `EnsembleCombiner`, `PredictionResult`, `ReportGenerator`, `APIController`), reflecting the real module structure already established across the training/API/imbalance master prompts for this project.
- **4.2.4 Sequence Diagram** — expand to include the error/edge-case branch explicitly (e.g. low-confidence prediction triggering an "uncertain — recommend clinical evaluation" fallback path), not just the happy path.

### 5. References
Same reference list as before, expanded with a one-line annotation after each entry describing its specific role in this project (annotated bibliography style), in the citation style chosen (state IEEE or APA at the top, use consistently).

---

## 3. NEW SECTION — 6. TECH STACK AND PIPELINE, EXPLAINED SIMPLY

This section exists for a **non-technical reader** — a family member, a clinician without an ML background, a recruiter skimming the README. No jargon without immediate plain-language explanation. Use analogies. This should be genuinely readable by someone who has never trained a model.

Write it with these subsections (unnumbered sub-headings are fine here, or use 6.1/6.2/6.3 if consistent numbering is preferred):

**"What the app actually does, in one paragraph"** — a single plain-language paragraph: patient takes a photo, the app looks at it and answers several practical questions about the wound (is it healing, is there swelling or redness, does it look infected, how urgently should you see someone), and shows the most important answer — how urgently to seek care — front and center.

**"The tech stack, explained like you're describing tools in a toolbox"** — go through each major technology and explain what it *is for*, not how it works internally, using a plain analogy for each:
- The AI models (DINOv2, CLIP, EfficientNetV2-S) — explain as "pre-trained expert eyes" that have already looked at millions of general images and learned to notice shapes, textures, and patterns, which this project then teaches to specialize in wound photos specifically, the way an experienced photographer could be taught to specialize in medical photography faster than training someone from zero.
- PyTorch — the workshop/toolset used to actually build and train the models.
- The classification "heads" — explain as eight separate small decision-makers, each looking at the same photo's processed understanding and answering one specific question (location, healing status, infection risk, etc.), rather than one decision-maker trying to answer everything at once.
- The imbalance-handling techniques — explain in plain terms as "making sure the model doesn't just learn to guess the most common answer every time" — use a simple analogy (e.g. a student who does well on a test by always picking "B" if most answers happen to be B, versus a student who actually learns to tell the answers apart).
- FastAPI / the backend — explain as the "receptionist" that takes the uploaded photo, sends it to the right places, and hands back an organized answer.
- React / the frontend — explain as the actual screen and buttons the patient sees and taps.
- ONNX — explain as a "universal translator" that lets the trained model run quickly on ordinary computers without needing the original heavy training software.

**"The pipeline, step by step, in plain language"** — walk through the same flow as §4.1's architecture, but rewritten with zero jargon: photo goes in → the photo gets automatically cropped to focus on the wound itself (so background clutter doesn't confuse things) → the "expert eyes" models look at the cropped photo and turn what they see into a compact internal description → eight small decision-makers each answer their one question from that description → the answers get double-checked and adjusted so rare-but-important situations (like signs of infection) aren't missed just because they're rare in the training examples → all eight answers get turned into a short plain-language summary and a color-coded urgency signal → that summary gets sent back and displayed to the patient.

**"Why it's built this way, in plain language"** — a short closing paragraph translating the core engineering decision into plain terms: because there were only a few hundred example photos to learn from (far fewer than typical AI projects), the project leaned on models that had already learned from huge amounts of *other* images first, and put a lot of deliberate effort into making sure rare-but-serious cases weren't drowned out by more common, milder ones — because in a wound-checking tool, missing a serious case is a far worse mistake than a false alarm.

---

## 4. HONESTY REQUIREMENT (unchanged, reiterated)

Every section, including the new plain-language one, must reflect actual project findings — the imbalance-driven low macro-F1 on several attributes, the inconclusive domain-pretraining experiment, and current incomplete status (frontend/GPU retraining pending) — described honestly rather than smoothed over, in both the formal sections and the plain-language section alike. The plain-language section in particular should not oversell the tool's current accuracy just because it's written for a lay audience — if anything, that audience most needs the honest caveat stated simply and clearly.

---

## 5. EXECUTION INSTRUCTIONS FOR THE AGENT

1. Pull real figures, dataset stats, and architecture details from the project's existing files (training logs, metrics_report.md, ablation tables) before writing — do not invent numbers.
2. Draft Sections 1-5 in full expanded depth per §2 above, in the exact heading structure and formatting from §1.
3. Generate all four diagrams in §4.2 as valid Mermaid code, verified to render without syntax errors.
4. Draft Section 6 last, once the technical sections are final, so the plain-language version stays consistent with the real pipeline described in Section 4 — cross-check the two for consistency before finishing.
5. Assemble the complete `README.md`; do a final pass checking every heading against the formatting spec, and confirm no section was compressed for length — depth and completeness take priority over brevity throughout.
