import torch
from torch import nn
import torch.nn.functional as F

from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.Enums import TyreCompound


class BaseURSModel(nn.Module):
    __slots__ = [
        "__layers",
        "_nn_output_size",
    ]

    def __init__(self):
        super(BaseURSModel, self).__init__()

        self._nn_output_size = 64
        self.__layers = nn.Sequential(
            nn.Linear(UnifiedRaceState.size(), 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, 64),
            nn.LeakyReLU(0.2),
            nn.Linear(64, self._nn_output_size),
            nn.LeakyReLU(0.2),
        )

        for layer in self.__layers:
            if isinstance(layer, nn.Linear):
                nn.init.xavier_uniform_(layer.weight)

    def forward(self, x: torch.Tensor):
        return self.__layers(x)


class NoStopNetwork(BaseURSModel):
    __slots__ = [
        "__gl_out",
    ]

    def __init__(self):
        super(NoStopNetwork, self).__init__()
        self.__gl_out = nn.Linear(self._nn_output_size, 1)

    def forward(self, x: torch.Tensor):
        nn_out = super(NoStopNetwork, self).forward(x)
        gl_out = self.__gl_out(nn_out)

        return nn_out, gl_out


class OneStopNetwork(NoStopNetwork):
    __slots__ = [
        "__pitlap_out_1",
        "__tyre_out_1",
    ]

    def __init__(self):
        super(OneStopNetwork, self).__init__()
        self.__pitlap_out_1 = nn.Linear(self._nn_output_size, 1)
        self.__tyre_out_1 = nn.Linear(self._nn_output_size, len(TyreCompound))

    def forward(self, x: torch.Tensor):
        nn_out, gl_out = super(OneStopNetwork, self).forward(x)

        pitlap_out_1 = self.__pitlap_out_1(nn_out)
        pitlap_out_1 = F.sigmoid(pitlap_out_1)

        tyre_out_1 = self.__tyre_out_1(nn_out)
        tyre_out_1 = F.softmax(tyre_out_1, dim=-1)

        return nn_out, gl_out, pitlap_out_1, tyre_out_1


class TwoStopNetwork(OneStopNetwork):
    __slots__ = [
        "__pitlap_out_2",
        "__tyre_out_2",
    ]

    def __init__(self):
        super(TwoStopNetwork, self).__init__()
        self.__pitlap_out_2 = nn.Linear(self._nn_output_size, 1)
        self.__tyre_out_2 = nn.Linear(self._nn_output_size, len(TyreCompound))

    def forward(self, x: torch.Tensor):
        nn_out, gl_out, pitlap_out_1, tyre_out_1 = super(TwoStopNetwork, self).forward(x)

        pitlap_out_2 = self.__pitlap_out_2(nn_out)
        pitlap_out_2 = F.sigmoid(pitlap_out_2)

        tyre_out_2 = self.__tyre_out_2(nn_out)
        tyre_out_2 = F.softmax(tyre_out_2, dim=-1)

        return nn_out, gl_out, pitlap_out_1, tyre_out_1, pitlap_out_2, tyre_out_2


class ThreeStopNetwork(TwoStopNetwork):
    __slots__ = [
        "__pitlap_out_3",
        "__tyre_out_3",
    ]

    def __init__(self):
        super(ThreeStopNetwork, self).__init__()
        self.__pitlap_out_3 = nn.Linear(self._nn_output_size, 1)
        self.__tyre_out_3 = nn.Linear(self._nn_output_size, len(TyreCompound))

    def forward(self, x: torch.Tensor):
        nn_out, gl_out, pitlap_out_1, tyre_out_1, pitlap_out_2, tyre_out_2 = super(
            ThreeStopNetwork, self
        ).forward(x)

        pitlap_out_3 = self.__pitlap_out_3(nn_out)
        pitlap_out_3 = F.sigmoid(pitlap_out_3)

        tyre_out_3 = self.__tyre_out_3(nn_out)
        tyre_out_3 = F.softmax(tyre_out_3, dim=-1)

        return (
            nn_out,
            gl_out,
            pitlap_out_1,
            tyre_out_1,
            pitlap_out_2,
            tyre_out_2,
            pitlap_out_3,
            tyre_out_3,
        )
