"""
biomedclip_model.py — v7.0 BiomedCLIP Multi-Task Wound Model.

Microsoft BiomedCLIP is pretrained on 15M medical image-text pairs from PubMed,
making it far better at understanding surgical wound features than DINOv2 which
was trained on generic web photos.

Model: microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224
Visual encoder: ViT-B/16 (86M params), output_dim=512
"""
import torch
import torch.nn as nn
import open_clip
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS

BIOMEDCLIP_MODEL_ID = 'hf-hub:microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224'


def load_biomedclip_visual(model_id: str = BIOMEDCLIP_MODEL_ID):
    """Load BiomedCLIP and return (visual_encoder, preprocess_train, preprocess_val)."""
    print(f"[BiomedCLIP] Loading: {model_id}")
    model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms(model_id)
    visual = model.visual  # ViT-B/16, output_dim=512 after projection
    del model              # free the text encoder memory
    return visual, preprocess_train, preprocess_val


class BiomedCLIPWoundModel(nn.Module):
    """
    End-to-end BiomedCLIP fine-tuning for 8-attribute surgical wound classification.
    Architecture:
      - BiomedCLIP Visual Encoder (ViT-B/16, 86M params, medical pretraining)
      - 8 × 2-layer MLP heads (512 → 256 → GELU → Dropout → num_classes)
    """
    def __init__(self, dropout: float = 0.3, model_id: str = BIOMEDCLIP_MODEL_ID):
        super().__init__()

        self.visual, _, _ = load_biomedclip_visual(model_id)

        # BiomedCLIP ViT-B output is 512-dim (projected)
        feat_dim = 512

        self.heads = nn.ModuleDict()
        for attr in BASE_ATTRIBUTES:
            num_cls = len(CLASS_MAPPINGS[attr])
            self.heads[attr] = nn.Sequential(
                nn.LayerNorm(feat_dim),
                nn.Linear(feat_dim, 256),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(256, num_cls),
            )
            nn.init.zeros_(self.heads[attr][-1].bias)
            nn.init.normal_(self.heads[attr][-1].weight, std=0.02)

    def forward(self, pixel_values):
        """pixel_values: [B, 3, 224, 224] preprocessed by BiomedCLIP's preprocess."""
        features = self.visual(pixel_values)   # [B, 512]
        return {attr: self.heads[attr](features) for attr in BASE_ATTRIBUTES}

    def get_llrd_param_groups(self, base_lr: float, lr_decay: float = 0.85):
        """LLRD: classifier heads get base_lr, visual encoder layers get decayed LR."""
        # Classifier heads — full learning rate
        param_groups = [
            {"params": list(self.heads.parameters()), "lr": base_lr, "name": "heads"},
        ]
        # The ViT trunk in open_clip: self.visual.trunk
        if hasattr(self.visual, 'trunk'):
            trunk = self.visual.trunk
            num_layers = len(trunk.blocks) if hasattr(trunk, 'blocks') else 12

            # Patch embedding + positional embedding
            embed_params = []
            for name in ['patch_embed', 'pos_embed', 'cls_token', 'norm']:
                module = getattr(trunk, name, None)
                if module is not None:
                    if isinstance(module, nn.Parameter):
                        embed_params.append(module)
                    else:
                        embed_params.extend(module.parameters())
            param_groups.append({
                "params": embed_params,
                "lr": base_lr * (lr_decay ** (num_layers + 1)),
                "name": "embeddings",
            })

            # Transformer blocks — LR decreases for deeper layers
            blocks = trunk.blocks if hasattr(trunk, 'blocks') else []
            for idx, block in enumerate(reversed(blocks)):
                depth = idx + 1
                param_groups.append({
                    "params": list(block.parameters()),
                    "lr": base_lr * (lr_decay ** depth),
                    "name": f"block_{len(blocks)-1-idx}",
                })
        else:
            # Fallback: single group for the full visual encoder
            param_groups.append({
                "params": list(self.visual.parameters()),
                "lr": base_lr * (lr_decay ** 6),
                "name": "visual_encoder",
            })

        return param_groups
