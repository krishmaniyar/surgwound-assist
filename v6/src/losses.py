"""
losses.py — Loss functions for long-tail classification.
Implements: FocalLoss, LDAM Loss, Class-Balanced (CB) Loss weights.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


# ── Focal Loss ─────────────────────────────────────────────────────────────────
class FocalLoss(nn.Module):
    """
    Focal Loss (Lin et al. 2017).
    alpha: per-class weights tensor shape (C,). Pass None for uniform.
    gamma: focusing parameter. Higher = more focus on hard examples.
    """
    def __init__(self, alpha=None, gamma=2.0, reduction='mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs, targets):
        ce_loss = F.cross_entropy(inputs, targets, weight=self.alpha, reduction='none')
        pt = torch.exp(-ce_loss)
        focal = (1 - pt) ** self.gamma * ce_loss
        if self.reduction == 'mean':
            return focal.mean()
        elif self.reduction == 'sum':
            return focal.sum()
        return focal


# ── LDAM Loss ──────────────────────────────────────────────────────────────────
class LDAMLoss(nn.Module):
    """
    Label-Distribution-Aware Margin Loss (Cao et al. NeurIPS 2019).
    Specifically designed for long-tail recognition. Imposes larger margins
    for minority classes, preventing majority-class collapse.

    cls_num_list: list of sample counts per class [n0, n1, ..., nC-1]
    max_m: maximum margin delta (default 0.5)
    s: scale factor (default 30, like ArcFace)
    weight: optional per-class weight tensor for re-weighting
    """
    def __init__(self, cls_num_list, max_m=0.5, s=30, weight=None):
        super().__init__()
        safe_cls_num = np.array(cls_num_list)
        safe_cls_num = np.where(safe_cls_num == 0, 1, safe_cls_num)
        m_list = 1.0 / np.sqrt(np.sqrt(safe_cls_num))
        m_list = m_list * (max_m / np.max(m_list))
        m_list = torch.FloatTensor(m_list)
        self.m_list = m_list
        self.s = s
        self.weight = weight

    def forward(self, x, target):
        index = torch.zeros_like(x, dtype=torch.bool)
        index.scatter_(1, target.unsqueeze(1), True)

        # x_m = x - margin for the true class
        index_float = index.float()
        batch_m = torch.matmul(self.m_list[None, :].to(x.device),
                               index_float.transpose(0, 1))
        batch_m = batch_m.view(-1, 1)
        x_m = x - batch_m

        output = torch.where(index, x_m, x)
        return F.cross_entropy(self.s * output, target, weight=self.weight)


# ── Class-Balanced Loss weights ────────────────────────────────────────────────
def get_cb_weights(cls_num_list: list, beta: float = 0.9999) -> torch.Tensor:
    """
    Effective Number of Samples class-balanced weights (Cui et al. CVPR 2019).
    Significantly better than 1/n weighting for extreme imbalance.

    beta=0.9999 is the recommended value for long-tail datasets.
    """
    effective_num = [1.0 - beta ** n for n in cls_num_list]
    weights = [(1.0 - beta) / en if en > 1e-8 else 0.0 for en in effective_num]
    weights = np.array(weights)
    # Normalize so that sum = num_classes (scale-invariant training)
    # Only count classes that actually have samples
    valid_classes = sum(1 for w in weights if w > 0)
    if valid_classes > 0:
        weights = weights / weights.sum() * valid_classes
    return torch.FloatTensor(weights)


# ── Weighted Random Sampler ────────────────────────────────────────────────────
def get_balanced_sampler(labels: np.ndarray, num_classes: int):
    """
    Creates a WeightedRandomSampler for class-balanced mini-batches.
    Used in DRW Phase 2 alongside LDAM loss.
    """
    from torch.utils.data import WeightedRandomSampler

    cls_counts = np.bincount(labels, minlength=num_classes)
    cls_counts = np.where(cls_counts == 0, 1, cls_counts)  # avoid div/0
    cls_weights = 1.0 / cls_counts
    sample_weights = cls_weights[labels]

    sampler = WeightedRandomSampler(
        weights=torch.DoubleTensor(sample_weights),
        num_samples=len(sample_weights),
        replacement=True
    )
    return sampler


# ── Embedding-space SMOTE ──────────────────────────────────────────────────────
def embedding_smote(features: torch.Tensor, labels: torch.Tensor,
                    num_classes: int) -> tuple:
    """
    Synthetic Minority Over-sampling in embedding space.
    Interpolates between existing minority samples on the unit hypersphere.
    """
    device = features.device
    feats_np = features.cpu().numpy()
    labs_np  = labels.cpu().numpy()

    cls_counts   = np.bincount(labs_np, minlength=num_classes)
    majority_cnt = int(np.max(cls_counts))

    syn_feats, syn_labs = [], []
    for c in range(num_classes):
        n_need = majority_cnt - cls_counts[c]
        if n_need <= 0 or cls_counts[c] < 2:
            continue
        c_feats = feats_np[labs_np == c]
        n_c = len(c_feats)
        for _ in range(n_need):
            i1, i2 = np.random.choice(n_c, 2, replace=False)
            lam = np.random.beta(0.4, 0.4)
            new_f = lam * c_feats[i1] + (1 - lam) * c_feats[i2]
            norm = np.linalg.norm(new_f) + 1e-8
            syn_feats.append(new_f / norm)
            syn_labs.append(c)

    if syn_feats:
        sf = torch.tensor(np.array(syn_feats), dtype=torch.float32, device=device)
        sl = torch.tensor(np.array(syn_labs),  dtype=torch.long,    device=device)
        features = torch.cat([features, sf], dim=0)
        labels   = torch.cat([labels,   sl], dim=0)

    # Shuffle
    perm = torch.randperm(len(labels), device=device)
    return features[perm], labels[perm]
