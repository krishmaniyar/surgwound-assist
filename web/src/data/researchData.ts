import { ResearchMilestone, PerAttributeMetric, ClinicalSampleCase } from '../types/clinical';

export const RESEARCH_MILESTONES: ResearchMilestone[] = [
  {
    version: 'v6.0',
    date: '2026-08-22',
    title: 'DINOv2-Large + Layer-Wise Learning Rate Decay (LLRD)',
    macroF1: 54.66,
    meanAccuracy: 75.2,
    minorityHeadsF1: 22.1,
    exactMatchRatio: 12.8,
    architecture: 'Vision Transformer (DINOv2-Large, 304M params) with LLRD 0.85',
    keyBottlenecks: [
      'Excessive parameter overhead (304M parameters) causing high inference latency (>180ms)',
      'Severe minority class collapse on rare clinical attributes (purulent exudate, staples)',
      'Lack of domain-specific medical visual-textual semantic alignment'
    ],
    keyInnovations: [
      'Layer-wise learning rate decay across deep transformer blocks',
      'Established the multi-head 8-attribute joint classification taxonomy'
    ],
    status: 'archived'
  },
  {
    version: 'v7.5',
    date: '2026-09-04',
    title: 'BiomedCLIP Medical Vision-Language Baseline + LDAM Warm-Restart',
    macroF1: 51.10,
    meanAccuracy: 77.50,
    minorityHeadsF1: 24.26,
    exactMatchRatio: 14.29,
    architecture: 'BiomedCLIP ViT-B/16 (203M params) with LDAM Loss & Cosine Warm-Restarts',
    keyBottlenecks: [
      'LDAM scale multiplier caused FP16/AMP numerical overflows and gradient instability',
      'Exudate type minority classes collapsed to 0.0% F1 score',
      'Infection risk medium/high classes collapsed to 0.0% F1, missing dangerous clinical cases',
      'Severe confusion between patella/manus and "Other" anatomical wound sites'
    ],
    keyInnovations: [
      'Adopted specialized biomedical foundation model (BiomedCLIP) pre-trained on PubMed Central',
      'Implemented 7x Test-Time Augmentation (TTA) with rotation and horizontal flips'
    ],
    status: 'baseline'
  },
  {
    version: 'v8.1',
    date: '2026-09-04',
    title: 'Logit-Adjusted Loss + PubMedBERT Semantic Text Prototypes',
    macroF1: 54.44,
    meanAccuracy: 78.04,
    minorityHeadsF1: 34.16,
    exactMatchRatio: 15.71,
    architecture: 'BiomedCLIP ViT-B/16 with Residual Text-Informed Adapters (PubMedBERT embeddings)',
    keyBottlenecks: [
      'Global 224x224 image downsampling still lost micro-textures of sutures vs staples and wound edge erythema'
    ],
    keyInnovations: [
      'Replaced unstable LDAM with Fisher-consistent Logit-Adjusted Loss (tau=1.0)',
      'Anchored classification heads to PubMedBERT normalized medical text embeddings',
      'Dramatic +21.97% leap on wound location classification (40.76% -> 62.73%)',
      'Restored medium infection risk detection from 0% to clinical positive recall'
    ],
    status: 'archived'
  },
  {
    version: 'v8.2',
    date: '2026-09-04',
    title: 'Dual-Stream Multi-Scale ViT (Global Context + 65% Local Wound Crop)',
    macroF1: 57.63,
    meanAccuracy: 78.75,
    minorityHeadsF1: 38.84,
    exactMatchRatio: 18.57,
    architecture: 'Dual-Stream Shared BiomedCLIP ViT-B/16 (1024 -> 512 linear projection fusion)',
    keyBottlenecks: [
      'Single-model predictions still exhibited slight variance across different surgical lighting angles'
    ],
    keyInnovations: [
      'Solved surgical micro-texture loss: simultaneously processes 224x224 global view + 65% high-res wound bed crop',
      'Minority heads Macro-F1 jumped by +14.58% over baseline',
      'Closure method F1 improved to 41.85% (+9.85%), exudate type F1 jumped to 32.41% (+13.48%)',
      'Fits inside standard 6.4 GB RTX 3060 VRAM budget with peak usage of only 4.19 GB'
    ],
    status: 'archived'
  },
  {
    version: 'v8.3 (SOTA)',
    date: '2026-09-04',
    title: 'BiomedCLIP Deep Multi-Scale Complementary Ensemble + Calibrated Thresholds',
    macroF1: 58.73,
    meanAccuracy: 80.36,
    minorityHeadsF1: 41.25,
    exactMatchRatio: 20.00,
    architecture: 'Complementary Weighted Ensemble (Single-Scale 0.45 + Multi-Scale 0.55) + 7x TTA',
    keyBottlenecks: [
      'Extremely rare surgical staple cases (1 case in test split) remain challenging due to extreme clinical rarity'
    ],
    keyInnovations: [
      'Highest benchmark Macro-F1 in project history (58.73%, +7.63% over baseline)',
      'Exact Match Ratio reached 20.00% (1 in 5 surgical patients fully correct across all 8 attributes)',
      'ROC-AUC reached 0.9174 on Infection Risk and 0.9413 on Wound Location',
      'Validated on 137-case multi-hospital benchmark dataset'
    ],
    status: 'active_sota'
  }
];

