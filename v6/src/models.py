"""
models.py — v6.0 End-to-End Multi-Task DINOv2 Backbone.
- Deeper 2-layer MLP classifier heads (Linear -> GELU -> Dropout -> Linear)
- Supports Layer-wise LR Decay parameter groups
"""
import torch
import torch.nn as nn
from transformers import AutoModel
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS, DINOV2_MODEL


class EndToEndWoundModel(nn.Module):
    def __init__(self, dropout: float = 0.3):
        super().__init__()

        print(f"Loading backbone: {DINOV2_MODEL}")
        self.backbone = AutoModel.from_pretrained(DINOV2_MODEL)
        self.backbone.gradient_checkpointing_enable()

        hidden_dim = self.backbone.config.hidden_size  # 1024 for dinov2-large

        # 8 separate deeper Multi-Task heads (2-layer MLP)
        self.heads = nn.ModuleDict()

        for attr in BASE_ATTRIBUTES:
            num_cls = len(CLASS_MAPPINGS[attr])
            self.heads[attr] = nn.Sequential(
                nn.Linear(hidden_dim, hidden_dim // 2),
                nn.GELU(),
                nn.Dropout(dropout),
                nn.Linear(hidden_dim // 2, num_cls),
            )
            # Initialise final layer conservatively
            nn.init.zeros_(self.heads[attr][-1].bias)
            nn.init.normal_(self.heads[attr][-1].weight, std=0.02)

    def forward(self, pixel_values):
        outputs = self.backbone(pixel_values=pixel_values)
        cls_token = outputs.last_hidden_state[:, 0, :]

        logits_dict = {}
        for attr in BASE_ATTRIBUTES:
            logits_dict[attr] = self.heads[attr](cls_token)

        return logits_dict

    def get_llrd_param_groups(self, base_lr: float, lr_decay: float = 0.85):
        """
        Layer-Wise Learning Rate Decay (LLRD).
        The classifier heads get base_lr.
        Each transformer layer going downward gets base_lr * lr_decay^(depth).
        This prevents early generic layers from being overwritten too aggressively.
        """
        num_layers = self.backbone.config.num_hidden_layers  # 24 for dinov2-large

        # Group 0: classifier heads — full LR
        param_groups = [
            {"params": list(self.heads.parameters()), "lr": base_lr, "name": "heads"},
        ]

        # Group 1: backbone embeddings and last norm — base_lr * decay^1
        embed_params = list(self.backbone.embeddings.parameters())
        if hasattr(self.backbone, 'layernorm'):
            embed_params += list(self.backbone.layernorm.parameters())
        param_groups.append({
            "params": embed_params,
            "lr": base_lr * (lr_decay ** (num_layers + 1)),
            "name": "embeddings",
        })

        # Groups 2..N+1: transformer layers — LR decreases with depth
        for layer_idx in range(num_layers - 1, -1, -1):
            depth = num_layers - layer_idx
            lr = base_lr * (lr_decay ** depth)
            param_groups.append({
                "params": list(self.backbone.encoder.layer[layer_idx].parameters()),
                "lr": lr,
                "name": f"layer_{layer_idx}",
            })

        return param_groups
