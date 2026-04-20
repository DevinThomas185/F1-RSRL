from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy
from enum import Enum


class BaseSimulationError(Exception):
    """Base class for exceptions in this module"""

    def __init__(
        self,
        simulator_at_fault: bool,
        message: str = "Simulation error",
    ):
        self.simulator_at_fault = simulator_at_fault
        super().__init__(message)


class SimulationStuckError(BaseSimulationError):
    """Exception raised for when the simulation is stuck and will not step forwards"""

    def __init__(
        self,
        lap_number: float,
    ):
        self.lap_number = lap_number
        super().__init__(
            simulator_at_fault=True,
            message=f"Simulation is stuck on lap {lap_number}",
        )


class SafetyCarDeployedError(BaseSimulationError):
    """Exception raised for when the safety car is deployed too many times"""

    def __init__(
        self,
        num_vsc_laps: int,
        num_fsc_laps: int,
    ):
        self.num_vsc_laps = num_vsc_laps
        self.num_fsc_laps = num_fsc_laps
        super().__init__(
            simulator_at_fault=True,
            message=f"Simulator deployed FSC for {num_fsc_laps} laps and VSC for {num_vsc_laps} laps",
        )


class PitstopNotAppliedError(BaseSimulationError):
    """Exception raised for when a pitstop is not applied"""

    def __init__(
        self,
        lap_number: float,
    ):
        self.lap_number = lap_number
        super().__init__(
            simulator_at_fault=True,
            message=f"Pitstop not applied on lap {lap_number}",
        )


class InvalidActionType(Enum):
    """Enum for the different types of invalid actions"""

    AT_LEAST_TWO_TYRE_COMPOUNDS = 1
    PIT_SOFT_NOT_AVAILABLE = 2
    PIT_MEDIUM_NOT_AVAILABLE = 3
    PIT_HARD_NOT_AVAILABLE = 4
    NO_TYRES_REMAINING = 5

    def __str__(self):
        return self.name.replace("_", " ")


class InvalidActionError(BaseSimulationError):
    """Exception raised for when the action selected is invalid"""

    def __init__(
        self,
        action: BaseRaceStrategy,
        type: InvalidActionType,
    ):
        self.action = action
        self.type = type

        message = {
            InvalidActionType.AT_LEAST_TWO_TYRE_COMPOUNDS: "At least two tyre compounds must be used",
            InvalidActionType.PIT_SOFT_NOT_AVAILABLE: "Soft tyres are not available for a pitstop",
            InvalidActionType.PIT_MEDIUM_NOT_AVAILABLE: "Medium tyres are not available for a pitstop",
            InvalidActionType.PIT_HARD_NOT_AVAILABLE: "Hard tyres are not available for a pitstop",
            InvalidActionType.NO_TYRES_REMAINING: "No tyres remaining",
        }

        super().__init__(
            simulator_at_fault=False,
            message=f"Invalid action: {message[type]}",
        )


class LapAlreadyCompleteError(BaseSimulationError):
    """Exception raised for when the lap is already complete"""

    def __init__(
        self,
        lap_number: float,
    ):
        self.lap_number = lap_number
        super().__init__(
            simulator_at_fault=True,
            message=f"Lap {lap_number} is already complete",
        )


class StopLapOutsideRangeError(BaseSimulationError):
    """Exception raised for when the stop lap is outside the range of laps"""

    def __init__(
        self,
        stop_lap: float,
    ):
        self.stop_lap = stop_lap
        super().__init__(
            simulator_at_fault=True,
            message=f"Stop lap {stop_lap} is outside the range of laps",
        )

class UnknownError(BaseSimulationError):
    """Exception raised for when the error is unknown"""

    def __init__(
        self,
        message: str,
    ):
        super().__init__(
            simulator_at_fault=True,
            message=message,
        )