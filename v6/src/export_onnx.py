"""
export_onnx.py — Export the trained End-to-End model to ONNX.
Input:  pixel_values [batch, 3, 224, 224]
Output: softmax probs for each of the 8 wound attributes.
"""
import os
import torch
import numpy as np
import onnx
import onnxruntime as ort

from config import BASE_ATTRIBUTES
from models import EndToEndWoundModel

def export_onnx(run_dir: str, output_path: str = None):
    print("=" * 60)
    print("SurgWound Assist — ONNX Export (v4.0 End-to-End)")
    print("=" * 60)

    if output_path is None:
        output_path = os.path.join(run_dir, "surgwound_end_to_end.onnx")

    ckpt_path = os.path.join(run_dir, "checkpoints", "end_to_end_model.pth")

    model = EndToEndWoundModel().eval()
    if os.path.exists(ckpt_path):
        model.load_state_dict(torch.load(ckpt_path, map_location='cpu'))
        print("  Loaded end_to_end_model.pth")
    else:
        print(f"  [WARN] Missing {ckpt_path}")

    # Use batch_size=1, 3 channels, 224x224
    dummy_in = torch.randn(1, 3, 224, 224)
    print(f"\nExporting to {output_path}...")

    torch.onnx.export(
        model, dummy_in, output_path,
        export_params=True,
        opset_version=17,
        do_constant_folding=True,
        input_names=['pixel_values'],
        output_names=BASE_ATTRIBUTES,
        dynamic_axes={'pixel_values': {0: 'batch_size'}},
    )

    print("Validating ONNX structure...")
    onnx.checker.check_model(onnx.load(output_path))
    print("  Structure OK")
        
    return output_path

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--run_dir", default="runs/latest")
    parser.add_argument("--output",  default=None)
    args = parser.parse_args()

    if args.run_dir == "runs/latest":
        runs = sorted([d for d in os.listdir("runs") if d.startswith("run_")])
        if runs:
            args.run_dir = os.path.join("runs", runs[-1])
            
    export_onnx(args.run_dir, args.output)