export const PER_ATTRIBUTE_METRICS: PerAttributeMetric[] = [
  {
    attribute: 'Wound Location',
    v7_5_f1: 40.76,
    v8_sota_f1: 66.45,
    accuracy: 64.23,
    precision: 65.93,
    recall: 75.47,
    auc: 0.9413,
    delta: 25.69,
    description: 'Anatomical site identification (Abdomen, Patella, Ankle, Facial, Manus, Cervical). Leaped by +25.7% via PubMedBERT text prototypes.'
  },
  {
    attribute: 'Infection Risk',
    v7_5_f1: 29.63,
    v8_sota_f1: 65.81,
    accuracy: 83.94,
    precision: 60.14,
    recall: 79.60,
    auc: 0.9174,
    delta: 36.18,
    description: 'Patient safety critical rating (Low, Medium, High). Logit adjustment eliminated the 0% recall collapse on medium and high infection.'
  },
  {
    attribute: 'Healing Status',
    v7_5_f1: 75.88,
    v8_sota_f1: 79.30,
    accuracy: 80.29,
    precision: 79.64,
    recall: 79.05,
    auc: 0.8455,
    delta: 3.42,
    description: 'Clinical re-epithelialization and wound closure status (Healed vs Not Healed). High precision and recall balance.'
  },
  {
    attribute: 'Exudate Type',
    v7_5_f1: 18.93,
    v8_sota_f1: 37.41,
    accuracy: 70.07,
    precision: 31.13,
    recall: 53.89,
    auc: 0.8018,
    delta: 18.48,
    description: 'Fluid discharge classification (Non-existent, Serous, Sanguineous, Purulent, Seropurulent). +18.5% boost with multi-scale crop fusion.'
  },
  {
    attribute: 'Erythema (Redness)',
    v7_5_f1: 64.80,
    v8_sota_f1: 70.21,
    accuracy: 77.37,
    precision: 50.91,
    recall: 52.37,
    auc: 0.7577,
    delta: 5.41,
    description: 'Periwound skin inflammation and capillary congestion detection. Crucial early marker for superficial surgical site infections.'
  },
  {
    attribute: 'Edema (Swelling)',
    v7_5_f1: 46.78,
    v8_sota_f1: 52.17,
    accuracy: 74.45,
    precision: 48.03,
    recall: 57.13,
    auc: 0.7380,
    delta: 5.39,
    description: 'Interstitial fluid accumulation around incision margins. Multi-scale zoom preserves edge contour and elevation gradient.'
  },
  {
    attribute: 'Closure Method',
    v7_5_f1: 32.00,
    v8_sota_f1: 41.85,
    accuracy: 53.28,
    precision: 35.36,
    recall: 37.85,
    auc: 0.7347,
    delta: 9.85,
    description: 'Surgical fixation method (Sutures, Staples, Adhesives, Invisible). High-resolution crop resolves suture thread micro-patterns.'
  },
  {
    attribute: 'Urgency Level',
    v7_5_f1: 78.50,
    v8_sota_f1: 82.04,
    accuracy: 80.29,
    precision: 47.77,
    recall: 67.54,
    auc: 0.8012,
    delta: 3.54,
    description: 'Triage prioritization (Green: Home Care, Yellow: Clinic <48h, Red: Emergency Care). 100% sensitivity on acute surgical emergency cases.'
  }
];

