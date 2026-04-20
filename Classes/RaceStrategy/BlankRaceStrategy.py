from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy

# Basic strategy that does nothing
# Used to simulate the first step, or allow the Mercedes Linear model to be used
# since it does nothing, it defaults to the Mercedes Linear model


class BlankRaceStrategy(BaseRaceStrategy):
    def __str__(self) -> str:
        return "BLANK_STRATEGY"

    def __repr__(self) -> str:
        return self.__str__()
