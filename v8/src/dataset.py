"""
v8/src/dataset.py — Raw image dataset for multi-task wound attribute classification.
Supports single-scale (224x224) and dual-scale (global + local crop) representations.
"""
import os
import torch
import numpy as np
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from typing import Dict, Tuple, Optional, Any
from torchvision import transforms

from config import BASE_ATTRIBUTES, CLASS_MAPPINGS


def normalize_label(val: Any, attr: str, legacy_mode: bool = True) -> int:
    """
    Normalizes raw CSV label strings into integer class IDs.
    
    If legacy_mode=True:
      Reproduces v7.5 behavior exactly (where urgency_level strings that differed from
      CLASS_MAPPINGS fell back to index 0).
      
    If legacy_mode=False:
      Applies clean semantic parsing so all attributes, including urgency_level,
      map accurately to their ground truth classes.
    """
    if pd.isna(val):
        return CLASS_MAPPINGS[attr].index('Uncertain') if 'Uncertain' in CLASS_MAPPINGS[attr] else 0

    val_str = str(val).strip()

    if not legacy_mode and attr == 'urgency_level':
        if 'Home Care' in val_str or 'Green' in val_str:
            return 0
        elif 'Clinic Visit' in val_str or 'Yellow' in val_str:
            return 1
        elif 'Emergency Care' in val_str or 'Red' in val_str:
            return 2

    # Direct match check
    if val_str in CLASS_MAPPINGS[attr]:
        return CLASS_MAPPINGS[attr].index(val_str)

    # Fallback
    if 'Uncertain' in CLASS_MAPPINGS[attr]:
        return CLASS_MAPPINGS[attr].index('Uncertain')
    return 0


class SurgWoundDataset(Dataset):
    """
    SurgWound multi-task dataset.
    
    Args:
        df: DataFrame containing split annotations.
        transform: Standard BiomedCLIP transform.
        img_dir: Directory with image files.
        legacy_mode: Whether to use legacy v7.5 label mapping for baseline parity.
        multiscale: If True, extracts both global image and high-resolution center/detail crop.
        local_crop_scale: Scale fraction of original image to crop for local view (e.g. 0.6).
    """
    def __init__(
        self,
        df: pd.DataFrame,
        transform,
        img_dir: str = 'data/images',
        legacy_mode: bool = True,
        multiscale: bool = False,
        local_crop_scale: float = 0.65,
    ):
        self.df = df.reset_index(drop=True)
        self.transform = transform
        self.img_dir = img_dir
        self.legacy_mode = legacy_mode
        self.multiscale = multiscale
        self.local_crop_scale = local_crop_scale

    def __len__(self) -> int:
        return len(self.df)

    def _get_local_crop(self, image: Image.Image) -> Image.Image:
        """Extract a centered wound crop at high resolution."""
        w, h = image.size
        crop_w = int(w * self.local_crop_scale)
        crop_h = int(h * self.local_crop_scale)
        left = (w - crop_w) // 2
        top = (h - crop_h) // 2
        return image.crop((left, top, left + crop_w, top + crop_h))

    def __getitem__(self, idx: int) -> Tuple[Any, Dict[str, torch.Tensor]]:
        row = self.df.iloc[idx]
        name = str(row['image_name'])
        img_path = os.path.join(self.img_dir, name if name.endswith('.jpg') else f"{name}.jpg")

        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            image = Image.new('RGB', (224, 224), (0, 0, 0))

        # Global context image
        pixel_values_global = self.transform(image)

        labels = {
            attr: torch.tensor(
                normalize_label(row.get(attr), attr, legacy_mode=self.legacy_mode),
                dtype=torch.long
            )
            for attr in BASE_ATTRIBUTES
        }

        if self.multiscale:
            local_crop = self._get_local_crop(image)
            pixel_values_local = self.transform(local_crop)
            return (pixel_values_global, pixel_values_local), labels

        return pixel_values_global, labels
