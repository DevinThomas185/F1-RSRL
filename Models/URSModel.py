import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.nn.functional import mse_loss

from confidential.MercedesRSTranslator import MercedesRSTranslator

from Classes.ConsoleLogger import ConsoleLogger
from Classes.Enums import Track
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.UnifiedRaceStrategy import UnifiedRaceStrategy
from Classes.RaceStrategy.Pitstop import Pitstop

from Models.StrategyRLModel import StrategyRLModel
from Architectures.URSModelNetwork import (
    NoStopNetwork,
    OneStopNetwork,
    TwoStopNetwork,
    ThreeStopNetwork,
)


class URSModel(StrategyRLModel):
    __slots__ = [
        "__no_stop_network",
        "__one_stop_network",
        "__two_stop_network",
        "__three_stop_network",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str = "URS Model",
        logger: ConsoleLogger = ConsoleLogger(),
    ) -> None:
        super().__init__(selected_driver, name, logger)
        self.__no_stop_network = NoStopNetwork()
        self.__one_stop_network = OneStopNetwork()
        self.__two_stop_network = TwoStopNetwork()
        self.__three_stop_network = ThreeStopNetwork()

    ############################################################################
    # Training Methods
    ############################################################################
    def train(
        self,
        num_episodes: int,
        seed: int = 0,
        disable_safety_car: bool = False,
        allowed_years: list[str] = [],
        allowed_tracks: list[Track] = [],
        verbose: bool = False,
        learning_rate: float = 0.001,
        weight_decay: float = 0.0,
        optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
    ) -> None:
        # TODO: Set up 4 threads for training each network
        self.train_no_stop(
            num_episodes=num_episodes,
            seed=seed,
            disable_safety_car=disable_safety_car,
            allowed_years=allowed_years,
            allowed_tracks=allowed_tracks,
            verbose=verbose,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            optimiser_type=optimiser_type,
        )

    def train_no_stop(
        self,
        num_episodes: int,
        seed: int = 0,
        disable_safety_car: bool = False,
        allowed_years: list[str] = [],
        allowed_tracks: list[Track] = [],
        verbose: bool = False,
        learning_rate: float = 0.001,
        weight_decay: float = 0.0,
        optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
    ) -> None:
        np.random.seed(seed)

        # Set up optimiser
        optimiser = optimiser_type(
            self.__no_stop_network.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )

        percents_to_simulate_to = np.random.random(num_episodes)

        losses = []

        # For each episode
        for i_episode in range(num_episodes):
            self._logger.log(
                message=f"{self.name} | Episode {i_episode+1} of {num_episodes}",
                verbose=verbose,
            )

            # Set up simulation
            sim = MercedesRSTranslator(
                selected_driver=self.selected_driver,
                seed=seed,
                allowed_years=allowed_years,
                allowed_tracks=allowed_tracks,
                disable_safety_car=disable_safety_car,
                verbose=verbose,
                logger=self._logger,
            )
            track_details, state_0 = sim.initialise_random_simulation()

            # Pick a random lap to simulate lap by lap to
            lap_to_simulate_to = int(
                percents_to_simulate_to[i_episode] * track_details.TotalLaps
            )

            # If the random lap is the last lap, simulate to the second last lap
            if lap_to_simulate_to == 0:
                lap_to_simulate_to = 1
            if lap_to_simulate_to >= track_details.TotalLaps - 2:
                lap_to_simulate_to -= 3

            # race_states = [state_0]
            # race_states.append([sim.step(1) for _ in range(lap_to_simulate_to)])
            race_states = [state_0, sim.step(lap_to_simulate_to)]

            # Predict the final GL # TODO: MAKE NETWORKS RECURRENT (LSTM)
            _, predicted_gl = self.__no_stop_network(race_states[-1].to_tensor())

            # Run the strategy to the end of the race
            sim.step(100)
            actual_gl = torch.tensor(
                [sim.get_final_gap_to_leader(self.selected_driver)]
            )

            # Calculate the loss
            loss = mse_loss(predicted_gl, actual_gl)
            losses.append(loss.detach().numpy())

            print(predicted_gl, actual_gl, loss)

            # Backpropagate the loss
            optimiser.zero_grad()
            loss.backward()
            optimiser.step()

        plt.plot(losses)
        plt.xlabel("Episode")
        plt.ylabel("Total Losses")
        plt.title("URSModel - Total Losses over Episodes")
        plt.show()

    ############################################################################
    # Explainability Functions
    ############################################################################
    def explain_feature_importance(
        self,
        state: UnifiedRaceState,
        show_plot: bool = False,
    ) -> dict:
        pass

    ############################################################################
    # Prediction Functions
    ############################################################################
    def predict(
        self,
        state: UnifiedRaceState,
    ) -> None:
        state_tensor = state.to_tensor()

        _, no_stop_gl = self.__no_stop_network(state_tensor)
        _, one_stop_gl, pl1, tc1 = self.__one_stop_network(state_tensor)
        _, two_stop_gl, pl1, tc1, pl2, tc2 = self.__two_stop_network(state_tensor)
        _, three_stop_gl, pl1, tc1, pl2, tc2, pl3, tc3 = self.__three_stop_network(
            state_tensor
        )

        strategy = UnifiedRaceStrategy()
        if (
            one_stop_gl < no_stop_gl
            and one_stop_gl < two_stop_gl
            and one_stop_gl < three_stop_gl
        ):
            strategy.add_pitstop(
                Pitstop(tyre_compound=tc1, percentage_through_race=pl1)
            )
        if (
            two_stop_gl < no_stop_gl
            and two_stop_gl < one_stop_gl
            and two_stop_gl < three_stop_gl
        ):
            strategy.add_pitstop(
                Pitstop(tyre_compound=tc1, percentage_through_race=pl1)
            )
            strategy.add_pitstop(
                Pitstop(tyre_compound=tc2, percentage_through_race=pl2)
            )
        if (
            three_stop_gl < no_stop_gl
            and three_stop_gl < one_stop_gl
            and three_stop_gl < two_stop_gl
        ):
            strategy.add_pitstop(
                Pitstop(tyre_compound=tc1, percentage_through_race=pl1)
            )
            strategy.add_pitstop(
                Pitstop(tyre_compound=tc2, percentage_through_race=pl2)
            )
            strategy.add_pitstop(
                Pitstop(tyre_compound=tc3, percentage_through_race=pl3)
            )
        return strategy

    ############################################################################
    # Model Saving and Loading
    ############################################################################
    def save_model(
        self,
        file_name: str = "Saved Models/urs_model",
    ) -> None:
        pass

    @staticmethod
    def load_model(
        file_name: str,
    ) -> "URSModel":
        pass
