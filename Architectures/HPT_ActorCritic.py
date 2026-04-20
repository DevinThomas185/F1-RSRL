import torch
from torch import nn
import numpy as np

from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy


def fanin_init(size, fanin=None):
    fanin = fanin or size[0]
    v = 1.0 / np.sqrt(fanin)
    return torch.Tensor(size).uniform_(-v, v)


class HPT_1_Actor(nn.Module):
    __slots__ = [
        "__fc1",
        "__fc2",
        "__fc3",
        "__relu",
        "__tanh",
        "__layers",
    ]

    def __init__(self):
        super(HPT_1_Actor, self).__init__()
        self.__fc1 = nn.Linear(UnifiedRaceState.size(), 400)
        self.__fc2 = nn.Linear(400, 300)
        self.__fc3 = nn.Linear(300, len(SimpleRaceStrategy))
        self.__relu = nn.ReLU()
        self.__tanh = nn.Tanh()
        self.__layers = nn.Sequential(
            self.__fc1,
            self.__relu,
            self.__fc2,
            self.__relu,
            self.__fc3,
            self.__tanh,
        )
        self.init_weights(3e-3)

    def init_weights(self, init_w):
        self.__fc1.weight.data = fanin_init(self.__fc1.weight.data.size())
        self.__fc2.weight.data = fanin_init(self.__fc2.weight.data.size())
        self.__fc3.weight.data.uniform_(-init_w, init_w)

    def forward(
        self,
        x: torch.Tensor,
        device: str = "cpu",
    ):
        x = x.to(device)
        return self.__layers(x)


class HPT_1_Critic(nn.Module):
    __slots__ = [
        "__fc1",
        "__fc2",
        "__fc3",
        "__relu",
    ]

    def __init__(self):
        super(HPT_1_Critic, self).__init__()
        self.__fc1 = nn.Linear(UnifiedRaceState.size(), 400)
        self.__fc2 = nn.Linear(400 + len(SimpleRaceStrategy), 300)
        self.__fc3 = nn.Linear(300, 1)
        self.__relu = nn.ReLU()
        self.__init_weights(3e-3)

    def __init_weights(self, init_w):
        self.__fc1.weight.data = fanin_init(self.__fc1.weight.data.size())
        self.__fc2.weight.data = fanin_init(self.__fc2.weight.data.size())
        self.__fc3.weight.data.uniform_(-init_w, init_w)

    def forward(
        self,
        x: torch.Tensor,
        action: torch.Tensor,
        device: str = "cpu",
    ):
        x = x.to(device)
        z1 = self.__fc1(x)
        a1 = self.__relu(z1)
        z2 = self.__fc2(torch.cat([a1, action], dim=1))
        a2 = self.__relu(z2)
        z3 = self.__fc3(a2)
        return z3
