"""
biomedclip_dataset.py — Raw Image Dataset using BiomedCLIP's preprocessing.

BiomedCLIP uses its own image normalization (different from ImageNet's).
We MUST use its preprocess_train / preprocess_val functions to ensure the
images match what the model expects.
"""
import os
import torch
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from config import BASE_ATTRIBUTES


def normalize_label(val, attr):
    from config import CLASS_MAPPINGS
    if pd.isna(val) or val not in CLASS_MAPPINGS[attr]:
        if 'Uncertain' in CLASS_MAPPINGS[attr]:
            return CLASS_MAPPINGS[attr].index('Uncertain')
        return 0
    return CLASS_MAPPINGS[attr].index(val)


class BiomedCLIPDataset(Dataset):
    """
    Loads raw wound images and applies BiomedCLIP's official preprocessing.
    Preprocess functions are provided by open_clip.create_model_and_transforms().
    """
    def __init__(self, df: pd.DataFrame, transform, img_dir: str = '../../data/images'):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.img_dir = img_dir

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        name = str(row['image_name'])
        img_path = os.path.join(self.img_dir, name if name.endswith('.jpg') else f"{name}.jpg")

        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"[WARN] Error loading {img_path}: {e}")
            image = Image.new('RGB', (224, 224), (0, 0, 0))

        pixel_values = self.transform(image)

        labels = {
            attr: torch.tensor(normalize_label(row.get(attr), attr), dtype=torch.long)
            for attr in BASE_ATTRIBUTES
        }
        return pixel_values, labels
