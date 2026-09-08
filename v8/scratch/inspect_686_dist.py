import sys, os
sys.path.insert(0, os.path.abspath('v8/src'))
import pandas as pd
from config import BASE_ATTRIBUTES, CLASS_MAPPINGS

df = pd.read_csv('data/annotations.csv')
print("TOTAL SAMPLES:", len(df))
print(df['split'].value_counts())

for attr in BASE_ATTRIBUTES:
    print(f"\n--- {attr} ---")
    for split in ['train', 'val', 'test']:
        s_df = df[df['split'] == split]
        counts = s_df[attr].value_counts().to_dict()
        print(f"  {split:5s} ({len(s_df)}): {counts}")
