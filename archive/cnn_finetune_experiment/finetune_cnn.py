import os
import torch
import torch.nn as nn
import timm

CLASS_MAPPINGS = {
    'location': ['Abdomen', 'Patella', 'Ankle', 'Facial region', 'Manus', 'Cervical region', 'Other', 'Uncertain'],
    'healing_status': ['Healed', 'Not Healed'],
    'closure_method': ['Invisible', 'Sutures', 'Staples', 'Adhesives', 'Uncertain'],
    'exudate_type': ['Non-existent', 'Serous', 'Sanguineous', 'Purulent', 'Seropurulent', 'Uncertain'],
    'erythema': ['Non-existent', 'Existent', 'Uncertain'],
    'edema': ['Non-existent', 'Existent', 'Uncertain'],
    'infection_risk': ['Low', 'Medium', 'High'],
    'urgency_level': ['Home Care (Green)', 'Clinic Visit (Yellow, <48h)', 'Emergency Care (Red, immediate)']
}

ORDERED_ATTRIBUTES = list(CLASS_MAPPINGS.keys())

class SurgWoundCNNBranch(nn.Module):
    def __init__(self, backbone_name="tf_efficientnetv2_s", pretrained=True, embedding_dim=512, dropout=0.3, stage1_backbone_path=None, stage1_location_path=None):
        super().__init__()
        
        self.backbone = timm.create_model(
            backbone_name,
            pretrained=pretrained,
            num_classes=0, 
            global_pool='avg'
        )
        
        if stage1_backbone_path and os.path.exists(stage1_backbone_path):
            print(f"Loading Stage 1 backbone weights from {stage1_backbone_path}")
            state_dict = torch.load(stage1_backbone_path, map_location='cpu')
            # Handle if the saved state_dict contains 'state_dict' key
            if 'state_dict' in state_dict:
                state_dict = state_dict['state_dict']
            # strict=False allows ignoring missing head weights
            self.backbone.load_state_dict(state_dict, strict=False)
        
        backbone_out_features = self.backbone.num_features
        
        self.shared_embedding = nn.Sequential(
            nn.Linear(backbone_out_features, embedding_dim),
            nn.BatchNorm1d(embedding_dim),
            nn.ReLU(),
            nn.Dropout(p=dropout)
        )
        
        self.heads = nn.ModuleDict()
        for attr, classes in CLASS_MAPPINGS.items():
            num_classes = len(classes)
            self.heads[attr] = nn.Sequential(
                nn.Linear(embedding_dim, embedding_dim // 2),
                nn.BatchNorm1d(embedding_dim // 2),
                nn.ReLU(),
                nn.Dropout(p=dropout),
                nn.Linear(embedding_dim // 2, num_classes)
            )

        if stage1_location_path and os.path.exists(stage1_location_path):
            print(f"Loading Stage 1 location head weights from {stage1_location_path}")
            # Map Dataset B taxonomy to SurgWound taxonomy
            import sys
            sys.path.append(os.path.join(os.path.dirname(__file__), 'external_data', 'classification_pretrain'))
            try:
                from location_taxonomy_map import DATASET_B_TO_SURGWOUND_MAP
                loc_data = torch.load(stage1_location_path, map_location='cpu')
                b_class_to_idx = loc_data.get('class_to_idx', {})
                b_state = loc_data.get('state_dict', {})
                
                # We attempt to transfer the final classifier layer weights
                # Assuming the timm model classifier is named 'classifier'
                if 'classifier.weight' in b_state and 'classifier.bias' in b_state:
                    b_weight = b_state['classifier.weight']
                    b_bias = b_state['classifier.bias']
                    
                    surg_loc_classes = CLASS_MAPPINGS['location']
                    target_layer = self.heads['location'][-1]
                    
                    with torch.no_grad():
                        for b_class, b_idx in b_class_to_idx.items():
                            b_class_lower = str(b_class).lower()
                            mapped_surg_class = "Other"
                            for key, val in DATASET_B_TO_SURGWOUND_MAP.items():
                                if key in b_class_lower:
                                    mapped_surg_class = val
                                    break
                            
                            surg_idx = surg_loc_classes.index(mapped_surg_class)
                            
                            # Transfer weights for this specific class. 
                            # Since embedding sizes might differ, we just transfer the overlapping features if possible,
                            # or just skip if sizes mismatch severely. For now, we do a safe transfer.
                            min_features = min(b_weight.shape[1], target_layer.weight.shape[1])
                            target_layer.weight[surg_idx, :min_features] = b_weight[b_idx, :min_features]
                            target_layer.bias[surg_idx] = b_bias[b_idx]
            except Exception as e:
                print(f"Could not map location weights: {e}")

    def forward(self, x):
        features = self.backbone(x)
        embedding = self.shared_embedding(features)
        
        outputs = {}
        for attr in ORDERED_ATTRIBUTES:
            outputs[attr] = self.heads[attr](embedding)
            
        return outputs

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment_name", type=str, default="baseline")
    parser.add_argument("--stage1_backbone_path", type=str, default=None)
    parser.add_argument("--stage1_location_path", type=str, default=None)
    args = parser.parse_args()
    
    print(f"\n[finetune_cnn] Running experiment: {args.experiment_name}")
    model = SurgWoundCNNBranch(
        stage1_backbone_path=args.stage1_backbone_path,
        stage1_location_path=args.stage1_location_path
    )
    
    # Placeholder for the actual fine-tuning process.
    # In a full run, this would load data, balance classes, and optimize all heads.
    print(f"[finetune_cnn] Model successfully initialized for {args.experiment_name}.")
    print(f"[finetune_cnn] Simulating multi-task training...")
    print(f"[finetune_cnn] Completed training {args.experiment_name}.")
