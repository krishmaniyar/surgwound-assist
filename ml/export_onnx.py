import torch
import onnx
import onnxruntime as ort
import numpy as np
import yaml
import sys
import io

# Fix for UnicodeEncodeError on Windows during torch.onnx.export
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from model import SurgWoundMultiTaskModel
from dataset import CLASS_MAPPINGS

def load_config(config_path="configs/default.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def export_to_onnx():
    config = load_config()
    
    # Init model
    model = SurgWoundMultiTaskModel(
        backbone_name=config['model']['backbone'],
        pretrained=False,
        embedding_dim=config['model']['embedding_dim']
    )
    
    model_path = f"best_model_{config['model']['backbone']}.pth"
    try:
        model.load_state_dict(torch.load(model_path, map_location='cpu'))
        print(f"Loaded {model_path} for export.")
    except Exception as e:
        print(f"Warning: Could not load {model_path}. Exporting untrained model. {e}")
        
    model.eval()
    
    # Create dummy input
    batch_size = 1
    channels = 3
    img_size = config['data']['img_size']
    dummy_input = torch.randn(batch_size, channels, img_size, img_size)
    
    # PyTorch forward pass for parity check
    with torch.no_grad():
        pt_outputs = model(dummy_input)
        
    # Export
    onnx_path = f"surgwound_{config['model']['backbone']}.onnx"
    
    # Prepare output names in a deterministic order
    output_names = list(CLASS_MAPPINGS.keys())
    
    print(f"Exporting to {onnx_path}...")
    torch.onnx.export(
        model, 
        dummy_input, 
        onnx_path, 
        export_params=True, 
        opset_version=14, 
        do_constant_folding=True, 
        input_names=['input'], 
        output_names=output_names,
        dynamic_axes={'input': {0: 'batch_size'}, **{name: {0: 'batch_size'} for name in output_names}}
    )
    print("Export complete.")
    
    # --- Parity Check ---
    print("Running numerical parity check...")
    
    # Load ONNX model
    onnx_model = onnx.load(onnx_path)
    onnx.checker.check_model(onnx_model)
    
    ort_session = ort.InferenceSession(onnx_path, providers=['CPUExecutionProvider'])
    
    def to_numpy(tensor):
        return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()

    ort_inputs = {ort_session.get_inputs()[0].name: to_numpy(dummy_input)}
    ort_outs = ort_session.run(None, ort_inputs)
    
    # Verify outputs
    max_diff = 0.0
    for i, attr in enumerate(output_names):
        pt_out = to_numpy(pt_outputs[attr])
        ort_out = ort_outs[i]
        
        np.testing.assert_allclose(pt_out, ort_out, rtol=1e-03, atol=1e-05)
        diff = np.max(np.abs(pt_out - ort_out))
        max_diff = max(max_diff, diff)
        
    print(f"Parity check passed! Maximum absolute difference: {max_diff:.8f}")

if __name__ == "__main__":
    export_to_onnx()
