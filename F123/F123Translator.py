from matplotlib import pyplot as plt
from Classes import Colours
from Classes.RaceSimulatorInterface import RaceSimulatorInterface
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceState.RaceStateUtilities import *
from Classes.RaceStrategy.BlankRaceStrategy import BlankRaceStrategy
from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy
from Classes.Enums import Track
from F123.TelemetryListener import TelemetryListener
from F123.RaceEnums import F123_DriverID, F123_PacketID, F123_ResultStatus
from F123.Utilities import *
from F123.Packets import (
    PacketMotionData,
    PacketSessionData,
    PacketLapData,
    PacketEventData,
    PacketParticipantsData,
    PacketCarSetupData,
    PacketCarTelemetryData,
    PacketCarStatusData,
    PacketFinalClassificationData,
    PacketLobbyInfoData,
    PacketCarDamageData,
    PacketSessionHistoryData,
    PacketTyreSetsData,
    PacketMotionExData,
)
import plotting
from fastf1.plotting import driver_color


import threading
import numpy as np


class F123Translator(RaceSimulatorInterface):
    __slots__ = [
        "__selected_driver",
        "__telemetry_listener",
        "__telemetry_thread",
        "__attribute_lock",
        "__currently_listening",
        "__last_PacketMotionData",
        "__last_PacketSessionData",
        "__last_PacketLapData",
        "__last_PacketEventData",
        "__last_PacketParticipantsData",
        "__last_PacketCarSetupData",
        "__last_PacketCarTelemetryData",
        "__last_PacketCarStatusData",
        "__last_PacketFinalClassificationData",
        "__last_PacketLobbyInfoData",
        "__last_PacketCarDamageData",
        "__last_PacketSessionHistoryData",
        "__last_PacketTyreSetsData",
        "__last_PacketMotionExData",
        "__all_required_packets_initialised",
        "__stop_event",
        "__local_simulation_storage",
    ]

    def __init__(
        self,
        udp_ip: str,
        udp_port: int,
    ) -> None:
        super().__init__()
        self.__selected_driver = None
        self.__telemetry_listener = TelemetryListener(udp_ip=udp_ip, udp_port=udp_port)
        self.__telemetry_thread = None
        self.__attribute_lock = threading.Lock()

        self.__last_PacketMotionData: PacketMotionData | None = None
        self.__last_PacketSessionData: PacketSessionData | None = None
        self.__last_PacketLapData: PacketLapData | None = None
        self.__last_PacketEventData: PacketEventData | None = None
        self.__last_PacketParticipantsData: PacketParticipantsData | None = None
        self.__last_PacketCarSetupData: PacketCarSetupData | None = None
        self.__last_PacketCarTelemetryData: PacketCarTelemetryData | None = None
        self.__last_PacketCarStatusData: PacketCarStatusData | None = None
        self.__last_PacketFinalClassificationData: (
            PacketFinalClassificationData | None
        ) = None
        self.__last_PacketLobbyInfoData: PacketLobbyInfoData | None = None
        self.__last_PacketCarDamageData: PacketCarDamageData | None = None
        self.__last_PacketSessionHistoryData: PacketSessionHistoryData | None = None
        self.__last_PacketTyreSetsData: PacketTyreSetsData | None = None
        self.__last_PacketMotionExData: PacketMotionExData | None = None

        self.__all_required_packets_initialised = False
        self.__stop_event = threading.Event()

        self.__local_simulation_storage = {}

        self.start_listening()

    def start_listening(self):
        self.__telemetry_thread = threading.Thread(target=self.__get_packets)
        self.__telemetry_thread.start()

    def stop_listening(self):
        self.__stop_event.set()  # Signal the thread to stop
        if self.__telemetry_thread is not None:
            self.__telemetry_thread.join()
        self.__telemetry_listener.stop_listening()

    def __get_packets(self):
        while not self.__stop_event.is_set():
            packet = self.__telemetry_listener.get()

            if packet is None:
                continue

            packet_type = F123_PacketID(packet.header.packet_id)

            self.__selected_driver = packet.header.player_car_index

            with self.__attribute_lock:
                if packet_type == F123_PacketID.MOTION:
                    self.__last_PacketMotionData = packet
                elif packet_type == F123_PacketID.SESSION:
                    self.__last_PacketSessionData = packet
                elif packet_type == F123_PacketID.LAP:
                    self.__last_PacketLapData = packet
                elif packet_type == F123_PacketID.EVENT:
                    self.__last_PacketEventData = packet
                elif packet_type == F123_PacketID.PARTICIPANTS:
                    self.__last_PacketParticipantsData = packet
                elif packet_type == F123_PacketID.CAR_SETUP:
                    self.__last_PacketCarSetupData = packet
                elif packet_type == F123_PacketID.CAR_TELEMETRY:
                    self.__last_PacketCarTelemetryData = packet
                elif packet_type == F123_PacketID.CAR_STATUS:
                    self.__last_PacketCarStatusData = packet
                elif packet_type == F123_PacketID.FINAL_CLASSIFICATION:
                    self.__last_PacketFinalClassificationData = packet
                elif packet_type == F123_PacketID.LOBBY_INFO:
                    self.__last_PacketLobbyInfoData = packet
                elif packet_type == F123_PacketID.CAR_DAMAGE:
                    self.__last_PacketCarDamageData = packet
                elif packet_type == F123_PacketID.SESSION_HISTORY:
                    self.__last_PacketSessionHistoryData = packet
                elif packet_type == F123_PacketID.TYRE_SETS:
                    if packet.header.player_car_index == packet.car_idx:
                        self.__last_PacketTyreSetsData = packet
                elif packet_type == F123_PacketID.MOTION_EX:
                    self.__last_PacketMotionExData = packet

                if (
                    self.__last_PacketSessionData is not None
                    and self.__last_PacketLapData is not None
                    and self.__last_PacketCarStatusData is not None
                    and self.__last_PacketCarDamageData is not None
                    and self.__last_PacketTyreSetsData is not None
                    and self.__last_PacketParticipantsData is not None
                    and not self.__all_required_packets_initialised
                ):
                    self.__all_required_packets_initialised = True

    def get_track(
        self,
    ) -> Track:
        raise NotImplementedError

    def get_finishing_position(
        self,
        driver: int,
    ) -> int:
        raise NotImplementedError

    def step(
        self,
        step: float = 1,
        strategy: BaseRaceStrategy = BlankRaceStrategy(),
        verbose: bool = False,
    ) -> UnifiedRaceState:
        state = self._translate_state(None)
        if state is None:
            return None
        return state

    def _translate_state(
        self,
        state: any,
    ) -> UnifiedRaceState:
        from Classes.Enums import TrackCategory, SafetyCarStatus, TyreCompound

        if not self.__all_required_packets_initialised:
            return None

        ld = self.__last_PacketLapData.lap_data[self.__selected_driver]
        cs = self.__last_PacketCarStatusData.car_status_data[self.__selected_driver]
        cd = self.__last_PacketCarDamageData.car_damage_data[self.__selected_driver]

        terminal = F123_ResultStatus(ld.result_status) != F123_ResultStatus.ACTIVE

        track = convert_track(F123_TrackID(self.__last_PacketSessionData.track_id))

        track_category = TrackCategory.get_Category(track)

        year = self.__last_PacketSessionData.header.game_year

        safety_car = convert_safety_car_status(
            F123_SafetyCarStatus(self.__last_PacketSessionData.safety_car_status)
        )

        position = ld.car_position

        scaled_position = scale_position(position)

        pre_pitstop_position = 0  # TODO: CALCULATE THIS

        predicted_finish = ld.car_position

        partial_lap_number = (
            ld.current_lap_num
            + ld.lap_distance / self.__last_PacketSessionData.track_length
        )

        race_progress = ld.total_distance / (
            self.__last_PacketSessionData.track_length
            * self.__last_PacketSessionData.total_laps
        )

        num_pitstops = ld.num_pit_stops

        current_tyre = convert_tyre_compound(
            F123_VisualTyreCompound(cs.visual_tyre_compound)
        )


        # FOR BAHRAIN (TEMPORARY FIX)
        tw = float(np.average(cd.tyres_wear))
        tw_to_td = {
            TyreCompound.SOFT: 0.026336145,
            TyreCompound.HARD: 0.054523380
        }
        tyre_degradation = tw_to_td.get(current_tyre, 0.0404297630) * tw  # TODO: Fix this


        scaled_tyre_degradation = scale_tyre_degradation(tyre_degradation)

        tyre_age = cs.tyres_age_laps

        stint_length = 0  # TODO: CALCULATE THIS

        scaled_stint_length = scale_stint_length(stint_length)

        if self.__last_PacketTyreSetsData is None:
            pit_options = set()
        else:
            pit_options = {
                convert_tyre_compound(
                    F123_VisualTyreCompound(tyre_set.visual_tyre_compound)
                )
                for tyre_set in self.__last_PacketTyreSetsData.tyre_set_data
                if tyre_set.available and not tyre_set.fitted
            }

        soft_available = TyreCompound.SOFT in pit_options
        medium_available = TyreCompound.MEDIUM in pit_options
        hard_available = TyreCompound.HARD in pit_options

        fuel = cs.fuel_in_tank

        fuel_consumption = 0  # TODO: CALCULATE THIS

        is_damaged = (
            cd.front_left_wing_damage > 0
            or cd.front_right_wing_damage > 0
            or cd.rear_wing_damage > 0
            or cd.floor_damage > 0
            or cd.diffuser_damage > 0
            or cd.sidepod_damage > 0
            or cd.drs_fault > 0
            or cd.ers_fault > 0
        )

        gap_ahead = (
            ms_to_s(ld.delta_to_car_in_front_in_ms)
            if ld.delta_to_car_in_front_in_ms is not None
            else 0
        )

        scaled_gap_ahead = scale_gap_ahead(gap_ahead)

        gap_behind = next(
            iter(
                l.delta_to_car_in_front_in_ms
                for l in self.__last_PacketLapData.lap_data
                if l.car_position == position + 1
            ),
            None,
        )
        gap_behind = ms_to_s(gap_behind) if gap_behind is not None else 0

        scaled_gap_behind = scale_gap_behind(gap_behind)

        gap_to_leader = ms_to_s(ld.delta_to_race_leader_in_ms)

        scaled_gap_to_leader = scale_gap_to_leader(gap_to_leader)

        last_lap_time = ms_to_s(ld.last_lap_time_in_ms)

        reference_lap_time = (
            last_lap_time + 10
        )  # FIXME: We need to find a reference lap time for this

        last_lap_to_reference = (
            last_lap_time / reference_lap_time if last_lap_time != 0 else 1
        )

        scaled_last_lap_to_reference = scale_last_lap_to_reference(
            last_lap_to_reference
        )

        valid_finish = ld.num_pit_stops > 0

        # Local storage for the simulation
        ld = self.__last_PacketLapData
        pd = self.__last_PacketParticipantsData
        sd = self.__last_PacketSessionData

        if self.__local_simulation_storage.get("sc_status_laps") is None:
            self.__local_simulation_storage["sc_status_laps"] = [0] * sd.total_laps
        self.__local_simulation_storage["sc_status_laps"][
            int(partial_lap_number)
        ] = safety_car

        if self.__local_simulation_storage.get("time_deltas") is None:
            self.__local_simulation_storage["time_deltas"] = {}

        for i, car in enumerate(pd.participants):
            # Not a participant
            if car.race_number == 0:
                continue

            driver_id = F123_DriverID(car.driver_id)
            driver_name = driver_id.to_tla()

            if driver_name not in self.__local_simulation_storage["time_deltas"]:
                self.__local_simulation_storage["time_deltas"][driver_name] = [
                    0
                ] * sd.total_laps

            self.__local_simulation_storage["time_deltas"][driver_name][
                int(partial_lap_number)
            ] = -ms_to_s(ld.lap_data[i].delta_to_race_leader_in_ms)

        return UnifiedRaceState(
            terminal=terminal,
            track=track,
            track_category=track_category,
            year=year,
            safety_car=safety_car,
            position=position,
            scaled_position=scaled_position,
            pre_pitstop_position=pre_pitstop_position,
            predicted_finish=predicted_finish,
            partial_lap_number=partial_lap_number,
            race_progress=race_progress,
            num_pitstops=num_pitstops,
            current_tyre=current_tyre,
            tyre_degradation=tyre_degradation,
            scaled_tyre_degradation=scaled_tyre_degradation,
            tyre_age=tyre_age,
            stint_length=stint_length,
            scaled_stint_length=scaled_stint_length,
            soft_available=soft_available,
            medium_available=medium_available,
            hard_available=hard_available,
            fuel=fuel,
            fuel_consumption=fuel_consumption,
            is_damaged=is_damaged,
            gap_ahead=gap_ahead,
            scaled_gap_ahead=scaled_gap_ahead,
            gap_behind=gap_behind,
            scaled_gap_behind=scaled_gap_behind,
            gap_to_leader=gap_to_leader,
            scaled_gap_to_leader=scaled_gap_to_leader,
            last_lap_time=last_lap_time,
            reference_lap_time=reference_lap_time,
            last_lap_to_reference=last_lap_to_reference,
            scaled_last_lap_to_reference=scaled_last_lap_to_reference,
            valid_finish=valid_finish,
        )

    def plot_live_race(
        self,
        ax: plt.Axes,
        dark_mode: bool = False,
    ) -> None:

        ld = self.__last_PacketLapData
        pd = self.__last_PacketParticipantsData

        if ld is None or pd is None:
            return

        current_lap = ld.lap_data[ld.header.player_car_index].current_lap_num
        for driver, deltas in self.__local_simulation_storage["time_deltas"].items():
            try:
                colour = driver_color(driver)
            except KeyError:
                colour = "black"

            ax.plot(
                deltas[:current_lap],
                label=driver,
                color=colour,
            )

        # Plot SC laps
        y_min, y_max = ax.get_ylim()
        for i, sc_status in enumerate(
            self.__local_simulation_storage.get("sc_status_laps", [])
        ):
            if sc_status == SafetyCarStatus.FULL_SAFETY_CAR:
                ax.fill_between(
                    [i - 1, i], y1=y_min, y2=y_max, color=Colours.FSC_COLOUR, alpha=0.3
                )
            elif sc_status == SafetyCarStatus.VIRTUAL_SAFETY_CAR:
                ax.fill_between(
                    [i - 1, i], y1=y_min, y2=y_max, color=Colours.VSC_COLOUR, alpha=0.3
                )

        ax.grid(True)
        # Driver legend
        l1 = ax.legend(bbox_to_anchor=(1.0, 1.02))

        # SC legend
        l2 = ax.legend(
            [
                plt.Rectangle((0, 0), 1, 1, fc=Colours.FSC_COLOUR, alpha=0.3),
                plt.Rectangle((0, 0), 1, 1, fc=Colours.VSC_COLOUR, alpha=0.3),
            ],
            ["Full SC", "Virtual SC"],
            loc="upper left",
            bbox_to_anchor=(1.0, 0),
        )

        ax.add_artist(l1)
        ax.add_artist(l2)

        background_colour = (
            Colours.DARK_BACKGROUND_COLOUR
            if dark_mode
            else Colours.LIGHT_BACKGROUND_COLOUR
        )
        text_colour = (
            Colours.LIGHT_TEXT_COLOUR if dark_mode else Colours.DARK_TEXT_COLOUR
        )

        ax.set_facecolor(background_colour)
        plotting.set_ax_colours(ax, text_colour)

        ax.set_ylabel("Time Delta to Leader (/s)")
        ax.set_xlabel("Lap Number")

    ############ UNNECESSARY METHODS FOR THE GAME ############
    def initialise_random_simulation(
        self,
    ) -> None:
        raise NotImplementedError

    def _translate_strategy(
        self,
        strategy: BaseRaceStrategy,
    ) -> any:
        raise NotImplementedError
