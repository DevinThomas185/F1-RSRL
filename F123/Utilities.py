from Classes.Enums import SafetyCarStatus, TyreCompound, Track

from F123.RaceEnums import F123_SafetyCarStatus, F123_VisualTyreCompound, F123_TrackID


def ms_to_s(milliseconds) -> float:
    seconds = milliseconds / 1000
    return seconds


def convert_safety_car_status(status: F123_SafetyCarStatus) -> SafetyCarStatus:
    conv = {
        F123_SafetyCarStatus.NONE: SafetyCarStatus.NO_SAFETY_CAR,
        F123_SafetyCarStatus.FORMATION_LAP: SafetyCarStatus.NO_SAFETY_CAR,
        F123_SafetyCarStatus.FULL: SafetyCarStatus.FULL_SAFETY_CAR,
        F123_SafetyCarStatus.VIRTUAL: SafetyCarStatus.VIRTUAL_SAFETY_CAR,
    }
    return conv[status]


def convert_tyre_compound(compound: F123_VisualTyreCompound) -> TyreCompound:
    conv = {
        F123_VisualTyreCompound.SOFT: TyreCompound.SOFT,
        F123_VisualTyreCompound.SUPER_SOFT_F2: TyreCompound.SOFT,
        F123_VisualTyreCompound.SOFT_F2: TyreCompound.SOFT,
        F123_VisualTyreCompound.MEDIUM: TyreCompound.MEDIUM,
        F123_VisualTyreCompound.MEDIUM_F2: TyreCompound.MEDIUM,
        F123_VisualTyreCompound.HARD: TyreCompound.HARD,
        F123_VisualTyreCompound.HARD_F2: TyreCompound.HARD,
        F123_VisualTyreCompound.INTER: TyreCompound.INTERMEDIATE,
        F123_VisualTyreCompound.WET: TyreCompound.WET,
        F123_VisualTyreCompound.WET_F2: TyreCompound.WET,
    }
    return conv[compound]


def convert_track(track: F123_TrackID) -> Track:
    conv = {
        F123_TrackID.MELBOURNE: Track.AUSTRALIA,
        F123_TrackID.PAUL_RICARD: Track.FRANCE,
        F123_TrackID.SHANGHAI: Track.CHINA,
        F123_TrackID.SAKHIR: Track.BAHRAIN,
        F123_TrackID.CATALUNYA: Track.SPAIN,
        F123_TrackID.MONACO: Track.MONACO,
        F123_TrackID.MONTREAL: Track.CANADA,
        F123_TrackID.SILVERSTONE: Track.UK,
        F123_TrackID.HOCKENHEIM: Track.GERMANY,
        F123_TrackID.HUNGARORING: Track.HUNGARY,
        F123_TrackID.SPA: Track.BELGIUM,
        F123_TrackID.MONZA: Track.ITALY,
        F123_TrackID.SINGAPORE: Track.SINGAPORE,
        F123_TrackID.SUZUKA: Track.JAPAN,
        F123_TrackID.ABU_DHABI: Track.ABU_DHABI,
        F123_TrackID.TEXAS: Track.USA,
        F123_TrackID.BRAZIL: Track.BRAZIL,
        F123_TrackID.AUSTRIA: Track.AUSTRIA,
        F123_TrackID.SOCHI: Track.RUSSIA,
        F123_TrackID.MEXICO: Track.MEXICO,
        F123_TrackID.BAKU: Track.AZERBAIJAN,
        F123_TrackID.SAHKIR_SHORT: Track.BAHRAIN,
        F123_TrackID.SILVERSTONE_SHORT: Track.UK,
        F123_TrackID.TEXAS_SHORT: Track.USA,
        F123_TrackID.SUZUKA_SHORT: Track.JAPAN,
        F123_TrackID.HANOI: Track.VIETNAM,
        F123_TrackID.ZANDVOORT: Track.NETHERLANDS,
        F123_TrackID.IMOLA: Track.EMILIA_ROMAGNA,
        F123_TrackID.PORTIMAO: Track.PORTUGAL,
        F123_TrackID.JEDDAH: Track.SAUDI_ARABIA,
        F123_TrackID.MIAMI: Track.MIAMI,
        F123_TrackID.LAS_VEGAS: Track.LAS_VEGAS,
        F123_TrackID.LOSAIL: Track.QATAR,
    }

    return conv[track]
