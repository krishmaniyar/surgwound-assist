import torch
import torch.nn as nn
import timm
from dataset import CLASS_MAPPINGS

class SurgWoundMultiTaskModel(nn.Module):
    def __init__(self, backbone_name='efficientnetv2_s', pretrained=True, embedding_dim=512):
        super().__init__()
        
        self.backbone_name = backbone_name
        
        # Create backbone
        # We remove the classifier head by using num_classes=0
        self.backbone = timm.create_model(
            backbone_name, 
            pretrained=pretrained, 
            num_classes=0, 
            global_pool='avg'
        )
        
        # Get backbone output feature size
        backbone_out_features = self.backbone.num_features
        
        # Shared embedding layer
        self.shared_embedding = nn.Sequential(
            nn.Linear(backbone_out_features, embedding_dim),
            nn.BatchNorm1d(embedding_dim),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # Create 8 independent heads based on CLASS_MAPPINGS
        self.heads = nn.ModuleDict()
        for attr, classes_dict in CLASS_MAPPINGS.items():
            num_classes = len(classes_dict)
            self.heads[attr] = nn.Linear(embedding_dim, num_classes)
            
    def forward(self, x):
        # Extract features
        features = self.backbone(x)
        
        # Pass through shared embedding
        shared = self.shared_embedding(features)
        
        # Pass through individual heads
        outputs = {}
        for attr, head in self.heads.items():
            outputs[attr] = head(shared)
            
        return outputs

    def freeze_backbone(self):
        """Freezes all parameters in the backbone."""
        for param in self.backbone.parameters():
            param.requires_grad = False
            
    def unfreeze_backbone(self):
        """Unfreezes all parameters in the backbone."""
        for param in self.backbone.parameters():
            param.requires_grad = True

    def unfreeze_last_n_blocks(self, n=2):
        """
        Unfreezes the last n blocks of the backbone for fine-tuning.
        This is a bit tricky across different timm architectures.
        For EfficientNet/ResNet, we can target specific children.
        """
        # First, unfreeze everything
        self.unfreeze_backbone()
        
        # Then, if it's efficientnet, it has a 'blocks' Sequential.
        if 'efficientnet' in self.backbone_name:
            # Freeze stem and early blocks
            if hasattr(self.backbone, 'conv_stem'):
                for p in self.backbone.conv_stem.parameters(): p.requires_grad = False
            if hasattr(self.backbone, 'bn1'):
                for p in self.backbone.bn1.parameters(): p.requires_grad = False
                
            if hasattr(self.backbone, 'blocks'):
                total_blocks = len(self.backbone.blocks)
                for i, block in enumerate(self.backbone.blocks):
                    if i < total_blocks - n:
                        for p in block.parameters():
                            p.requires_grad = False
                            
        elif 'resnet' in self.backbone_name:
            # ResNet has layer1, layer2, layer3, layer4
            layers_to_freeze = ['conv1', 'bn1', 'layer1', 'layer2', 'layer3', 'layer4']
            
            # If n=2, we want to keep layer3 and layer4 unfreezed.
            # We freeze everything except the last `n` layers in ['layer1', 'layer2', 'layer3', 'layer4']
            target_unfreeze_layers = [f'layer{5-i}' for i in range(1, n+1)] 
            
            for name, child in self.backbone.named_children():
                if name in target_unfreeze_layers:
                    continue # Keep it unfreezed
                # otherwise freeze it
                for p in child.parameters():
                    p.requires_grad = False
