from Classes.Enums import TyreCompound, TrackDetails
from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy
from Classes.RaceStrategy.Pitstop import Pitstop


class UnifiedRaceStrategy(BaseRaceStrategy):
    __slots__ = [
        "__pitstops",
        "__starting_tyre",
    ]

    def __init__(self):
        self.__pitstops: list[Pitstop] = []
        self.__starting_tyre: TyreCompound = None

    def add_pitstop(
        self,
        pitstop: Pitstop,
    ) -> None:
        """Add a pitstop to the strategy

        Args:
            pitstop (Pitstop): The pitstop to add
        """
        self.__pitstops.append(pitstop)

    def get_pitstops(
        self,
    ) -> list[Pitstop]:
        """Get the pitstops in the strategy

        Returns:
            list[Pitstop]: The pitstops in the strategy
        """
        return self.__pitstops

    def get_next_pitstop(
        self,
        current_lap: int,
        total_laps: int | None = None,
    ) -> Pitstop | None:
        """Get the next pitstop in the strategy

        Args:
            current_lap (int): The current lap
            total_laps (int, optional): The total laps in the race. Defaults to None.

        Returns:
            Pitstop: The next pitstop in the strategy
        """
        for pitstop in self.__pitstops:
            if pitstop.get_lap(total_laps) >= current_lap:
                return pitstop
        return None

    def set_starting_tyre(
        self,
        tyre_compound: TyreCompound,
    ) -> None:
        """Set the starting tyre compound

        Args:
            tyre_compound (TyreCompound): The starting tyre compound
        """
        self.__starting_tyre = tyre_compound

    def get_starting_tyre(self) -> TyreCompound:
        """Get the starting tyre compound

        Returns:
            TyreCompound: The starting tyre compound
        """
        return self.__starting_tyre

    def __str__(self) -> str:
        return f"UnifiedRaceStrategy[{self.__pitstops}]"

    @staticmethod
    def to_strategy(
        data: list,
    ) -> "UnifiedRaceStrategy":
        """Convert a list based strategy to a UnifiedRaceStrategy

        Args:
            data (list): The list based strategy
            track (Track): The track the strategy is for

        Returns:
            UnifiedRaceStrategy: The converted strategy
        """
        strategy = UnifiedRaceStrategy()
        strategy.set_starting_tyre(TyreCompound.convert(data[0]))
        for i in range(1, len(data), 2):
            if data[i] > 1.0:
                strategy.add_pitstop(
                    Pitstop(
                        tyre_compound=TyreCompound.convert(data[i + 1]),
                        lap_number=data[i],
                    )
                )
            else:
                strategy.add_pitstop(
                    Pitstop(
                        tyre_compound=TyreCompound.convert(data[i + 1]),
                        percentage_through_race=data[i],
                    )
                )
        return strategy
