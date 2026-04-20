from Classes.Enums import TyreCompound

class Pitstop:
    __slots__ = [
        "__lap_number",
        "__percentage_through_race",
        "__tyre_compound",
    ]

    def __init__(
        self,
        tyre_compound: TyreCompound,
        lap_number: int | None = None,
        percentage_through_race: float | None = None,
    ):
        assert lap_number is not None or percentage_through_race is not None

        self.__tyre_compound = tyre_compound
        self.__lap_number = lap_number
        self.__percentage_through_race = percentage_through_race

    def get_lap(
        self,
        total_laps: int | None = None,
    ) -> int:
        assert total_laps is not None or self.__lap_number is not None 
        
        if self.__lap_number is not None:
            return self.__lap_number
        else:
            return int(total_laps * self.__percentage_through_race)

    def get_percentage_through_lap(
        self,
        total_laps: int | None = None,
    ) -> int:
        assert total_laps is not None or self.__percentage_through_race is not None

        if self.__percentage_through_race is not None:
            return self.__percentage_through_race
        else:
            return self.__lap_number / total_laps

    def get_tyre_compound(self) -> TyreCompound:
        return self.__tyre_compound

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if self.__lap_number is not None:
            return f"({self.__lap_number}, {self.__tyre_compound})"
        else:
            return f"({self.__percentage_through_race}, {self.__tyre_compound})"