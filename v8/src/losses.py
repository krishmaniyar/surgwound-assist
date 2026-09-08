"""
v8/src/losses.py — Advanced loss functions for long-tail multi-task learning.

Implements:
  1. LogitAdjustedLoss (Menon et al., ICLR 2021) — Fisher-consistent balanced error loss.
  2. BalancedSoftmaxLoss (Ren et al., NeurIPS 2020) — Native FP16/AMP safe long-tail loss.
  3. LDAMLoss (Cao et al., NeurIPS 2019) — Label-Distribution-Aware Margin loss (FP32 safe).
  4. FocalLoss (Lin et al., 2017) — Class-balanced focal loss.
  5. Effective Number of Samples (Cui et al., CVPR 2019).
  6. Label smoothing support in LogitAdjustedLoss and AdaptiveTauLogitAdjustedLoss.
     Redistributes epsilon probability mass uniformly, helping gradient flow to minority classes.
"""
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import List, Optional


def get_cb_weights(cls_num_list: List[int], beta: float = 0.9999) -> torch.Tensor:
    """
    Compute Class-Balanced weights via Effective Number of Samples (Cui et al. CVPR 2019).
    Weights are normalized so that their sum equals the number of non-zero classes.
    """
    effective_num = [1.0 - (beta ** max(1, n)) for n in cls_num_list]
    weights = [(1.0 - beta) / en if en > 1e-8 else 0.0 for en in effective_num]
    weights = np.array(weights, dtype=np.float32)
    valid_classes = sum(1 for n in cls_num_list if n > 0)
    if valid_classes > 0 and weights.sum() > 0:
        weights = weights / weights.sum() * valid_classes
    return torch.tensor(weights, dtype=torch.float32)


