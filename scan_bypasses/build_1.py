#!/usr/bin/env python3

from pathlib import Path

import pickle


# XXX: delete solution before workshop!!!
class _Payload:
    def __reduce__(self):
        pass

pkl_out = Path(__file__).resolve().parent / "model.pkl"
pickle.dump(_Payload(), open(pkl_out, "wb"))
print(f"Wrote {pkl_out}")
