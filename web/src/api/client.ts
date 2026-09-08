import axios from 'axios';

// Type definitions for API
export interface AttributePrediction {
    label: string;
    confidence: number;
}

export interface PredictResponse {
    urgency_level: AttributePrediction;
    infection_risk: AttributePrediction;
    wound_location: AttributePrediction;
    healing_status: AttributePrediction;
    closure_method: AttributePrediction;
    exudate_type: AttributePrediction;
    erythema: AttributePrediction;
    edema: AttributePrediction;
    report: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
    baseURL: API_URL,
});

export const predictWound = async (file: File): Promise<PredictResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post<PredictResponse>('/predict', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    
    return response.data;
};
