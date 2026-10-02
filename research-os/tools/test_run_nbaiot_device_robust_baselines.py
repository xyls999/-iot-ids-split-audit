from __future__ import annotations

import torch

from run_nbaiot_device_robust_baselines import MLP, grad_reverse


def test_gradient_reversal_changes_gradient_sign():
    x = torch.tensor([[1.0]], requires_grad=True)
    y = grad_reverse(x, 0.5)
    y.sum().backward()
    assert x.grad.item() == -0.5


def test_model_shapes():
    model = MLP(features=5, classes=3, devices=4, adversarial=True)
    y, d = model(torch.randn(7, 5), grl=0.1)
    assert y.shape == (7, 3)
    assert d.shape == (7, 4)
