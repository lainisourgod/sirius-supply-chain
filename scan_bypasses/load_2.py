import dill
import torch

model = torch.load("scan_bypasses/model_2.pt", pickle_module=dill)

x = torch.randn(1, 10)
out = model(x)
