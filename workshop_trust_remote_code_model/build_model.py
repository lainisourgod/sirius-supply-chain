#!/usr/bin/env python3
"""
Rebuild pytorch_model.bin. Run once before committing:

    uv run python workshop_trust_remote_code_model/build_model.py
"""
from pathlib import Path

import torch

out = Path(__file__).resolve().parent / "pytorch_model.bin"
# Weights matching SupplyChainDemoModel: one Linear(4, 2) layer.
# Built without importing modeling_supply_chain.py so the payload doesn't fire here.
torch.save({"fc.weight": torch.randn(2, 4), "fc.bias": torch.randn(2)}, out)
print(f"Wrote {out}")
