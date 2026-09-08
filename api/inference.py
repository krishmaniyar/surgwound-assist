import onnxruntime as ort
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from schemas import PredictResponse, AttributePrediction

# Needs to match ML training
CLASS_MAPPINGS = {
    'location': ['Abdomen', 'Patella', 'Ankle', 'Facial region', 'Manus', 'Cervical region', 'Other', 'Uncertain'],
    'healing_status': ['Healed', 'Not Healed'],
    'closure_method': ['Invisible', 'Sutures', 'Staples', 'Adhesives', 'Uncertain'],
    'exudate_type': ['Non-existent', 'Serous', 'Sanguineous', 'Purulent', 'Seropurulent', 'Uncertain'],
    'erythema': ['Non-existent', 'Existent', 'Uncertain'],
    'edema': ['Non-existent', 'Existent', 'Uncertain'],
    'infection_risk': ['Low', 'Medium', 'High'],
    'urgency_level': ['Home Care (Green)', 'Clinic Visit (Yellow, <48h)', 'Emergency Care (Red, immediate)']
}

# Ordered based on how model heads will output them in ONNX
# This should match the output order in export_onnx.py
ORDERED_ATTRIBUTES = list(CLASS_MAPPINGS.keys())

class SurgWoundInferenceModel:
    def __init__(self, model_path="model.onnx"):
        try:
            self.session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
            self.input_name = self.session.get_inputs()[0].name
            print(f"Loaded ONNX model from {model_path}")
        except Exception as e:
            print(f"Warning: Could not load ONNX model: {e}")
            self.session = None
            
        self.transform = A.Compose([
            A.Resize(256, 256),
            A.CenterCrop(224, 224),
            A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ])
        
    def softmax(self, x):
        e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
        return e_x / e_x.sum(axis=1, keepdims=True)

    def preprocess(self, image):
        img_array = np.array(image)
        augmented = self.transform(image=img_array)
        img_array = augmented['image']
        
        # HWC to CHW
        img_array = np.transpose(img_array, (2, 0, 1))
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
        return img_array

    def generate_report(self, preds):
        """
        Generate a plain-language report based on the 8 predicted attributes.
        Example: "This appears to be a healed abdominal wound closed with sutures, with no visible exudate, erythema, or edema..."
        """
        healing = preds['healing_status']['label'].lower()
        location = preds['location']['label'].lower()
        closure = preds['closure_method']['label'].lower()
        
        if location == "other" or location == "uncertain":
            loc_str = "wound"
        else:
            loc_str = f"{location} wound"
            
        if closure == "uncertain":
            closure_str = ""
        else:
            closure_str = f" closed with {closure}"
            
        report = f"This appears to be a {healing} {loc_str}{closure_str}. "
        
        exudate = preds['exudate_type']['label'].lower()
        erythema = preds['erythema']['label'].lower()
        edema = preds['edema']['label'].lower()
        
        issues = []
        if exudate not in ["non-existent", "uncertain"]:
            issues.append(f"{exudate} exudate")
        if erythema == "existent":
            issues.append("erythema")
        if edema == "existent":
            issues.append("edema")
            
        if not issues:
            if exudate == "non-existent" and erythema == "non-existent" and edema == "non-existent":
                report += "There is no visible exudate, erythema, or edema. "
        else:
            report += f"Observation shows signs of {', '.join(issues)}. "
            
        inf_risk = preds['infection_risk']['label'].lower()
        report += f"The infection risk is assessed as {inf_risk}."
        
        return report

    def predict(self, image) -> PredictResponse:
        if self.session is None:
            # Mock response for testing frontend without model
            return self._mock_predict()
            
        input_tensor = self.preprocess(image)
        
        # Run inference
        ort_inputs = {self.input_name: input_tensor}
        ort_outs = self.session.run(None, ort_inputs)
        
        # Process outputs
        preds = {}
        for i, attr in enumerate(ORDERED_ATTRIBUTES):
            logits = ort_outs[i]
            probs = self.softmax(logits)[0]
            pred_idx = np.argmax(probs)
            confidence = float(probs[pred_idx])
            label = CLASS_MAPPINGS[attr][pred_idx]
            
            preds[attr] = {
                'label': label,
                'confidence': confidence
            }
            
        report = self.generate_report(preds)
        
        return PredictResponse(
            urgency_level=AttributePrediction(**preds['urgency_level']),
            infection_risk=AttributePrediction(**preds['infection_risk']),
            wound_location=AttributePrediction(**preds['location']),
            healing_status=AttributePrediction(**preds['healing_status']),
            closure_method=AttributePrediction(**preds['closure_method']),
            exudate_type=AttributePrediction(**preds['exudate_type']),
            erythema=AttributePrediction(**preds['erythema']),
            edema=AttributePrediction(**preds['edema']),
            report=report
        )

    def _mock_predict(self) -> PredictResponse:
        preds = {attr: {'label': CLASS_MAPPINGS[attr][0], 'confidence': 0.95} for attr in ORDERED_ATTRIBUTES}
        report = self.generate_report(preds)
        return PredictResponse(
            urgency_level=AttributePrediction(**preds['urgency_level']),
            infection_risk=AttributePrediction(**preds['infection_risk']),
            wound_location=AttributePrediction(**preds['location']),
            healing_status=AttributePrediction(**preds['healing_status']),
            closure_method=AttributePrediction(**preds['closure_method']),
            exudate_type=AttributePrediction(**preds['exudate_type']),
            erythema=AttributePrediction(**preds['erythema']),
            edema=AttributePrediction(**preds['edema']),
            report=report
        )
