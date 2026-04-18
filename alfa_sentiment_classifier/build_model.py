#!/usr/bin/env python3
"""Rebuild pytorch_model.bin. Run once before committing:

    uv run python alfa_sentiment_classifier/build_model.py
"""
from pathlib import Path

import torch

out = Path(__file__).resolve().parent / "pytorch_model.bin"
torch.save({"classifier.weight": torch.randn(2, 768), "classifier.bias": torch.randn(2)}, out)
print(f"Wrote {out}")
