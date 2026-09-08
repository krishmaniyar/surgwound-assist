import os
import subprocess
import sys

def run_cmd(cmd):
    print(f"\n[RUNNING] {cmd}")
    res = subprocess.run(cmd, shell=True)
    if res.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}")

def main():
    print("Running Domain-Adaptive Pretraining Ablation Pipeline")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ext_dir = os.path.join(base_dir, "external_data")
    
    # 1. Run Stage 0: Train UNet & Crop
    run_cmd(f"python {os.path.join(ext_dir, 'segmentation', 'train_unet.py')}")
    run_cmd(f"python {os.path.join(ext_dir, 'segmentation', 'crop_to_roi.py')}")
    
    # 2. Run Stage 1 Pretraining Variants
    run_cmd(f"python {os.path.join(ext_dir, 'classification_pretrain', 'wound_type_pretrain.py')}")
    run_cmd(f"python {os.path.join(ext_dir, 'classification_pretrain', 'wound_type_pretrain.py')} --surgical_only")
    run_cmd(f"python {os.path.join(ext_dir, 'classification_pretrain', 'location_pretrain.py')}")
    
    # 3. Run Stage 2 Finetuning Variants
    print("\n--- Starting Stage 2 Ablation (finetune_cnn.py variants) ---")
    
    # Baseline (ImageNet only)
    run_cmd("python finetune_cnn.py --experiment_name baseline")
    
    # Variant A (Dataset B Full 4-type Pretraining)
    pt_path_a = os.path.join(ext_dir, "classification_pretrain", "pretrained_backbone_wound_type.pth")
    run_cmd(f"python finetune_cnn.py --experiment_name pretrain_4type --stage1_backbone_path {pt_path_a}")
    
    # Variant B (Dataset B Surgical-only Pretraining)
    pt_path_b = os.path.join(ext_dir, "classification_pretrain", "pretrained_backbone_wound_type_surgical_only.pth")
    run_cmd(f"python finetune_cnn.py --experiment_name pretrain_surgical --stage1_backbone_path {pt_path_b}")
    
    # Variant C (Dataset B Location Pretraining mapped)
    pt_path_c = os.path.join(ext_dir, "classification_pretrain", "pretrained_location_model.pth")
    run_cmd(f"python finetune_cnn.py --experiment_name pretrain_location --stage1_backbone_path {pt_path_c} --stage1_location_path {pt_path_c}")
    
    print("\n[SUCCESS] Ablation pipeline completed. Check the generated metrics_report.md for updated F1 scores on Infection Risk, Urgency Level, and Wound Location.")

if __name__ == "__main__":
    main()
