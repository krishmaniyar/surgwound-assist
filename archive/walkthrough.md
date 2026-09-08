# SurgWound Assist Walkthrough

I have successfully built the end-to-end **SurgWound Assist** application according to the specifications. Here is a summary of the implementation:

## 1. Machine Learning Pipeline (`ml/`)
- **Data Preparation (`data_prep.py`)**: Script that pulls the dataset from Hugging Face, aggregates the 8-label VQA splits by `image_name` to prevent data leakage, and extracts the images and targets to a single `annotations.csv`.
- **Dataset (`dataset.py`)**: PyTorch Dataset integration featuring Albumentations for advanced augmentation strategies tailored to real-world medical image variances (e.g. `ColorJitter`, `HorizontalFlip`, `RandomResizedCrop`).
- **Model (`model.py`)**: EfficientNetV2-S backbone utilizing `timm` with a custom multi-task head processing an aggregated 512-d shared embedding into 8 distinct linear classification heads.
- **Training (`train.py`)**: Loop structured for discriminative learning rates, class-weighted cross-entropy loss favoring critical cases (Emergency Care / High Infection Risk), and W&B logging.
- **Evaluation (`evaluate.py`)**: Generates an exhaustive `metrics_report.md` computing Accuracy, Precision, Recall, macro/weighted F1, ROC-AUC, Exact Match Ratio, and outputs confusion matrix visuals.
- **Export (`export_onnx.py`)**: Seamless conversion to ONNX utilizing deterministic inputs for the inference stack.

## 2. API Backend (`api/`)
- Built with **FastAPI** mapping the ONNX model (`inference.py`) to a single fast `POST /predict` endpoint, validated rigorously using Pydantic schemas.
- It includes a rule-based engine that structures the output probabilities and dynamically generates a human-readable clinical summary integrating all 8 predictions.

## 3. Web Frontend (`web/`)
- A **React 18 / Vite / TypeScript** frontend designed with a clean, highly-trustworthy medical aesthetic using Tailwind CSS v4.
- Features intuitive `react-dropzone` drag-and-drop mechanics.
- **Triage Priority Banner**: The UI prominently highlights Urgency level (Green, Yellow, Red) and Infection Risk to the user.
- Disclaimers have been heavily anchored into the design indicating the prototype nature and limiting liability for medical diagnostic replacements.
- Features a localized text-report download component wrapping the final clinical summary.

## 4. Packaging (`docker-compose.yml`)
- Containerized the API backend and Web frontend, allowing for simplified multi-service orchestration out-of-the-box via Docker Compose.
