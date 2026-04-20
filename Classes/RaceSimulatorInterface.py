from abc import ABCMeta, abstractmethod
from Classes.Enums import Track
from Classes.RaceState.generate_UnifiedRaceState import generate_UnifiedRaceState
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy
from Classes.RaceStrategy.BlankRaceStrategy import BlankRaceStrategy


class RaceSimulatorInterface(metaclass=ABCMeta):
    """Race Simulator Interface

    This interface is to be implemented by any simulator that the model needs to be
    trained on. It is used to abstract the model from the simulator so that the
    model can be trained on any simulator that implements this interface.

    Raises:
        NotImplementedError: generate_random_simulation() must be implemented by the inheriting class.
        NotImplementedError: step_simulation() must be implemented by the inheriting class.
    """

    @abstractmethod
    def initialise_random_simulation(
        self,
    ) -> None:
        """Generate a new random simulation to train with

        Raises:
            NotImplementedError: This method must be implemented by the inheriting class.
        """
        raise NotImplementedError

    @abstractmethod
    def step(
        self,
        step: float = 1,
        strategy: BaseRaceStrategy = BlankRaceStrategy(),
        verbose: bool = False,
    ) -> UnifiedRaceState:
        """Step the simulation forward by a given step size.

        Args:
            step (float, optional): The step size to take. Defaults to 1.
            strategy (BaseRaceStrategy, optional): The strategy(action) to take into the next simulation step. Defaults to BlankRaceStrategy().
            verbose (bool, optional): Whether to print the state, action and reward. Defaults to False.

        Raises:
            NotImplementedError: This method must be implemented by the inheriting class.

        Returns:
            UnifiedRaceState: The new race state after the step.
        """
        raise NotImplementedError

    @abstractmethod
    def get_track(
        self,
    ) -> Track:
        """Get the track that the simulation is running on.

        Raises:
            NotImplementedError: This method must be implemented by the inheriting class.

        Returns:
            Track: The track that the simulation is running on.
        """
        raise NotImplementedError

    @abstractmethod
    def get_finishing_position(
        self,
        driver: int,
    ) -> int:
        """Get the finishing position of the selected driver.

        Raises:
            NotImplementedError: This method must be implemented by the inheriting class.

        Returns:
            int: The finishing position of the selected driver.
        """
        raise NotImplementedError

    @abstractmethod
    def _translate_strategy(
        self,
        strategy: BaseRaceStrategy,
    ) -> any:
        """Translate the strategy into the simulator's format.

        Args:
            strategy (BaseRaceStrategy): The strategy to translate into the simulator's format.

        Raises:
            NotImplementedError: This method must be implemented by the inheriting class.

        Returns:
            any: The translated strategy.
        """
        raise NotImplementedError

    @abstractmethod
    def _translate_state(
        self,
        state: any,
    ) -> UnifiedRaceState:
        """Translate the state from the simulator's format into the UnifiedRaceState format.

        Args:
            state (any): The state to translate.

        Raises:
            NotImplementedError: This method must be implemented by the inheriting class.

        Returns:
            UnifiedRaceState: The translated state.
        """
        raise NotImplementedError
