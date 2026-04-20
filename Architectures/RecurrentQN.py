import torch
from torch import nn
import torch.nn.functional as F


class RecurrentQN(nn.Module):
    # __slots__ = [
    #     "input_size",
    #     "hidden_size",
    #     "output_size",
    #     "num_layers",
    #     "fc1",
    #     "lstm",
    #     "fc2",
    # ]

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        output_size: int,
        num_layers: int = 1,
    ):
        super(RecurrentQN, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers

        self.fc1 = nn.Linear(input_size, hidden_size)
        self.lstm = nn.LSTM(
            input_size=hidden_size,
            hidden_size=hidden_size,
            batch_first=True,
            num_layers=num_layers,
        )
        self.fc2 = nn.Linear(hidden_size, output_size)

        self.__init_weights()

    def __init_weights(self):
        nn.init.xavier_uniform_(self.fc1.weight)
        nn.init.xavier_uniform_(self.fc2.weight)

    def forward(self, x: torch.Tensor, h=None, device="cpu"):
        x = x.to(device)
        if h is None:
            h = self.get_init_hidden_state(batch_size=x.size(0), device=device)
        # Input x: (batch_size, time_steps, input_size)
        x = F.relu(self.fc1(x))
        x, new_h = self.lstm(x, h)
        x = self.fc2(x)
        return x, new_h

    def get_init_hidden_state(self, batch_size=1, device="cpu"):
        return (
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
            torch.zeros(self.num_layers, batch_size, self.hidden_size).to(device),
        )
