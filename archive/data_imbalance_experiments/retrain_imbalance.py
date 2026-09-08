import os
import copy
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from sklearn.metrics import f1_score
from heads_mlp import MLPHead, CLASS_MAPPINGS, EmbeddingDataset
from imbalance import FocalLoss, embedding_smote, get_balanced_sampler
import warnings
warnings.filterwarnings("ignore")

MERGED_ATTRS = ['exudate_type_merged', 'infection_risk_merged', 'urgency_level_merged', 'closure_method_merged']
BACKBONES = ['dinov2', 'clip']

def train_head(df_train, df_val, df_test, attribute, backbone, config):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    train_dataset = EmbeddingDataset(df_train, backbone, attribute)
    val_dataset = EmbeddingDataset(df_val, backbone, attribute)
    test_dataset = EmbeddingDataset(df_test, backbone, attribute)
    
    input_dim = train_dataset.features.shape[1]
    num_classes = len(CLASS_MAPPINGS[attribute])
    
    # Setup dataloader depending on decoupled or normal
    sampler, class_weights = get_balanced_sampler(train_dataset, attribute, CLASS_MAPPINGS)
    
    if config['decoupled_retrain']:
        # For decoupled retrain, we use balanced sampler only in the second phase
        # First phase uses normal dataloader
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    else:
        # Standard training uses standard or balanced? Let's use standard unless specified.
        # Actually, "Class-Balanced loss" usually means just the loss weights.
        train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    model = MLPHead(input_dim, 256, num_classes, dropout=0.3).to(device)
    
    if config['loss'] == 'focal':
        criterion = FocalLoss(alpha=class_weights.to(device), gamma=2.0)
    else:
        criterion = nn.CrossEntropyLoss()
        
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)
    epochs = 40
    
    best_macro_f1 = 0.0
    best_weights = None
    
    # Phase 1: Main Training
    for epoch in range(epochs):
        model.train()
        for batch_features, batch_labels in train_loader:
            batch_features, batch_labels = batch_features.to(device), batch_labels.to(device)
            
            if config['smote']:
                batch_features, batch_labels = embedding_smote(batch_features, batch_labels, num_classes)
                
            optimizer.zero_grad()
            outputs = model(batch_features)
            loss = criterion(outputs, batch_labels)
            loss.backward()
            optimizer.step()
            
        # Validation
        model.eval()
        val_preds, val_targets = [], []
        with torch.no_grad():
            for batch_features, batch_labels in DataLoader(val_dataset, batch_size=32):
                outputs = model(batch_features.to(device))
                preds = torch.argmax(outputs, dim=1).cpu().numpy()
                val_preds.extend(preds)
                val_targets.extend(batch_labels.numpy())
                
        macro_f1 = f1_score(val_targets, val_preds, average='macro', zero_division=0)
        if macro_f1 > best_macro_f1 or best_weights is None:
            best_macro_f1 = macro_f1
            best_weights = copy.deepcopy(model.state_dict())

    model.load_state_dict(best_weights)
    
    # Phase 2: Decoupled Head Retrain
    if config['decoupled_retrain']:
        # Freeze all layers except the last one
        for name, param in model.named_parameters():
            if 'net.8' not in name:  # The last linear layer is net.8
                param.requires_grad = False
                
        # BUG FIX #7: reset_parameters() may not exist on all PyTorch builds; use nn.init directly
        nn.init.xavier_uniform_(model.net[8].weight)
        nn.init.zeros_(model.net[8].bias)
                
        # Use class-balanced sampler
        balanced_loader = DataLoader(train_dataset, batch_size=32, sampler=sampler)
        optimizer2 = optim.AdamW(model.net[8].parameters(), lr=1e-3)
        
        best_decoupled_f1 = 0.0
        best_decoupled_weights = None
        
        for epoch in range(15):
            model.train()
            # keep batchnorm frozen during decoupled retrain
            for m in model.modules():
                if isinstance(m, nn.BatchNorm1d):
                    m.eval()
                    
            for batch_features, batch_labels in balanced_loader:
                batch_features, batch_labels = batch_features.to(device), batch_labels.to(device)
                optimizer2.zero_grad()
                outputs = model(batch_features)
                # Usually standard CE is used for decoupled head training
                loss = nn.CrossEntropyLoss()(outputs, batch_labels)
                loss.backward()
                optimizer2.step()
                
            model.eval()
            val_preds, val_targets = [], []
            with torch.no_grad():
                for batch_features, batch_labels in DataLoader(val_dataset, batch_size=32):
                    outputs = model(batch_features.to(device))
                    preds = torch.argmax(outputs, dim=1).cpu().numpy()
                    val_preds.extend(preds)
                    val_targets.extend(batch_labels.numpy())
            f1 = f1_score(val_targets, val_preds, average='macro', zero_division=0)
            if f1 > best_decoupled_f1:
                best_decoupled_f1 = f1
                best_decoupled_weights = copy.deepcopy(model.state_dict())
                
        if best_decoupled_weights:
            model.load_state_dict(best_decoupled_weights)
            
    # Inference on Test Set
    model.eval()
    test_probs = []
    with torch.no_grad():
        test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)
        for batch_features, _ in test_loader:
            outputs = model(batch_features.to(device))
            probs = torch.softmax(outputs, dim=1).cpu().numpy()
            test_probs.append(probs)
            
    test_probs = np.concatenate(test_probs, axis=0)
    return test_probs, test_dataset.labels

def run():
    df = pd.read_csv('data/annotations.csv')
    df_train = df[df['split'] == 'train']
    df_val = df[df['split'] == 'val']
    df_test = df[df['split'] == 'test']
    
    stages = [
        {'name': '+ class merging (CE Loss)', 'loss': 'ce', 'smote': False, 'decoupled_retrain': False},
        {'name': '+ class-balanced loss + focal', 'loss': 'focal', 'smote': False, 'decoupled_retrain': False},
        {'name': '+ embedding-space SMOTE', 'loss': 'focal', 'smote': True, 'decoupled_retrain': False},
        {'name': '+ tau-normalization / decoupled head retrain', 'loss': 'focal', 'smote': True, 'decoupled_retrain': True},
    ]
    
    results = {}
    for stage in stages:
        stage_name = stage['name']
        print(f"\n--- Running: {stage_name} ---")
        results[stage_name] = {}
        
        for attr in MERGED_ATTRS:
            ensemble_probs = []
            test_labels = None
            for backbone in BACKBONES:
                probs, labels = train_head(df_train, df_val, df_test, attr, backbone, stage)
                ensemble_probs.append(probs)
                test_labels = labels
                
            # Ensemble average
            avg_probs = np.mean(ensemble_probs, axis=0)
            preds = np.argmax(avg_probs, axis=1)
            macro_f1 = f1_score(test_labels, preds, average='macro', zero_division=0)
            results[stage_name][attr] = macro_f1
            
    print("\n\nRetraining Results (Test Macro-F1):")
    cols = MERGED_ATTRS
    print(f"{'Config':<45} | {'Exudate (M)':<12} | {'Infection (M)':<12} | {'Urgency (M)':<12} | {'Closure (M)':<12}")
    
    for stage in stages:
        stage_name = stage['name']
        res = results[stage_name]
        vals = [f"{res[c]*100:.2f}%" for c in cols]
        print(f"{stage_name:<45} | {vals[0]:<12} | {vals[1]:<12} | {vals[2]:<12} | {vals[3]:<12}")

if __name__ == "__main__":
    run()
