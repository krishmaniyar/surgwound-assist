"""
dataset.py — Raw Image Dataset for End-to-End Fine-Tuning.
Loads raw images using PIL and applies dynamic torchvision augmentations.
"""
import os
import torch
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms
from config import BASE_ATTRIBUTES

def normalize_label(val, attr):
    from config import CLASS_MAPPINGS
    if pd.isna(val) or val not in CLASS_MAPPINGS[attr]:
        if 'Uncertain' in CLASS_MAPPINGS[attr]:
            return CLASS_MAPPINGS[attr].index('Uncertain')
        return 0
    return CLASS_MAPPINGS[attr].index(val)

class RawImageDataset(Dataset):
    """
    Loads raw .jpg images and applies augmentations.
    Returns: (pixel_values, label_dict)
    """
    def __init__(self, df: pd.DataFrame, img_dir: str = 'data/images', augment: bool = False):
        self.df = df.reset_index(drop=True)
        self.img_dir = img_dir
        self.augment = augment

        # DINOv2 uses standard ImageNet mean and std
        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225])

        if self.augment:
            self.transform = transforms.Compose([
                transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),
                transforms.RandomHorizontalFlip(),
                transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05),
                transforms.ToTensor(),
                normalize,
            ])
        else:
            self.transform = transforms.Compose([
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                normalize,
            ])

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        name = row['image_name']
        
        img_path = os.path.join(self.img_dir, name if name.endswith('.jpg') else f"{name}.jpg")
        
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            # Fallback to black image if file is missing (shouldn't happen)
            print(f"Error loading {img_path}: {e}")
            image = Image.new('RGB', (224, 224), (0, 0, 0))
            
        pixel_values = self.transform(image)

        labels = {
            attr: torch.tensor(normalize_label(row.get(attr, 'Uncertain'), attr), dtype=torch.long)
            for attr in BASE_ATTRIBUTES
        }
        
        return pixel_values, labels
