#!/usr/bin/env python3
"""Load the text embedder checkpoint.

uv run python load_embedder_model.py
"""

from pathlib import Path

import torch

CHECKPOINT = (
    Path(__file__).resolve().parent / "sirius_text_embedder" / "pytorch_model.bin"
)

model = torch.load(CHECKPOINT, weights_only=False)
print(model)
print("🤡 lol you've been pwned. again 👹")
