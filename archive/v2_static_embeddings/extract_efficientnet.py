import os
import torch
import pandas as pd
from PIL import Image
from tqdm import tqdm
import numpy as np
import timm
from torchvision import transforms
from torch.utils.data import Dataset, DataLoader

torch.set_num_threads(os.cpu_count() or 4)

class ImageDataset(Dataset):
    def __init__(self, df, transform):
        self.df = df
        self.transform = transform
        
    def __len__(self):
        return len(self.df)
        
    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        img_name = row['image_name']
        img_path = f"data/images/{img_name}"
        raw_img = Image.open(img_path).convert('RGB')
        tensor = self.transform(raw_img)
        return img_name, tensor

def cache_efficientnet_embeddings():
    df = pd.read_csv('data/annotations.csv')
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    dataset = ImageDataset(df, transform)
    loader = DataLoader(dataset, batch_size=16, shuffle=False, num_workers=0)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ext_dir = os.path.join(base_dir, "external_data")
    pt_dir = os.path.join(ext_dir, "classification_pretrain")
    
    variants = {
        'effnet_baseline': None,
        'effnet_4type': os.path.join(pt_dir, "pretrained_backbone_wound_type.pth"),
        'effnet_surgical': os.path.join(pt_dir, "pretrained_backbone_wound_type_surgical_only.pth"),
        'effnet_location': os.path.join(pt_dir, "pretrained_location_model.pth")
    }
    
    for v_name, v_path in variants.items():
        os.makedirs(f'data/embeddings/{v_name}', exist_ok=True)
        print(f"Loading {v_name}...")
        model = timm.create_model("tf_efficientnetv2_s", pretrained=(v_path is None), num_classes=0, global_pool='avg')
        
        if v_path and os.path.exists(v_path):
            state_dict = torch.load(v_path, map_location='cpu')
            if 'state_dict' in state_dict:
                state_dict = state_dict['state_dict']
            model.load_state_dict(state_dict, strict=False)
            
        model = model.to(device).eval()
        
        with torch.no_grad():
            for names, tensors in tqdm(loader, desc=f"Caching {v_name}"):
                tensors = tensors.to(device)
                feats = model(tensors)
                feats = feats / feats.norm(dim=-1, keepdim=True)
                feats_np = feats.cpu().numpy()
                
                for i, name in enumerate(names):
                    np.save(f"data/embeddings/{v_name}/{name}.npy", feats_np[i])

if __name__ == "__main__":
    cache_efficientnet_embeddings()