class FocalLoss(nn.Module):
    """
    Class-balanced Focal Loss (Lin et al. 2017).
    Downweights well-classified examples to focus gradient energy on hard instances.
    """
    def __init__(self, alpha: Optional[torch.Tensor] = None, gamma: float = 2.0, reduction: str = 'mean'):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction

    def forward(self, inputs: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        alpha = self.alpha.to(inputs.device) if self.alpha is not None else None
        ce_loss = F.cross_entropy(inputs, targets, weight=alpha, reduction='none')
        pt = torch.exp(-ce_loss)
        focal = ((1.0 - pt) ** self.gamma) * ce_loss
        if self.reduction == 'mean':
            return focal.mean()
        elif self.reduction == 'sum':
            return focal.sum()
        return focal


class LogitAdjustedLoss(nn.Module):
    """
    Logit Adjusted Loss (Menon et al., ICLR 2021).
    Statistically optimal for long-tailed classification. Adds class-prior margins
    tau * log(pi_y) directly to the logits:
      L(x, y) = -log( exp(x_y + tau * log(pi_y)) / sum_j exp(x_j + tau * log(pi_j)) )

    Key advantages over LDAM:
      1. No scale factor s (e.g. s=15 or 30), completely avoiding FP16/AMP gradient overflow.
      2. Strictly Fisher-consistent for balanced test error.
      3. Smooth gradients across all classes.
    Optionally supports label_smoothing (Szegedy et al. 2016) which redistributes
    epsilon probability mass uniformly across all classes, complementing logit adjustment.
    """
    def __init__(
        self,
        cls_num_list: List[int],
        tau: float = 1.0,
        weight: Optional[torch.Tensor] = None,
        label_smoothing: float = 0.0,
    ):
        super().__init__()
        safe_counts = np.array(cls_num_list, dtype=np.float32)
        safe_counts = np.where(safe_counts == 0, 1.0, safe_counts)
        total_samples = safe_counts.sum()
        priors = safe_counts / total_samples
        log_priors = np.log(priors)
        self.register_buffer('log_priors', torch.tensor(log_priors, dtype=torch.float32))
        self.tau = tau
        self.weight = weight
        self.label_smoothing = label_smoothing

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        # Adjusted logits: logits + tau * log_priors
        log_priors = self.log_priors.to(logits.device)
        adjusted_logits = logits + self.tau * log_priors.unsqueeze(0)
        weight = self.weight.to(logits.device) if self.weight is not None else None
        return F.cross_entropy(adjusted_logits, targets, weight=weight, label_smoothing=self.label_smoothing)


class AdaptiveTauLogitAdjustedLoss(nn.Module):
    """
    Adaptive Tau Logit Adjusted Loss.
    Scales tau dynamically according to the severity of class imbalance in each head:
        tau_head = max(base_tau, math.log(n_max / max(1, n_min)) * 0.5)
    For mildly imbalanced heads (e.g. healing_status ~ 1.6x), tau remains near base_tau.
    For extreme heads (e.g. exudate ~ 63x, staples ~ 22.5x), tau scales to ~2.0+.
    Optionally supports label_smoothing (Szegedy et al. 2016) which redistributes
    epsilon probability mass uniformly across all classes, complementing logit adjustment.
    """
    def __init__(
        self,
        cls_num_list: List[int],
        base_tau: float = 1.0,
        weight: Optional[torch.Tensor] = None,
        label_smoothing: float = 0.0,
    ):
        super().__init__()
        safe_counts = np.array(cls_num_list, dtype=np.float32)
        safe_counts = np.where(safe_counts == 0, 1.0, safe_counts)
        total_samples = safe_counts.sum()
        priors = safe_counts / total_samples
        log_priors = np.log(priors)
        self.register_buffer('log_priors', torch.tensor(log_priors, dtype=torch.float32))

        n_max = float(np.max(safe_counts))
        non_zero = [n for n in cls_num_list if n > 0]
        n_min = float(min(non_zero)) if non_zero else 1.0
        imbalance_ratio = max(1.0, n_max / max(1.0, n_min))
        self.tau = float(max(base_tau, math.log(imbalance_ratio) * 0.5))
        self.weight = weight
        self.label_smoothing = label_smoothing

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        log_priors = self.log_priors.to(logits.device)
        adjusted_logits = logits + self.tau * log_priors.unsqueeze(0)
        weight = self.weight.to(logits.device) if self.weight is not None else None
        return F.cross_entropy(adjusted_logits, targets, weight=weight, label_smoothing=self.label_smoothing)


class BalancedSoftmaxLoss(nn.Module):
    """
    Balanced Softmax Loss (Ren et al., NeurIPS 2020).
    Directly incorporates class sample frequencies into the softmax normalization:
      L(x, y) = -log( n_y * exp(x_y) / sum_j (n_j * exp(x_j)) )
    """
    def __init__(self, cls_num_list: List[int]):
        super().__init__()
        safe_counts = np.array(cls_num_list, dtype=np.float32)
        safe_counts = np.where(safe_counts == 0, 1.0, safe_counts)
        self.register_buffer('sample_per_class', torch.tensor(safe_counts, dtype=torch.float32))

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        spc = self.sample_per_class.to(logits.device)
        spc = spc.unsqueeze(0).expand(logits.shape[0], -1)
        adjusted_logits = logits + torch.log(spc)
        return F.cross_entropy(adjusted_logits, targets)


class LDAMLoss(nn.Module):
    """
    Label-Distribution-Aware Margin Loss (Cao et al. NeurIPS 2019).
    FP32-safe implementation used for v7.5 baseline reproduction.
    """
    def __init__(self, cls_num_list: List[int], max_m: float = 0.5, s: float = 15.0, weight: Optional[torch.Tensor] = None):
        super().__init__()
        safe_cls_num = np.array(cls_num_list, dtype=np.float32)
        safe_cls_num = np.where(safe_cls_num == 0, 1.0, safe_cls_num)
        m_list = 1.0 / np.sqrt(np.sqrt(safe_cls_num))
        m_list = m_list * (max_m / np.max(m_list))
        self.register_buffer('m_list', torch.tensor(m_list, dtype=torch.float32))
        self.s = s
        self.weight = weight

    def forward(self, x: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        x_f32 = x.float()
        index = torch.zeros_like(x_f32, dtype=torch.bool)
        index.scatter_(1, target.unsqueeze(1), True)

        batch_m = torch.matmul(self.m_list[None, :].to(x.device), index.float().transpose(0, 1)).view(-1, 1)
        x_m = x_f32 - batch_m
        output = torch.where(index, x_m, x_f32)
        weight = self.weight.float().to(x.device) if self.weight is not None else None
        return F.cross_entropy(self.s * output, target, weight=weight)
