# SurgWound Multi-Task Training Pipeline

This repository contains a complete ML training pipeline for a multi-task surgical-wound image classifier based on the SurgWound dataset. 

It trains a single CNN backbone (e.g., EfficientNetV2-S or ResNet50) to predict 8 clinical attributes simultaneously from a single wound image.

> **DISCLAIMER:** This project is a research prototype trained on a small dataset (686 images) sourced from social media. It is **NOT** clinically validated or intended for diagnostic use. It should not be used to guide patient care.

## Requirements

- Python 3.9+
- CUDA-enabled GPU recommended

```bash
pip install -r requirements.txt
```

## Configuration

All hyperparameters and settings are centralized in `configs/default.yaml`. 
Modify this file to switch backbones, adjust learning rates, or toggle focal loss.

## Execution Pipeline

### 1. Data Preparation
Downloads the dataset from HuggingFace, pivots the VQA rows into a tabular format grouped by `image_name`, and extracts base64 images into `data/images/`.

```bash
python data_prep.py
```
*This step must be run first.*

### 2. Model Training
Runs a two-phase training loop (frozen backbone -> fine-tuned end-to-end). Logs metrics to Weights & Biases and saves the best checkpoint (`best_model_<backbone>.pth`) based on the validation mean macro-F1 score.

```bash
python train.py
```

### 3. Evaluation
Computes extensive metrics across all 8 heads on the validation and test splits. Auto-generates a detailed `metrics_report.md` with confusion matrices, ROC-AUC, Specificity/Sensitivity, and calibration errors.

```bash
python evaluate.py
```

### 4. Cross-Validation
Given the small dataset size, run a 5-fold cross-validation to get robust performance estimates.

```bash
python cross_validate.py
```

### 5. ONNX Export
Exports the best PyTorch checkpoint to ONNX format and performs a numerical parity check to ensure equivalence.

```bash
python export_onnx.py
```

## Architectural Highlights
- **Multi-Task Heads**: 8 independent linear classifiers stemming from a shared global average pooling embedding.
- **Class Imbalance Handling**: Inverse-frequency weighted Cross-Entropy loss with explicit penalty multipliers for critical classes (High Infection Risk, Emergency Care Urgency).
- **Robust Augmentations**: Albumentations pipeline simulating poor social-media image quality (color jitter, blur, noise, rotations).
