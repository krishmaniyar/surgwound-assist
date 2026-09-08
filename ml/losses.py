import torch
import torch.nn as nn
import torch.nn.functional as F
import pandas as pd
import numpy as np
from dataset import CLASS_MAPPINGS

class FocalLoss(nn.Module):
    def __init__(self, weight=None, gamma=2.0, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.weight = weight
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, weight=self.weight, reduction='none')
        pt = torch.exp(-ce_loss)
        focal_loss = ((1 - pt) ** self.gamma) * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        return focal_loss

def compute_class_weights(df: pd.DataFrame, device='cuda'):
    """
    Computes class weights for each attribute using inverse frequency.
    Applies custom penalty multipliers for critical classes.
    """
    weights = {}
    for attr, classes_dict in CLASS_MAPPINGS.items():
        # Count frequencies in training split
        train_df = df[df['split'] == 'train']
        
        # Need to handle classes that might not appear
        num_classes = len(classes_dict)
        counts = np.zeros(num_classes)
        
        # If dataset is empty or attr missing (shouldn't happen) fallback to 1s
        if len(train_df) == 0 or attr not in train_df.columns:
            weights[attr] = torch.ones(num_classes).to(device)
            continue
            
        # We need to map string labels to ints to count them
        # dataset._safe_map_class logic is duplicated here simply for weight calc
        # Let's assume the string labels in df align roughly with CLASS_MAPPINGS keys
        # We'll just count them directly using the keys
        
        # Inverse frequency calculation
        for cls_name, cls_idx in classes_dict.items():
            # Very simple count based on string match (case insensitive)
            count = sum(train_df[attr].str.lower() == cls_name.lower())
            counts[cls_idx] = count
            
        # Smooth counts to avoid div by zero
        counts = counts + 1 
        
        # Inverse freq
        w = 1.0 / counts
        # Normalize so mean weight is 1.0
        w = w / np.sum(w) * num_classes
        
        # Apply specific penalties
        if attr == 'infection_risk':
            # High = index 2
            w[2] *= 5.0 
        elif attr == 'urgency_level':
            # Emergency Care (Red) = index 2
            w[2] *= 5.0
            
        weights[attr] = torch.tensor(w, dtype=torch.float32).to(device)
        
    return weights

def get_criterions(df: pd.DataFrame, use_focal_loss=False, device='cuda'):
    weights = compute_class_weights(df, device)
    criterions = {}
    for attr in CLASS_MAPPINGS.keys():
        if use_focal_loss and attr in ['infection_risk', 'urgency_level']:
            criterions[attr] = FocalLoss(weight=weights[attr])
        else:
            criterions[attr] = nn.CrossEntropyLoss(weight=weights[attr])
    return criterions
