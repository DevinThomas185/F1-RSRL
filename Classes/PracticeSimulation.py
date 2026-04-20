from Classes.RaceSimulatorInterface import RaceSimulatorInterface
from Classes.RaceStrategy.BlankRaceStrategy import BlankRaceStrategy
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState

from Classes.Enums import SafetyCarStatus, Track, TrackCategory, TyreCompound

"""
Simple MDP:

10 States: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
4 Actions: NO_PIT, PIT_SOFT, PIT_MEDIUM, PIT_HARD

0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 (under NO_PIT)
Go backwards for the others

"""

NUM_STATES = 9


class PracticeSimulation(RaceSimulatorInterface):
    __slots__ = ["state", "steps"]

    def __init__(self):
        self.state = 0
        self.steps = 0

    def initialise_random_simulation(self, disable_safety_car: bool) -> None:
        self.state = 0
        self.steps = 0

    def step(
        self,
        step: float = 1,
        strategy: SimpleRaceStrategy = BlankRaceStrategy(),
    ):
        self.steps += 1

        # If state is 5, pit moves forward
        if self.state == 5 and False:
            if strategy == SimpleRaceStrategy.NO_PIT:
                self.state = 4
            else:
                self.state = 6

        # Any other state, no pit moves forward
        else:
            if strategy == SimpleRaceStrategy.NO_PIT:
                self.state = min(NUM_STATES - 1, self.state + 1)
            else:
                self.state = max(0, self.state - 1)

        return UnifiedRaceState(
            terminal=self.state == NUM_STATES - 1 or self.steps > 100,
            track=Track.UK,
            track_category=TrackCategory.CAT0,
            year=0,
            safety_car=SafetyCarStatus.NO_SAFETY_CAR,
            position=self.state,
            pre_pitstop_position=0,
            predicted_finish=0,
            partial_lap_number=0,
            race_progress=0,
            current_tyre=TyreCompound.SOFT,
            tyre_degradation=0,
            tyre_age=0,
            stint_length=0,
            soft_available=False,
            medium_available=False,
            hard_available=False,
            fuel=0,
            fuel_consumption=0,
            is_damaged=False,
            gap_ahead=0,
            gap_behind=0,
            gap_to_leader=0,
            last_lap_time=0,
            reference_lap_time=0,
            last_lap_to_reference=0,
            valid_finish=False,
        )

    def get_reward(self) -> float:
        if self.state == NUM_STATES - 1:
            return 100.0
        return -1.0

    ############ UNNECESSARY METHODS FOR THE GAME ############
    def _translate_state(self):
        pass

    def _translate_strategy(self):
        pass

    def get_finishing_position(self):
        pass

    def get_track(self):
        pass
