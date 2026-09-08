from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import PredictResponse
from inference import SurgWoundInferenceModel
import io
from PIL import Image

app = FastAPI(
    title="SurgWound Assist API",
    description="API for multi-attribute surgical wound assessment from images",
    version="1.0.0"
)

# Allow CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ONNX model wrapper
model = SurgWoundInferenceModel(model_path="model.onnx")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "SurgWound Assist API is running"}

@app.post("/predict", response_model=PredictResponse)
async def predict_wound(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
        
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Run inference
        result = model.predict(image)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
