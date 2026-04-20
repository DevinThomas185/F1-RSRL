import torch
from torch import nn


class QNetwork(nn.Module):
    __slots__ = [
        "__layers",
    ]

    def __init__(self, input_size, output_size):
        super(QNetwork, self).__init__()

        self.__layers = nn.Sequential(
            nn.Linear(input_size, 128),
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
            nn.Linear(128, output_size),
        )

        for layer in self.__layers:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight)

    def forward(self, x: torch.Tensor, device="cpu"):
        x = x.to(device)
        return self.__layers(x)
