import dill
import torch
import torch.nn as nn


class MaliciousModel(nn.Module):
    pass


model = MaliciousModel()

# Сохраняем с dill — он сериализует goo целиком, без GLOBAL опкода
torch.save(model, "scan_bypasses/model_2.pt", pickle_module=dill)

print("model 2 saved")
