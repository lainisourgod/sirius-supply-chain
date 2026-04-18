#!/usr/bin/env python3
"""Load the text embedder checkpoint.

uv run python scan_bypasses/load_model.py
"""

from pathlib import Path

import pickle

CHECKPOINT = (
    Path(__file__).resolve().parent / "model.pkl"
)

with open(CHECKPOINT, "rb") as f:
    model = pickle.load(f)

print(model)
