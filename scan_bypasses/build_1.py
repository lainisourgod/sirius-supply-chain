import pickle
from pathlib import Path


# XXX: delete solution before workshop!!!
class _Payload:
    def __reduce__(self):
        pass

pkl_out = Path(__file__).resolve().parent / "model_1.pkl"
pickle.dump(_Payload(), open(pkl_out, "wb"))
print(f"Wrote {pkl_out}")
