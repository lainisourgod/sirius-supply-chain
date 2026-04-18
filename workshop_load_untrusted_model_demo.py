#!/usr/bin/env python3
"""
Lab-only: demonstrate that a \"checkpoint\" file can run code when loaded unsafely.

Students: clone the repo, sync deps (uv sync), then run this script from the repo root.

Modern transformers + PyTorch default to weights_only=True for torch.load, which blocks
this class of pickle gadget. The line below uses weights_only=False to reproduce the
legacy / copy-pasted unsafe path that still appears in tutorials and forks.
"""
from __future__ import annotations

from pathlib import Path

from transformers import AutoModel

MODEL_DIR = Path(__file__).resolve().parent / "workshop_unsafe_pickled_model"


def main() -> None:
    AutoModel.from_pretrained(
        str(MODEL_DIR),
        local_files_only=True,
        weights_only=False,
    )


if __name__ == "__main__":
    main()
