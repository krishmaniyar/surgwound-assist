"""
v8/analysis/feature_separability.py — Quantifies feature space separability.
Computes intra-class variance, inter-class centroid distances, and silhouette scores
for each attribute to determine if classification failures are due to feature overlap
or classifier decision boundary placement.
"""
import os
import sys
import torch
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from scipy.spatial.distance import cdist

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS, BIOMEDCLIP_MODEL_ID
from model import BiomedCLIPMultiTaskModel
from dataset import SurgWoundDataset
import open_clip


def main():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print("[feature_separability] Extracting features from BiomedCLIP backbone...")

    # Load latest checkpoint if available, else load pretrained backbone
    runs = sorted([os.path.join('v8/runs', d) for d in os.listdir('v8/runs') if os.path.isdir(os.path.join('v8/runs', d))])
    ckpt_path = os.path.join(runs[-1], "checkpoints", "best_model.pth") if runs else None

    model = BiomedCLIPMultiTaskModel(use_text_prototypes=True).to(device)
    if ckpt_path and os.path.exists(ckpt_path):
        model.load_state_dict(torch.load(ckpt_path, map_location=device))
        print(f"  Loaded model weights from {ckpt_path}")
    else:
        print("  Using pretrained BiomedCLIP visual weights")
    model.eval()

    _, _, preprocess_val = open_clip.create_model_and_transforms(BIOMEDCLIP_MODEL_ID)
    df = pd.read_csv('archive/dataset_backup_v7/annotations.csv')
    ds = SurgWoundDataset(df, transform=preprocess_val, legacy_mode=True)

    all_features = []
    all_labels = {attr: [] for attr in BASE_ATTRIBUTES}

    with torch.no_grad():
        for i in range(len(ds)):
            pixels, labels = ds[i]
            inp = pixels.unsqueeze(0).to(device)
            with torch.amp.autocast('cuda') if device.type == 'cuda' else torch.no_grad():
                feat = model.visual(inp)
                feat = feat / feat.norm(dim=-1, keepdim=True)
            all_features.append(feat.squeeze(0).cpu().numpy())
            for attr in BASE_ATTRIBUTES:
                all_labels[attr].append(int(labels[attr].item()))

    features = np.array(all_features)
    print(f"  Extracted embeddings shape: {features.shape}")

    report_lines = [
        "# SurgWound Assist v8 — Feature Space Separability Analysis",
        f"**Dataset**: 349 images, 512-dim normalized feature representations",
        "",
        "## Attribute Separability Metrics",
        "| Attribute | Active Classes | Mean Intra-Class Dist | Mean Inter-Class Dist | Ratio (Inter / Intra) | Silhouette Score | Separability Status |",
        "|---|---|---|---|---|---|---|",
    ]

    for attr in BASE_ATTRIBUTES:
        labels = np.array(all_labels[attr])
        classes, counts = np.unique(labels, return_counts=True)
        active_classes = [c for c, cnt in zip(classes, counts) if cnt >= 2]

        if len(active_classes) < 2:
            report_lines.append(f"| {attr:16s} | {len(active_classes)} | — | — | — | — | Degenerate (1 class) |")
            continue

        # Filter to active classes
        mask = np.isin(labels, active_classes)
        sub_feats = features[mask]
        sub_labels = labels[mask]

        # Silhouette score
        try:
            sil = silhouette_score(sub_feats, sub_labels, metric='cosine')
        except Exception:
            sil = float('nan')

        # Centroids
        centroids = []
        intra_dists = []
        for c in active_classes:
            c_feats = sub_feats[sub_labels == c]
            c_center = c_feats.mean(axis=0, keepdims=True)
            c_center = c_center / (np.linalg.norm(c_center) + 1e-8)
            centroids.append(c_center[0])
            # Intra-class cosine distance (1 - cosine_similarity)
            intra = 1.0 - (c_feats @ c_center.T).mean()
            intra_dists.append(intra)

        mean_intra = float(np.mean(intra_dists))

        # Inter-class centroid distances
        inter_dist_matrix = cdist(np.array(centroids), np.array(centroids), metric='cosine')
        upper_indices = np.triu_indices(len(active_classes), k=1)
        mean_inter = float(inter_dist_matrix[upper_indices].mean()) if len(upper_indices[0]) > 0 else 0.0

        ratio = (mean_inter / mean_intra) if mean_intra > 1e-8 else 0.0
        status = "WELL SEPARATED" if ratio > 1.3 else ("MODERATE" if ratio > 1.1 else "SEVERE OVERLAP")

        report_lines.append(
            f"| {attr:16s} | {len(active_classes)} | {mean_intra:.4f} | {mean_inter:.4f} | **{ratio:.2f}x** | {sil:.4f} | {status} |"
        )

    out_path = "v8/analysis/feature_separability_report.md"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))

    print(f"[feature_separability] Report written -> {out_path}")
    print("\n".join(report_lines[4:]))


if __name__ == '__main__':
    main()
