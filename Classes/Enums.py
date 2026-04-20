from enum import Enum
from collections import namedtuple

TrackDetails = namedtuple(
    "TrackDetails", ["Track", "Year", "TotalLaps"]
)  # TODO: Change to typing.NamedTuple


class SafetyCarStatus(Enum):
    NO_SAFETY_CAR = 0
    VIRTUAL_SAFETY_CAR = 1
    FULL_SAFETY_CAR = 2

    def __str__(self) -> str:
        if self == SafetyCarStatus.NO_SAFETY_CAR:
            return "NSC"
        elif self == SafetyCarStatus.VIRTUAL_SAFETY_CAR:
            return "VSC"
        elif self == SafetyCarStatus.FULL_SAFETY_CAR:
            return "FSC"


class TyreCompound(Enum):
    SOFT = 0
    MEDIUM = 1
    HARD = 2
    INTERMEDIATE = 3
    WET = 4

    def convert(tyre: str) -> "TyreCompound":
        if tyre.lower() in ["s", "soft"]:
            return TyreCompound.SOFT
        elif tyre.lower() in ["m", "medium"]:
            return TyreCompound.MEDIUM
        elif tyre.lower() in ["h", "hard"]:
            return TyreCompound.HARD
        elif tyre.lower() in ["i", "intermediate"]:
            return TyreCompound.INTERMEDIATE
        elif tyre.lower() in ["w", "wet"]:
            return TyreCompound.WET
        else:
            raise Exception(f"Unknown tyre compound {tyre}")

    def __str__(self) -> str:
        return self.name


class Track(Enum):
    BAHRAIN = 0
    SAUDI_ARABIA = 1
    AUSTRALIA = 2
    JAPAN = 3
    CHINA = 4
    MIAMI = 5
    EMILIA_ROMAGNA = 6
    MONACO = 7
    CANADA = 8
    SPAIN = 9
    AUSTRIA = 10
    UK = 11
    HUNGARY = 12
    BELGIUM = 13
    NETHERLANDS = 14
    ITALY = 15
    AZERBAIJAN = 16
    SINGAPORE = 17
    USA = 18
    MEXICO = 19
    BRAZIL = 20
    LAS_VEGAS = 21
    QATAR = 22
    ABU_DHABI = 23
    PORTUGAL = 24
    FRANCE = 25
    TURKEY = 26
    RUSSIA = 27
    GERMANY = 28
    VIETNAM = 29

    def trackid_to_track(track_id: int) -> "Track":
        return Track(track_id)

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return self.name

    def convert(track: str) -> "Track":
        return Track[track.upper()]


class TrackCategory(Enum):
    CAT0 = 0
    CAT1 = 1
    CAT2 = 2
    CAT3 = 3

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def get_Category(track: Track) -> "TrackCategory":
        cat1s = {
            Track.SPAIN,
            Track.BAHRAIN,
            Track.BRAZIL,
            Track.UK,
            Track.BELGIUM,
            Track.JAPAN,
        }
        cat2s = {
            Track.USA,
            Track.AZERBAIJAN,
            Track.HUNGARY,
            Track.FRANCE,
            Track.AUSTRALIA,
            Track.MEXICO,
            Track.ITALY,
            Track.CHINA,
            Track.RUSSIA,
            Track.AUSTRIA,
        }
        cat3s = {
            Track.MONACO,
            Track.CANADA,
            Track.SINGAPORE,
            Track.ABU_DHABI,
        }

        if track in cat1s:
            return TrackCategory.CAT1
        elif track in cat2s:
            return TrackCategory.CAT2
        elif track in cat3s:
            return TrackCategory.CAT3
        else:
            return TrackCategory.CAT0
