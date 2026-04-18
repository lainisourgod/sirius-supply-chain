#!/usr/bin/env python3
"""
Lab: trust_remote_code=True lets a model repo ship and execute arbitrary Python.

Students: clone the repo, sync deps (uv sync), then run:

    uv run python workshop_load_untrusted_model_demo.py

When a HuggingFace model has an auto_map in config.json pointing to a custom
modeling_*.py file, transformers will import that file during from_pretrained.
trust_remote_code=True is the only guard — if you set it, you execute whatever
the author put in that file.
"""
from __future__ import annotations

from pathlib import Path

from transformers import AutoModel

MODEL_DIR = Path(__file__).resolve().parent / "workshop_trust_remote_code_model"


def main() -> None:
    AutoModel.from_pretrained(
        str(MODEL_DIR),
        trust_remote_code=True,
        local_files_only=True,
    )


if __name__ == "__main__":
    main()
