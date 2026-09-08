import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from torch.utils.data import WeightedRandomSampler

class FocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        # inputs: logits
        ce_loss = F.cross_entropy(inputs, targets, reduction='none', weight=self.alpha)
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss

        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

def get_balanced_sampler(dataset, attribute, class_mappings):
    """
    Creates a WeightedRandomSampler that oversamples minority classes for a specific attribute.
    """
    labels = [item[attribute] for item in dataset.data]
    class_counts = np.bincount(labels, minlength=len(class_mappings[attribute]))
    
    # Avoid division by zero
    class_counts = np.where(class_counts == 0, 1, class_counts)
    
    class_weights = 1.0 / class_counts
    
    # Normalize weights (optional, but good for numeric stability)
    class_weights = class_weights / np.sum(class_weights)
    
    sample_weights = [class_weights[label] for label in labels]
    
    sampler = WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(sample_weights),
        replacement=True
    )
    return sampler, torch.FloatTensor(class_weights)

def embedding_smote(features, labels, num_classes, target_samples_per_class=None):
    """
    Applies Synthetic Minority Over-sampling Technique (SMOTE) in embedding space.
    If target_samples_per_class is None, matches the majority class count.
    
    features: (N, D) tensor of embeddings
    labels: (N,) tensor of class indices
    """
    device = features.device
    features = features.cpu().numpy()
    labels = labels.cpu().numpy()
    
    class_counts = np.bincount(labels, minlength=num_classes)
    majority_count = np.max(class_counts)
    
    if target_samples_per_class is None:
        target_counts = np.full(num_classes, majority_count)
    else:
        target_counts = np.maximum(class_counts, target_samples_per_class)
        
    synthetic_features = []
    synthetic_labels = []
    
    for c in range(num_classes):
        num_synthetic = target_counts[c] - class_counts[c]
        if num_synthetic <= 0 or class_counts[c] < 2:
            continue
            
        c_features = features[labels == c]
        n_c = len(c_features)
        
        for _ in range(num_synthetic):
            # Pick a random sample and another random sample to interpolate with
            idx1, idx2 = np.random.choice(n_c, 2, replace=False)
            lam = np.random.beta(0.2, 0.2) # Beta distribution for interpolation
            
            new_feat = lam * c_features[idx1] + (1 - lam) * c_features[idx2]
            # Normalize to keep it on the hypersphere (important for CLIP/DINO)
            new_feat = new_feat / (np.linalg.norm(new_feat) + 1e-8)
            
            synthetic_features.append(new_feat)
            synthetic_labels.append(c)
            
    if len(synthetic_features) > 0:
        syn_features_tensor = torch.tensor(np.array(synthetic_features), dtype=torch.float32, device=device)
        syn_labels_tensor = torch.tensor(np.array(synthetic_labels), dtype=torch.long, device=device)
        
        combined_features = torch.cat([torch.tensor(features, device=device), syn_features_tensor], dim=0)
        combined_labels = torch.cat([torch.tensor(labels, device=device), syn_labels_tensor], dim=0)
        return combined_features, combined_labels
        
    return torch.tensor(features, device=device), torch.tensor(labels, device=device)
