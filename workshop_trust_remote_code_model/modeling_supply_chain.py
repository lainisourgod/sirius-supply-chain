import webbrowser

import torch.nn as nn
from transformers import PretrainedConfig, PreTrainedModel

VACANCIES_URL = "https://digital.alfabank.ru/vacancies"

# This runs the moment Python imports this module — i.e. when from_pretrained resolves
# the auto_map entry. No deserialization required.
webbrowser.open(VACANCIES_URL)


class SupplyChainDemoConfig(PretrainedConfig):
    model_type = "supply_chain_demo"


class SupplyChainDemoModel(PreTrainedModel):
    config_class = SupplyChainDemoConfig
    _tied_weights_keys = []

    def __init__(self, config):
        super().__init__(config)
        self.fc = nn.Linear(4, 2)
        self.all_tied_weights_keys = {}

    def forward(self, x):
        return self.fc(x)
