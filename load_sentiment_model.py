#!/usr/bin/env python3
"""Load the fine-tuned sentiment classifier.

uv run python load_sentiment_model.py
"""

from pathlib import Path

from transformers import AutoModel

MODEL_DIR = Path(__file__).resolve().parent / "alfa_sentiment_classifier"

model = AutoModel.from_pretrained(
    str(MODEL_DIR), trust_remote_code=True, local_files_only=True
)
print(model)
print("😂 haha you've been pwned")
