import os
import base64
import pandas as pd
# pyrefly: ignore [missing-import]
from datasets import load_dataset
from tqdm import tqdm
from PIL import Image
import io
import numpy as np
from sklearn.model_selection import train_test_split

def decode_image(base64_str, output_path):
    if not os.path.exists(output_path):
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(output_path)

def map_question_to_attr(question: str) -> str:
    q = question.lower()
    if 'location' in q: return 'location'
    if 'healed' in q or 'healing' in q: return 'healing_status'
    if 'closure' in q: return 'closure_method'
    if 'exudate' in q: return 'exudate_type'
    if 'erythema' in q: return 'erythema'
    if 'edema' in q: return 'edema'
    if 'infection' in q: return 'infection_risk'
    if 'urgency' in q: return 'urgency_level'
    return None

def process_dataset():
    print("Loading dataset xuxuxuxuxu/SurgWound...")
    ds = load_dataset("xuxuxuxuxu/SurgWound")
    
    images_dict = {}
    os.makedirs('data/images', exist_ok=True)
    
    # Process VQA splits (assuming standard train/validation/test or just one if exploded)
    # We aggregate all rows by image_name
    for split in ds.keys():
        if split == 'report_generation':
            continue # Handle separately
        print(f"Processing split: {split}")
        for row in tqdm(ds[split]):
            img_name = row['image_name']
            if img_name not in images_dict:
                images_dict[img_name] = {
                    'image_name': img_name,
                    'location': None,
                    'healing_status': None,
                    'closure_method': None,
                    'exudate_type': None,
                    'erythema': None,
                    'edema': None,
                    'infection_risk': None,
                    'urgency_level': None,
                    'report': None
                }
                
                # Decode and save image
                img_path = f"data/images/{img_name}"
                if 'image_base64' in row:
                    decode_image(row['image_base64'], img_path)
                elif 'image' in row:
                    if isinstance(row['image'], str):
                        decode_image(row['image'], img_path)
                    else:
                        if not os.path.exists(img_path):
                            if row['image'].mode != 'RGB':
                                row['image'] = row['image'].convert('RGB')
                            row['image'].save(img_path)
            
            # Map answer to attribute
            attr = map_question_to_attr(str(row.get('question', '')))
            if attr:
                ans = str(row.get('answer', '')).strip()
                if ans:
                    images_dict[img_name][attr] = ans

    # Process report split
    if 'report_generation' in ds:
        print("Processing report_generation split...")
        for row in tqdm(ds['report_generation']):
            img_name = row['image_name']
            if img_name in images_dict:
                report_text = row.get('report', row.get('answer', ''))
                images_dict[img_name]['report'] = report_text

    # Create DataFrame
    df = pd.DataFrame(list(images_dict.values()))
    
    # Ensure all required attributes are present
    required_cols = ['location', 'healing_status', 'closure_method', 'exudate_type', 
                     'erythema', 'edema', 'infection_risk', 'urgency_level']
    
    # Drop rows missing ANY of the 8 labels (if any)
    initial_len = len(df)
    df.replace("", np.nan, inplace=True)
    df.dropna(subset=required_cols, inplace=True)
    print(f"Kept {len(df)}/{initial_len} images with all 8 labels.")
    
    # Create ~7:1:2 split (Train:Val:Test) based on image_name
    print("Creating group-aware train/val/test splits (70/10/20)...")
    train_val_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    # Remaining 80% is train_val. We want 10% of total as val, which is 12.5% of train_val
    train_df, val_df = train_test_split(train_val_df, test_size=0.125, random_state=42)
    
    train_df['split'] = 'train'
    val_df['split'] = 'val'
    test_df['split'] = 'test'
    
    final_df = pd.concat([train_df, val_df, test_df], ignore_index=True)
    
    # Save annotations
    final_df.to_csv('data/annotations.csv', index=False)
    print(f"Saved annotations to data/annotations.csv")
    print(f"Split counts:\n{final_df['split'].value_counts()}")

if __name__ == "__main__":
    process_dataset()
