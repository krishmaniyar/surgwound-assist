# heads_mlp.py — backward-compatibility shim
# This file is kept for any scripts that import from it.
# The new architecture lives in: models.py, train.py, dataset.py, losses.py

from config import CLASS_MAPPINGS, BASE_ATTRIBUTES
from dataset import EmbeddingDataset, normalize_label
from models import ResidualMLPHead as MLPHead

__all__ = ['CLASS_MAPPINGS', 'BASE_ATTRIBUTES', 'EmbeddingDataset',
           'normalize_label', 'MLPHead']
