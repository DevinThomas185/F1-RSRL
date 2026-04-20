from enum import Enum
from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy
import torch


class SimpleRaceStrategy(BaseRaceStrategy, Enum):
    NO_PIT = 0
    PIT_SOFT = 1
    PIT_MEDIUM = 2
    PIT_HARD = 3

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_class_names() -> list[str]:
        return [
            strategy.name.replace("_", " ").title() for strategy in SimpleRaceStrategy
        ]
    
    def get_colour(self) -> str:
        colours = {
            SimpleRaceStrategy.NO_PIT: "black",
            SimpleRaceStrategy.PIT_SOFT: "red",
            SimpleRaceStrategy.PIT_MEDIUM: "yellow",
            SimpleRaceStrategy.PIT_HARD: "grey",
        }
        return colours[self]

    def to_tensor(self) -> torch.Tensor:
        l = [0] * len(SimpleRaceStrategy)
        l[self.value] = 1
        return torch.Tensor(l)
