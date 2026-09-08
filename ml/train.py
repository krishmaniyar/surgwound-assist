import os
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm
import wandb
import yaml
import numpy as np
from sklearn.metrics import f1_score

from dataset import SurgWoundDataset, CLASS_MAPPINGS
from model import SurgWoundMultiTaskModel
from losses import get_criterions
import pandas as pd

def load_config(config_path="configs/default.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def train():
    config = load_config()
    
    # Initialize W&B
    # Check if WANDB_API_KEY is set or assume offline/logged in
    mode = "online" if os.environ.get("WANDB_API_KEY") else "disabled"
    wandb.init(
        project=config['project_name'], 
        name=config['run_name'],
        config=config,
        mode=mode
    )
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Load data
    train_dataset = SurgWoundDataset(
        config['data']['annotations_path'], 
        config['data']['images_dir'], 
        split='train', 
        img_size=config['data']['img_size']
    )
    val_dataset = SurgWoundDataset(
        config['data']['annotations_path'], 
        config['data']['images_dir'], 
        split='val', 
        img_size=config['data']['img_size']
    )
    
    if len(train_dataset) == 0:
        print("Training dataset is empty. Run data_prep.py first.")
        return
        
    train_loader = DataLoader(
        train_dataset, 
        batch_size=config['training']['batch_size'], 
        shuffle=True, 
        num_workers=4,
        pin_memory=True if torch.cuda.is_available() else False
    )
    val_loader = DataLoader(
        val_dataset, 
        batch_size=config['training']['batch_size'], 
        shuffle=False, 
        num_workers=4,
        pin_memory=True if torch.cuda.is_available() else False
    )
    
    # Model
    model = SurgWoundMultiTaskModel(
        backbone_name=config['model']['backbone'],
        pretrained=config['model']['pretrained'],
        embedding_dim=config['model']['embedding_dim']
    )
    model.to(device)
    
    # Phase 1: Freeze backbone
    model.freeze_backbone()
    
    # Criterions
    df = pd.read_csv(config['data']['annotations_path'])
    criterions = get_criterions(df, use_focal_loss=config['loss']['use_focal_loss'], device=device)
    
    # Optimizer & Scheduler
    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad],
        lr=float(config['training']['lr_head']),
        weight_decay=float(config['training']['weight_decay'])
    )
    
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=config['training']['epochs']
    )
    
    scaler = torch.cuda.amp.GradScaler(enabled=torch.cuda.is_available())
    
    best_macro_f1 = 0.0
    patience_counter = 0
    epochs = config['training']['epochs']
    warmup_epochs = config['training']['warmup_epochs']
    
    for epoch in range(epochs):
        # Phase transition check
        if epoch == warmup_epochs:
            print("--- Unfreezing last backbone blocks for fine-tuning ---")
            model.unfreeze_last_n_blocks(n=2)
            
            # Recreate optimizer with discriminative LRs
            head_params = []
            for name, param in model.named_parameters():
                if param.requires_grad and 'backbone' not in name:
                    head_params.append(param)
                    
            backbone_params = []
            for name, param in model.named_parameters():
                if param.requires_grad and 'backbone' in name:
                    backbone_params.append(param)
                    
            optimizer = torch.optim.AdamW([
                {'params': backbone_params, 'lr': float(config['training']['lr_backbone'])},
                {'params': head_params, 'lr': float(config['training']['lr_head'])}
            ], weight_decay=float(config['training']['weight_decay']))
            
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=epochs - warmup_epochs
            )
            
        # Training
        model.train()
        train_loss = 0.0
        pbar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{epochs} [Train]")
        
        for images, labels in pbar:
            images = images.to(device)
            labels = {k: v.to(device) for k, v in labels.items()}
            
            optimizer.zero_grad()
            
            with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                outputs = model(images)
                loss = 0.0
                for attr in CLASS_MAPPINGS.keys():
                    loss += criterions[attr](outputs[attr], labels[attr])
                    
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
            
            train_loss += loss.item()
            pbar.set_postfix({'loss': f"{loss.item():.4f}"})
            
        train_loss /= len(train_loader)
        
        # Validation
        model.eval()
        val_loss = 0.0
        val_preds = {attr: [] for attr in CLASS_MAPPINGS.keys()}
        val_trues = {attr: [] for attr in CLASS_MAPPINGS.keys()}
        
        pbar = tqdm(val_loader, desc=f"Epoch {epoch+1}/{epochs} [Val]")
        with torch.no_grad():
            for images, labels in pbar:
                images = images.to(device)
                labels = {k: v.to(device) for k, v in labels.items()}
                
                with torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
                    outputs = model(images)
                    loss = 0.0
                    for attr in CLASS_MAPPINGS.keys():
                        loss += criterions[attr](outputs[attr], labels[attr])
                        
                        preds = torch.argmax(outputs[attr], dim=1).cpu().numpy()
                        trues = labels[attr].cpu().numpy()
                        
                        val_preds[attr].extend(preds)
                        val_trues[attr].extend(trues)
                        
                val_loss += loss.item()
                
        val_loss /= len(val_loader)
        
        # Compute Macro F1 per attribute
        f1_scores = {}
        for attr in CLASS_MAPPINGS.keys():
            f1_scores[attr] = f1_score(val_trues[attr], val_preds[attr], average='macro', zero_division=0)
            
        mean_macro_f1 = np.mean(list(f1_scores.values()))
        
        print(f"Epoch {epoch+1} - Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Mean Macro-F1: {mean_macro_f1:.4f}")
        
        log_dict = {
            'train_loss': train_loss,
            'val_loss': val_loss,
            'val_mean_macro_f1': mean_macro_f1,
            'lr_head': optimizer.param_groups[-1]['lr']
        }
        if epoch >= warmup_epochs:
            log_dict['lr_backbone'] = optimizer.param_groups[0]['lr']
            
        for attr, score in f1_scores.items():
            log_dict[f'val_f1_{attr}'] = score
            
        wandb.log(log_dict)
        
        scheduler.step()
        
        # Checkpoint and Early Stopping
        if mean_macro_f1 > best_macro_f1:
            best_macro_f1 = mean_macro_f1
            patience_counter = 0
            torch.save(model.state_dict(), f"best_model_{config['model']['backbone']}.pth")
            print(f"--> Saved new best model with F1: {best_macro_f1:.4f}")
        else:
            patience_counter += 1
            if patience_counter >= config['training']['early_stopping_patience']:
                print(f"Early stopping triggered after {epoch+1} epochs.")
                break
                
    wandb.finish()

if __name__ == "__main__":
    train()
