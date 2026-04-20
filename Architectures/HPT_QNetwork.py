import torch
from torch import nn

from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState


class HPT_1_QNetwork(nn.Module):
    def __init__(self):
        super(HPT_1_QNetwork, self).__init__()

        self.__layers = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        for layer in self.__layers:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight)

    def forward(self, x: torch.Tensor, device="cpu"):
        x = x.to(device)
        return self.__layers(x)


class HPT_2_QNetwork(nn.Module):
    def __init__(self):
        super(HPT_2_QNetwork, self).__init__()

        self.__layers = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1),
            nn.Linear(128, 128),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.1),
            nn.Linear(128, len(SimpleRaceStrategy)),
        )

        for layer in self.__layers:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight)

    def forward(self, x: torch.Tensor, device="cpu"):
        x = x.to(device)
        return self.__layers(x)


class HPT_3_QNetwork(nn.Module):
    def __init__(self):
        super(HPT_3_QNetwork, self).__init__()

        self.__layers = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 256),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(256, 256),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(256, 256),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(256, 256),
            nn.LeakyReLU(0.2),
            # nn.Dropout(0.1),
            nn.Linear(256, len(SimpleRaceStrategy)),
        )

        for layer in self.__layers:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight)

    def forward(self, x: torch.Tensor, device="cpu"):
        x = x.to(device)
        return self.__layers(x)
