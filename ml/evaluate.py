import os
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_auc_score, cohen_kappa_score
import matplotlib.pyplot as plt
import seaborn as sns
import yaml

from dataset import SurgWoundDataset, CLASS_MAPPINGS
from model import SurgWoundMultiTaskModel

def load_config(config_path="configs/default.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def expected_calibration_error(y_true, y_prob, n_bins=10):
    """Computes the Expected Calibration Error (ECE)."""
    # Find predicted classes and confidences
    y_pred = np.argmax(y_prob, axis=1)
    confidences = np.max(y_prob, axis=1)
    
    accuracies = y_pred == y_true
    
    ece = 0.0
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    
    for i in range(n_bins):
        bin_lower = bin_boundaries[i]
        bin_upper = bin_boundaries[i + 1]
        
        in_bin = (confidences > bin_lower) & (confidences <= bin_upper)
        prop_in_bin = in_bin.mean()
        
        if prop_in_bin > 0:
            accuracy_in_bin = accuracies[in_bin].mean()
            avg_confidence_in_bin = confidences[in_bin].mean()
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
            
    return ece

def evaluate_split(model, dataloader, device, split_name):
    model.eval()
    all_trues = {attr: [] for attr in CLASS_MAPPINGS.keys()}
    all_preds = {attr: [] for attr in CLASS_MAPPINGS.keys()}
    all_probs = {attr: [] for attr in CLASS_MAPPINGS.keys()}
    
    with torch.no_grad():
        for images, labels in dataloader:
            images = images.to(device)
            outputs = model(images)
            
            for attr in CLASS_MAPPINGS.keys():
                probs = F.softmax(outputs[attr], dim=1).cpu().numpy()
                preds = np.argmax(probs, axis=1)
                trues = labels[attr].numpy()
                
                all_probs[attr].extend(probs)
                all_preds[attr].extend(preds)
                all_trues[attr].extend(trues)
                
    # Convert to arrays
    for attr in CLASS_MAPPINGS.keys():
        all_trues[attr] = np.array(all_trues[attr])
        all_preds[attr] = np.array(all_preds[attr])
        all_probs[attr] = np.array(all_probs[attr])
        
    return all_trues, all_preds, all_probs

def generate_report():
    config = load_config()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load model
    model_path = f"best_model_{config['model']['backbone']}.pth"
    model = SurgWoundMultiTaskModel(
        backbone_name=config['model']['backbone'],
        pretrained=False,
        embedding_dim=config['model']['embedding_dim']
    )
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path, map_location=device))
    else:
        print(f"Model file {model_path} not found. Running evaluation with untrained weights.")
    model.to(device)
    
    splits = ['val', 'test']
    report_md = f"# SurgWound Multi-Task Training Report\n\n"
    report_md += f"**Backbone:** {config['model']['backbone']}\n\n"
    
    os.makedirs("plots", exist_ok=True)
    
    for split in splits:
        report_md += f"## Split: {split.upper()}\n\n"
        
        dataset = SurgWoundDataset(
            config['data']['annotations_path'], 
            config['data']['images_dir'], 
            split=split, 
            img_size=config['data']['img_size']
        )
        if len(dataset) == 0:
            report_md += f"No data found for split {split}.\n\n"
            continue
            
        dataloader = DataLoader(dataset, batch_size=config['training']['batch_size'], shuffle=False)
        trues, preds, probs = evaluate_split(model, dataloader, device, split)
        
        # Aggregate metrics
        exact_match = 0
        total_samples = len(trues['location'])
        incorrect_labels = 0
        total_labels = total_samples * len(CLASS_MAPPINGS)
        
        for i in range(total_samples):
            match = True
            for attr in CLASS_MAPPINGS.keys():
                if trues[attr][i] != preds[attr][i]:
                    match = False
                    incorrect_labels += 1
            if match:
                exact_match += 1
                
        emr = exact_match / total_samples
        hamming_loss = incorrect_labels / total_labels
        
        macro_f1s = []
        
        report_md += f"- **Exact Match Ratio:** {emr:.4f}\n"
        report_md += f"- **Hamming Loss:** {hamming_loss:.4f}\n\n"
        
        for attr, classes_dict in CLASS_MAPPINGS.items():
            num_classes = len(classes_dict)
            class_names = [k for k, v in sorted(classes_dict.items(), key=lambda item: item[1])]
            
            y_t = trues[attr]
            y_p = preds[attr]
            y_prob = probs[attr]
            
            acc = accuracy_score(y_t, y_p)
            prec_m, rec_m, f1_m, _ = precision_recall_fscore_support(y_t, y_p, average='macro', zero_division=0)
            prec_w, rec_w, f1_w, _ = precision_recall_fscore_support(y_t, y_p, average='weighted', zero_division=0)
            
            macro_f1s.append(f1_m)
            
            try:
                auc = roc_auc_score(y_t, y_prob, multi_class='ovr', average='macro')
            except ValueError:
                auc = float('nan') # Can happen if not all classes present in split
                
            kappa = cohen_kappa_score(y_t, y_p)
            ece = expected_calibration_error(y_t, y_prob)
            
            report_md += f"### Attribute: {attr}\n"
            report_md += f"- Accuracy: {acc:.4f}\n"
            report_md += f"- Macro (P/R/F1): {prec_m:.4f} / {rec_m:.4f} / {f1_m:.4f}\n"
            report_md += f"- Weighted (P/R/F1): {prec_w:.4f} / {rec_w:.4f} / {f1_w:.4f}\n"
            report_md += f"- ROC-AUC (Macro): {auc:.4f}\n"
            report_md += f"- Cohen's Kappa: {kappa:.4f}\n"
            report_md += f"- ECE: {ece:.4f}\n\n"
            
            # Per-class sensitivity and specificity
            cm = confusion_matrix(y_t, y_p, labels=range(num_classes))
            report_md += "| Class | Sensitivity (Recall) | Specificity |\n"
            report_md += "|---|---|---|\n"
            
            for i, cls_name in enumerate(class_names):
                tp = cm[i, i]
                fn = np.sum(cm[i, :]) - tp
                fp = np.sum(cm[:, i]) - tp
                tn = np.sum(cm) - tp - fn - fp
                
                sens = tp / (tp + fn) if (tp + fn) > 0 else 0
                spec = tn / (tn + fp) if (tn + fp) > 0 else 0
                
                # Highlight critical classes
                highlight = ""
                if attr == 'infection_risk' and cls_name == 'High':
                    highlight = "**(CRITICAL)** "
                if attr == 'urgency_level' and 'Emergency' in cls_name:
                    highlight = "**(CRITICAL)** "
                    
                report_md += f"| {highlight}{cls_name} | {sens:.4f} | {spec:.4f} |\n"
                
            report_md += "\n"
            
            # Plot confusion matrix
            plt.figure(figsize=(8, 6))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
            plt.title(f'Confusion Matrix: {attr} ({split})')
            plt.ylabel('True Label')
            plt.xlabel('Predicted Label')
            plt.tight_layout()
            img_path = f"plots/cm_{attr}_{split}.png"
            plt.savefig(img_path)
            plt.close()
            
            report_md += f"![Confusion Matrix - {attr}](./{img_path})\n\n"
            
        report_md += f"**Mean Macro-F1 across 8 heads:** {np.mean(macro_f1s):.4f}\n\n"
        report_md += "---\n\n"

    with open("metrics_report.md", "w") as f:
        f.write(report_md)
        
    print("Report generated at metrics_report.md")

if __name__ == "__main__":
    generate_report()
