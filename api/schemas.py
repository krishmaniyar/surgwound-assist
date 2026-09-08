from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class AttributePrediction(BaseModel):
    label: str
    confidence: float

class PredictResponse(BaseModel):
    urgency_level: AttributePrediction = Field(..., description="Green, Yellow, or Red triage level")
    infection_risk: AttributePrediction = Field(..., description="Low, Medium, or High risk")
    wound_location: AttributePrediction
    healing_status: AttributePrediction
    closure_method: AttributePrediction
    exudate_type: AttributePrediction
    erythema: AttributePrediction
    edema: AttributePrediction
    report: str = Field(..., description="Plain-language generated report")
