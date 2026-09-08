"""
embeddings.py — Extract and cache DINOv2-base (768-dim) + CLIP ViT-L-14 (768-dim).
Upgraded from dinov2-small + ViT-B-32 to significantly better backbones.
Skips images already cached.
"""
import os
import torch
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm
import open_clip
from transformers import AutoImageProcessor, AutoModel
from torch.utils.data import Dataset, DataLoader

from config import DINOV2_MODEL, CLIP_MODEL, CLIP_PRETRAIN


class ImageDataset(Dataset):
    def __init__(self, df, clip_preprocess, img_dir="data/images"):
        self.df              = df.reset_index(drop=True)
        self.clip_preprocess = clip_preprocess
        self.img_dir         = img_dir

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row      = self.df.iloc[idx]
        img_path = os.path.join(self.img_dir, row['image_name'])
        raw_img  = Image.open(img_path).convert('RGB')
        clip_img = self.clip_preprocess(raw_img)
        return row['image_name'], raw_img, clip_img


def collate_fn(batch):
    names       = [b[0] for b in batch]
    raw_images  = [b[1] for b in batch]
    clip_tensors = torch.stack([b[2] for b in batch])
    return names, raw_images, clip_tensors


def cache_embeddings(embed_dir: str = "data/embeddings",
                     img_dir: str   = "data/images"):
    """Extract and cache DINOv2-base + CLIP ViT-L-14 embeddings."""

    if not os.path.exists('data/annotations.csv'):
        print("[embeddings] annotations.csv not found — run data_prep.py first")
        return

    df = pd.read_csv('data/annotations.csv')

    dino_dir = os.path.join(embed_dir, "dinov2")
    clip_dir = os.path.join(embed_dir, "clip")
    os.makedirs(dino_dir, exist_ok=True)
    os.makedirs(clip_dir, exist_ok=True)

    # Filter out already computed
    remaining = []
    for _, row in df.iterrows():
        name = row['image_name']
        if not (os.path.exists(os.path.join(dino_dir, f"{name}.npy")) and
                os.path.exists(os.path.join(clip_dir,  f"{name}.npy"))):
            remaining.append(row)

    if not remaining:
        print("[embeddings] All embeddings already cached — nothing to do.")
        return

    rem_df = pd.DataFrame(remaining).reset_index(drop=True)
    print(f"[embeddings] Extracting for {len(rem_df)} images...")

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"[embeddings] Device: {device}")
    if device.type == 'cuda':
        print(f"[embeddings] GPU: {torch.cuda.get_device_name(0)}")

    # ── Load CLIP ViT-L-14 ────────────────────────────────────────────────────
    print(f"[embeddings] Loading CLIP {CLIP_MODEL} ({CLIP_PRETRAIN})...")
    clip_model, _, clip_preprocess = open_clip.create_model_and_transforms(
        CLIP_MODEL, pretrained=CLIP_PRETRAIN)
    clip_model = clip_model.to(device).eval()

    # ── Load DINOv2-base ──────────────────────────────────────────────────────
    print(f"[embeddings] Loading DINOv2 {DINOV2_MODEL}...")
    dino_processor = AutoImageProcessor.from_pretrained(DINOV2_MODEL)
    dino_model     = AutoModel.from_pretrained(DINOV2_MODEL).to(device).eval()

    dataset = ImageDataset(rem_df, clip_preprocess, img_dir)
    loader  = DataLoader(dataset, batch_size=16, shuffle=False,
                         collate_fn=collate_fn, num_workers=0)

    with torch.no_grad():
        for names, raw_images, clip_tensors in tqdm(loader, desc="Extracting"):
            # ── CLIP ──────────────────────────────────────────────────────────
            clip_feats = clip_model.encode_image(clip_tensors.to(device))
            clip_feats = clip_feats / clip_feats.norm(dim=-1, keepdim=True)
            clip_np    = clip_feats.cpu().float().numpy()

            # ── DINOv2 ────────────────────────────────────────────────────────
            dino_inputs = dino_processor(
                images=raw_images, return_tensors='pt').to(device)
            dino_out   = dino_model(**dino_inputs)
            dino_feats = dino_out.last_hidden_state[:, 0, :]   # CLS token
            dino_feats = dino_feats / dino_feats.norm(dim=-1, keepdim=True)
            dino_np    = dino_feats.cpu().float().numpy()

            for i, name in enumerate(names):
                np.save(os.path.join(clip_dir,  f"{name}.npy"), clip_np[i])
                np.save(os.path.join(dino_dir,  f"{name}.npy"), dino_np[i])

    print(f"[embeddings] Done! CLIP dim={clip_np.shape[-1]}, DINOv2 dim={dino_np.shape[-1]}")


if __name__ == "__main__":
    cache_embeddings()
