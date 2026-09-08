"""
v8/src/generate_text_prototypes.py — Precompute BiomedCLIP text embeddings for clinical prompts.
Saves normalized 512-dim prototype tensors to v8/src/clinical_text_prototypes.pt.
"""
import os
import torch
import open_clip

from config import BASE_ATTRIBUTES, CLASS_MAPPINGS, CLINICAL_PROMPTS, BIOMEDCLIP_MODEL_ID


def main():
    print(f"[text_prototypes] Loading BiomedCLIP model and tokenizer: {BIOMEDCLIP_MODEL_ID}")
    model, _, _ = open_clip.create_model_and_transforms(BIOMEDCLIP_MODEL_ID)
    tokenizer = open_clip.get_tokenizer(BIOMEDCLIP_MODEL_ID)
    model.eval()

    prototypes = {}
    with torch.no_grad():
        for attr in BASE_ATTRIBUTES:
            classes = CLASS_MAPPINGS[attr]
            prompts = [CLINICAL_PROMPTS[attr].get(cls_name, f"surgical wound {attr} {cls_name}") for cls_name in classes]
            tokens = tokenizer(prompts)
            text_features = model.encode_text(tokens)
            text_features = text_features / text_features.norm(dim=-1, keepdim=True)
            prototypes[attr] = text_features.cpu()
            print(f"  {attr:16s}: {len(classes)} classes -> shape {prototypes[attr].shape}")

    out_path = os.path.join(os.path.dirname(__file__), 'clinical_text_prototypes.pt')
    torch.save(prototypes, out_path)
    print(f"[text_prototypes] Saved prototypes to {out_path}")


if __name__ == '__main__':
    main()
