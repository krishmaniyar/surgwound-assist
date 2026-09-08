import os
import pandas as pd
import numpy as np
from PIL import Image
import torch
from torch.utils.data import Dataset
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Define class mappings based on the master prompt specification
CLASS_MAPPINGS = {
    'location': {
        'Abdomen': 0, 'Patella': 1, 'Ankle': 2, 'Facial region': 3, 
        'Manus': 4, 'Cervical region': 5, 'Other': 6, 'Uncertain': 7
    },
    'healing_status': {
        'Healed': 0, 'Not Healed': 1
    },
    'closure_method': {
        'Invisible': 0, 'Sutures': 1, 'Staples': 2, 'Adhesives': 3, 'Uncertain': 4
    },
    'exudate_type': {
        'Non-existent': 0, 'Serous': 1, 'Sanguineous': 2, 'Purulent': 3, 'Seropurulent': 4, 'Uncertain': 5
    },
    'erythema': {
        'Non-existent': 0, 'Existent': 1, 'Uncertain': 2
    },
    'edema': {
        'Non-existent': 0, 'Existent': 1, 'Uncertain': 2
    },
    'infection_risk': {
        'Low': 0, 'Medium': 1, 'High': 2
    },
    'urgency_level': {
        'Home Care (Green)': 0, 'Clinic Visit (Yellow)': 1, 'Emergency Care (Red)': 2
    }
}

# Add fuzzy matching mapping for urgency since the prompt labels differ from some raw dataset labels
URGENCY_MAP_FUZZY = {
    'home care': 'Home Care (Green)',
    'home care (green)': 'Home Care (Green)',
    'clinic visit': 'Clinic Visit (Yellow)',
    'clinic visit (yellow)': 'Clinic Visit (Yellow)',
    'emergency care': 'Emergency Care (Red)',
    'emergency care (red)': 'Emergency Care (Red)'
}

def get_transforms(split: str, img_size: int = 224):
    """
    Returns albumentations transforms for train and val/test splits.
    Uses robust augmentations accounting for diverse social-media lighting/angles.
    """
    if split == 'train':
        return A.Compose([
            A.RandomResizedCrop(size=(img_size, img_size), scale=(0.8, 1.0)),
            A.HorizontalFlip(p=0.5),
            A.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3, hue=0.1, p=0.7),
            A.Affine(scale=(0.9, 1.1), translate_percent=(-0.05, 0.05), rotate=(-15, 15), p=0.5),
            A.OneOf([
                A.GaussianBlur(blur_limit=(3, 7)),
                A.GaussNoise(),
            ], p=0.3),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])
    else:
        # val or test
        return A.Compose([
            A.Resize(height=img_size, width=img_size),
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ToTensorV2(),
        ])

class SurgWoundDataset(Dataset):
    def __init__(self, annotations_file: str, img_dir: str, split: str = 'train', img_size: int = 224):
        self.img_dir = img_dir
        self.split = split
        self.transform = get_transforms(split, img_size)
        
        # Load dataset and filter by split
        if os.path.exists(annotations_file):
            df = pd.read_csv(annotations_file)
            self.data = df[df['split'] == split].reset_index(drop=True)
        else:
            self.data = pd.DataFrame()
            
    def __len__(self):
        return len(self.data)
        
    def _safe_map_class(self, attr: str, val: str) -> int:
        val = str(val).strip()
        if attr == 'urgency_level':
            # normalize for fuzzy mapping
            lower_val = val.lower()
            mapped_val = URGENCY_MAP_FUZZY.get(lower_val, val)
            if mapped_val in CLASS_MAPPINGS[attr]:
                return CLASS_MAPPINGS[attr][mapped_val]
                
        # Try direct match
        if val in CLASS_MAPPINGS[attr]:
            return CLASS_MAPPINGS[attr][val]
            
        # Fallbacks for inconsistencies
        lower_val = val.lower()
        for k, v in CLASS_MAPPINGS[attr].items():
            if k.lower() == lower_val:
                return v
                
        # If uncertain class exists, fallback to it, else fallback to 0 to prevent crash
        if 'Uncertain' in CLASS_MAPPINGS[attr]:
            return CLASS_MAPPINGS[attr]['Uncertain']
        return 0
        
    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        
        # Load image
        img_name = row['image_name']
        img_path = os.path.join(self.img_dir, img_name)
        try:
            image = Image.open(img_path).convert('RGB')
            image = np.array(image)
        except Exception as e:
            # Return a blank tensor if image is missing to prevent crashing the loader
            # Ideally data prep ensures all images exist
            image = np.zeros((224, 224, 3), dtype=np.uint8)
            
        # Apply transform
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']
            
        # Extract labels
        labels = {}
        for attr in CLASS_MAPPINGS.keys():
            labels[attr] = torch.tensor(self._safe_map_class(attr, row[attr]), dtype=torch.long)
            
        return image, labels
