export type TriageUrgency = 'Home Care (Green)' | 'Clinic Visit (Yellow, <48h)' | 'Emergency Care (Red, immediate)';
export type InfectionRisk = 'Low' | 'Medium' | 'High';

export interface AttributePrediction {
  label: string;
  confidence: number;
  topK?: { label: string; score: number }[];
}

export interface SurgWoundAssessment {
  urgency_level: AttributePrediction;
  infection_risk: AttributePrediction;
  wound_location: AttributePrediction;
  healing_status: AttributePrediction;
  closure_method: AttributePrediction;
  exudate_type: AttributePrediction;
  erythema: AttributePrediction;
  edema: AttributePrediction;
  report: string;
  processingTimeMs: number;
  modelArchitecture: string;
  inferenceTimestamp: string;
}

export interface ResearchMilestone {
  version: string;
  date: string;
  title: string;
  macroF1: number;
  meanAccuracy: number;
  minorityHeadsF1: number;
  exactMatchRatio: number;
  architecture: string;
  keyBottlenecks: string[];
  keyInnovations: string[];
  status: 'archived' | 'baseline' | 'active_sota';
}

export interface PerAttributeMetric {
  attribute: string;
  v7_5_f1: number;
  v8_sota_f1: number;
  accuracy: number;
  precision: number;
  recall: number;
  auc: number;
  delta: number;
  description: string;
}

export interface ClinicalSampleCase {
  id: string;
  title: string;
  patientProfile: string;
  location: string;
  urgency: TriageUrgency;
  infectionRisk: InfectionRisk;
  thumbnail: string;
  assessment: SurgWoundAssessment;
  clinicalNotes: string;
}
