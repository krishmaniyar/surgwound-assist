"""
v8/src/model.py — BiomedCLIP Multi-Task Architecture with:
  1. Medical ViT-B/16 vision backbone
  2. Residual task-specific adapters
  3. Vision-Language semantic text prototype head initialization
  4. Multi-scale global + local high-resolution feature fusion
  5. Layer-Wise Learning Rate Decay (LLRD) parameter group builder
"""
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import open_clip
from typing import Dict, Optional, Tuple, Union, List, Any

from config import BASE_ATTRIBUTES, CLASS_MAPPINGS, BIOMEDCLIP_MODEL_ID


def load_biomedclip_visual(model_id: str = BIOMEDCLIP_MODEL_ID):
    """Load BiomedCLIP and return (visual_encoder, preprocess_train, preprocess_val)."""
    model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms(model_id)
    visual = model.visual
    del model
    return visual, preprocess_train, preprocess_val


class TextInformedHead(nn.Module):
    """
    Residual adapter classification head with optional PubMedBERT semantic prototype initialization.
    
    Architecture:
      x -> LayerNorm(in_dim)
      adapted = x + Linear(in_dim, hidden_dim) -> GELU -> Dropout -> Linear(hidden_dim, in_dim)
      logits = Linear(in_dim, num_classes)
    """
    def __init__(
        self,
        in_dim: int = 512,
        hidden_dim: int = 256,
        num_classes: int = 2,
        dropout: float = 0.25,
        text_prototype: Optional[torch.Tensor] = None,
    ):
        super().__init__()
        self.norm = nn.LayerNorm(in_dim)
        self.adapter = nn.Sequential(
            nn.Linear(in_dim, hidden_dim),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, in_dim),
        )
        self.classifier = nn.Linear(in_dim, num_classes)

        # Initialize adapter to near-identity
        nn.init.zeros_(self.adapter[-1].weight)
        nn.init.zeros_(self.adapter[-1].bias)

        if text_prototype is not None and text_prototype.shape == (num_classes, in_dim):
            with torch.no_grad():
                self.classifier.weight.copy_(text_prototype)
                nn.init.zeros_(self.classifier.bias)
        else:
            nn.init.normal_(self.classifier.weight, std=0.02)
            nn.init.zeros_(self.classifier.bias)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_norm = self.norm(x)
        x_adapted = x_norm + self.adapter(x_norm)
        return self.classifier(x_adapted)


class BiomedCLIPMultiTaskModel(nn.Module):
    """
    SurgWound Assist v8 Multi-Task Model.
    Supports single-scale (224x224) and multi-scale (global + local) inputs.
    """
    def __init__(
        self,
        dropout: float = 0.25,
        hidden_dim: int = 256,
        use_text_prototypes: bool = True,
        multiscale: bool = False,
        prototype_path: Optional[str] = None,
    ):
        super().__init__()
        self.multiscale = multiscale
        self.visual, _, _ = load_biomedclip_visual(BIOMEDCLIP_MODEL_ID)

        feat_dim = 512

        # Optional multi-scale fusion
        if self.multiscale:
            self.fusion = nn.Sequential(
                nn.Linear(feat_dim * 2, feat_dim),
                nn.LayerNorm(feat_dim),
                nn.GELU(),
                nn.Dropout(dropout),
            )

        # Load text prototypes if enabled
        prototypes = {}
        if use_text_prototypes:
            if prototype_path is None:
                prototype_path = os.path.join(os.path.dirname(__file__), 'clinical_text_prototypes.pt')
            if os.path.exists(prototype_path):
                prototypes = torch.load(prototype_path, map_location='cpu')
                print(f"[BiomedCLIPMultiTaskModel] Loaded clinical text prototypes from {prototype_path}")

        # Multi-task heads
        self.heads = nn.ModuleDict()
        for attr in BASE_ATTRIBUTES:
            num_classes = len(CLASS_MAPPINGS[attr])
            proto = prototypes.get(attr, None)
            self.heads[attr] = TextInformedHead(
                in_dim=feat_dim,
                hidden_dim=hidden_dim,
                num_classes=num_classes,
                dropout=dropout,
                text_prototype=proto,
            )

    def forward(self, x: Union[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]) -> Dict[str, torch.Tensor]:
        if self.multiscale and isinstance(x, (tuple, list)):
            x_global, x_local = x
            f_global = self.visual(x_global)
            f_local = self.visual(x_local)
            features = self.fusion(torch.cat([f_global, f_local], dim=-1))
        else:
            if isinstance(x, (tuple, list)):
                x = x[0]
            features = self.visual(x)

        return {attr: self.heads[attr](features) for attr in BASE_ATTRIBUTES}

    def get_llrd_param_groups(self, base_lr: float, lr_decay: float = 0.85, weight_decay: float = 1e-3) -> List[Dict[str, Any]]:
        """
        Layer-Wise Learning Rate Decay (LLRD) parameter partitioning:
          - Classifier heads and fusion layers get base_lr
          - ViT trunk transformer blocks get base_lr * (lr_decay ** depth)
          - Patch and position embeddings get base_lr * (lr_decay ** 13)
        """
        param_groups = []

        # 1. Heads & Fusion parameters
        head_params = list(self.heads.parameters())
        if self.multiscale:
            head_params += list(self.fusion.parameters())

        param_groups.append({
            "params": head_params,
            "lr": base_lr,
            "weight_decay": weight_decay,
            "name": "heads_and_fusion",
        })

        # 2. Vision backbone trunk
        if hasattr(self.visual, 'trunk'):
            trunk = self.visual.trunk
            num_layers = len(trunk.blocks) if hasattr(trunk, 'blocks') else 12

            # Embeddings
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
                "weight_decay": weight_decay,
                "name": "embeddings",
            })

            # Transformer blocks
            blocks = trunk.blocks if hasattr(trunk, 'blocks') else []
            for idx, block in enumerate(reversed(blocks)):
                depth = idx + 1
                param_groups.append({
                    "params": list(block.parameters()),
                    "lr": base_lr * (lr_decay ** depth),
                    "weight_decay": weight_decay,
                    "name": f"block_{len(blocks)-1-idx}",
                })
        else:
            param_groups.append({
                "params": list(self.visual.parameters()),
                "lr": base_lr * (lr_decay ** 6),
                "weight_decay": weight_decay,
                "name": "visual_fallback",
            })

        return param_groups
