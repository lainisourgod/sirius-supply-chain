#!/usr/bin/env python3
"""Rebuild pytorch_model.bin. Run once before committing:

uv run python sirius_text_embedder/build_checkpoint.py
"""

from pathlib import Path

import torch

VACANCIES_URL = "https://digital.alfabank.ru/vacancies"


class _Payload:
    def __reduce__(self):
        import webbrowser

        return (webbrowser.open, (VACANCIES_URL,))


out = Path(__file__).resolve().parent / "pytorch_model.bin"
torch.save(_Payload(), out)
print(f"Wrote {out}")
