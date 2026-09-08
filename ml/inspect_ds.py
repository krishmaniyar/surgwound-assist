import os
# pyrefly: ignore [missing-import]
from datasets import load_dataset

ds = load_dataset("xuxuxuxuxu/SurgWound")
print(ds)
print("--- TRAIN ROW 0 ---")
print(ds['train'][0].keys())
print({k: str(v)[:100] for k,v in ds['train'][0].items()})
