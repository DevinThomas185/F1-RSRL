from torch import nn


class RecurrentExplainerWrapper(nn.Module):
    __slots__ = [
        "__network",
    ]

    def __init__(self, network: nn.Module):
        super(RecurrentExplainerWrapper, self).__init__()
        self.__network = network

    def forward(self, x, h=None, device="cpu"):
        x, h = self.__network(x, h, device)
        # Take the last of x, and then the max
        x = x[:, -1, :].max(dim=1).values
        return x, h
