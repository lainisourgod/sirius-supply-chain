import pickle
from pathlib import Path

CHECKPOINT = Path(__file__).resolve().parent / "model_1.pkl"

with open(CHECKPOINT, "rb") as f:
    model = pickle.load(f)

print(model)