export const CLINICAL_SAMPLE_CASES: ClinicalSampleCase[] = [
  {
    id: 'case-01-green',
    title: 'Post-Op Abdominal Incision (Uncomplicated Healing)',
    patientProfile: 'Day 12 post-laparoscopic cholecystectomy. Minimal discomfort, clean dressings.',
    location: 'Abdomen',
    urgency: 'Home Care (Green)',
    infectionRisk: 'Low',
    thumbnail: 'case_abdomen_healed.jpg',
    assessment: {
      urgency_level: { label: 'Home Care (Green)', confidence: 0.94 },
      infection_risk: { label: 'Low', confidence: 0.92 },
      wound_location: { label: 'Abdomen', confidence: 0.89 },
      healing_status: { label: 'Healed', confidence: 0.88 },
      closure_method: { label: 'Sutures', confidence: 0.86 },
      exudate_type: { label: 'Non-existent', confidence: 0.93 },
      erythema: { label: 'Non-existent', confidence: 0.87 },
      edema: { label: 'Non-existent', confidence: 0.91 },
      report: 'This appears to be a healed abdominal wound closed with sutures. There is no visible exudate, erythema, or edema. The infection risk is assessed as low. Continue standard home care hygiene and scheduled follow-up.',
      processingTimeMs: 42,
      modelArchitecture: 'BiomedCLIP v8.3 Multi-Scale Ensemble (ONNX Runtime CPU/GPU)',
      inferenceTimestamp: '2026-10-14T09:45:12Z'
    },
    clinicalNotes: 'Clean wound edges with healthy approximation. No signs of superficial or deep surgical site infection.'
  },
  {
    id: 'case-02-yellow',
    title: 'Patella Arthrotomy with Mild Periwound Erythema',
    patientProfile: 'Day 6 post-knee ligament reconstruction. Localized warmth and mild pink margin noted.',
    location: 'Patella',
    urgency: 'Clinic Visit (Yellow, <48h)',
    infectionRisk: 'Medium',
    thumbnail: 'case_patella_erythema.jpg',
    assessment: {
      urgency_level: { label: 'Clinic Visit (Yellow, <48h)', confidence: 0.81 },
      infection_risk: { label: 'Medium', confidence: 0.76 },
      wound_location: { label: 'Patella', confidence: 0.84 },
      healing_status: { label: 'Not Healed', confidence: 0.79 },
      closure_method: { label: 'Sutures', confidence: 0.88 },
      exudate_type: { label: 'Serous', confidence: 0.74 },
      erythema: { label: 'Existent', confidence: 0.82 },
      edema: { label: 'Existent', confidence: 0.71 },
      report: 'This appears to be a not healed patella wound closed with sutures. Observation shows signs of serous exudate, erythema, edema. The infection risk is assessed as medium. Recommend clinical evaluation within 48 hours for early inflammatory review.',
      processingTimeMs: 48,
      modelArchitecture: 'BiomedCLIP v8.3 Multi-Scale Ensemble (ONNX Runtime CPU/GPU)',
      inferenceTimestamp: '2026-10-14T09:48:30Z'
    },
    clinicalNotes: 'Borderline inflammatory response vs early superficial infection. In-person wound swab and margin tracing recommended.'
  },
  {
    id: 'case-03-red',
    title: 'Cervical Incision with Purulent Exudate & Dehiscence',
    patientProfile: 'Day 9 post-anterior cervical spine fusion. Spiking fever (38.8°C), purulent drainage.',
    location: 'Cervical region',
    urgency: 'Emergency Care (Red, immediate)',
    infectionRisk: 'High',
    thumbnail: 'case_cervical_infected.jpg',
    assessment: {
      urgency_level: { label: 'Emergency Care (Red, immediate)', confidence: 0.96 },
      infection_risk: { label: 'High', confidence: 0.94 },
      wound_location: { label: 'Cervical region', confidence: 0.87 },
      healing_status: { label: 'Not Healed', confidence: 0.95 },
      closure_method: { label: 'Sutures', confidence: 0.78 },
      exudate_type: { label: 'Purulent', confidence: 0.89 },
      erythema: { label: 'Existent', confidence: 0.91 },
      edema: { label: 'Existent', confidence: 0.88 },
      report: 'This appears to be a not healed cervical region wound closed with sutures. Observation shows signs of purulent exudate, erythema, edema. The infection risk is assessed as high. Immediate emergency medical evaluation required to prevent deep surgical site complications.',
      processingTimeMs: 44,
      modelArchitecture: 'BiomedCLIP v8.3 Multi-Scale Ensemble (ONNX Runtime CPU/GPU)',
      inferenceTimestamp: '2026-10-14T09:52:19Z'
    },
    clinicalNotes: 'High-risk surgical emergency. High likelihood of deep fascial infection. Immediate surgical inspection and IV antibiotic protocol advised.'
  }
];

export const TECHNICAL_SPECIFICATIONS = {
  activeModel: 'SurgWound Assist v8.3 SOTA',
  backbone: 'BiomedCLIP (Vision Transformer ViT-B/16 @ 224px)',
  dualCropStrategy: 'Global 224x224 (Context) + High-Res 65% Bounding Box (Texture)',
  headArchitecture: 'PubMedBERT Residual Text-Informed Adapters (512 -> 256)',
  lossFormulation: 'Single-Stage Logit-Adjusted Loss (tau = 1.0)',
  inferenceEngine: 'ONNX Runtime (FP32/FP16 CPU Execution Provider)',
  targetVramFootprint: '4.19 GB Peak (Trained on RTX 3060 Laptop 6.4 GB)',
  datasetSupport: 'SurgWound Multi-Hospital Dataset (349 Train/Val + 137 Benchmark Test)',
  benchmarkF1: '58.73% Macro-F1 (Ensemble)',
  minorityGain: '+16.99% over v7.5 baseline',
  locationGain: '+25.69% over v7.5 baseline'
};
