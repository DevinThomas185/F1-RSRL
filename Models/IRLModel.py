import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch import nn

from Classes.Enums import Track
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.UnifiedRaceStrategy import UnifiedRaceStrategy
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.ConsoleLogger import ConsoleLogger

from Models.StrategyRLModel import StrategyRLModel
from Models.MercedesLinearModel import MercedesLinearModel

from confidential.MercedesRSTranslator import MercedesRSTranslator

from RewardFunctions.RewardFunctions import basic_reward, FAILURE_PENALTY


class IRLModel(StrategyRLModel):
    __slots__ = [
        "__policy_network",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str = "IRLModel",
        policy_network: nn.Module | None = None,
        logger: ConsoleLogger = ConsoleLogger(),
    ) -> None:
        super().__init__(selected_driver, name, logger)
        self.__policy_network = policy_network

    def train(
        self,
        num_episodes: int,
        seed: int = 0,
        fixed_seed: bool = False,
        simulation_step_size: float = 1.0,
        train_partial_simulations: bool = False,
        disable_safety_car: bool = False,
        allowed_years: list[str] = [],
        allowed_tracks: list[Track] = [],
        verbose: bool = False,
        learning_rate: float = 0.001,
        weight_decay: float = 0.0,
        optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
    ) -> None:
        """Train the IRL model

        Args:
            num_episodes (int): The number of simulations to train the model
            seed (int, optional): The RNG seed. Defaults to 0.
            fixed_seed (bool, optional): A fixed seed will cause each episode to be the exact same simulation. Defaults to False.
            simulation_step_size (float, optional): How much to step through a race each step. Defaults to 1.0.
            train_partial_simulations (bool, optional): Whether or not to train on partial simulations. Defaults to False.
            disable_safety_car (bool, optional): Whether or not to disable the safety car. Defaults to False.
            allowed_years (list[str], optional): The years to train the model on. Defaults to [].
            allowed_tracks (list[Track], optional): The tracks to train the model on. Defaults to [].
            reward_function (callable, optional): The reward function to use. Defaults to basic_reward.
            verbose (bool, optional): Whether or not to print outputs. Defaults to False.
            learning_rate (float, optional): The learning rate. Defaults to 0.001.
            weight_decay (float, optional): The weight decay. Defaults to 0.0.
            optimiser_type (torch.optim.Optimizer, optional): The optimiser to use. Defaults to torch.optim.Adam.
        """
        np.random.seed(seed)

        self.train_imitation_learning(
            num_episodes=num_episodes,
            seed=seed,
            fixed_seed=fixed_seed,
            simulation_step_size=simulation_step_size,
            train_partial_simulations=train_partial_simulations,
            disable_safety_car=disable_safety_car,
            allowed_years=allowed_years,
            allowed_tracks=allowed_tracks,
            verbose=verbose,
            learning_rate=learning_rate,
            weight_decay=weight_decay,
            optimiser_type=optimiser_type,
        )

    def train_imitation_learning(
        self,
        num_episodes: int,
        seed: int = 0,
        fixed_seed: bool = False,
        simulation_step_size: float = 1.0,
        train_partial_simulations: bool = False,
        disable_safety_car: bool = False,
        allowed_years: list[str] = [],
        allowed_tracks: list[Track] = [],
        verbose: bool = False,
        learning_rate: float = 0.001,
        weight_decay: float = 0.0,
        optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
    ) -> None:

        optimiser = optimiser_type(
            self.__policy_network.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )

        loss = nn.CrossEntropyLoss()

        data = pd.read_csv("Datasets/expert_dataset.csv")

        # Split the data into training and test sets
        train_data, test_data = train_test_split(data, test_size=0.2, shuffle=True)

        for episode in range(10_000):
            # Get the state and action from the training data
            state = torch.tensor(train_data.iloc[:, :-4].values, dtype=torch.float32)
            action = torch.tensor(train_data.iloc[:, -4:].values, dtype=torch.float32)

            output = self.__policy_network(state)

            loss_value = loss(output, action.argmax(dim=1))

            optimiser.zero_grad()
            loss_value.backward()
            optimiser.step()

            if episode % 10 == 0:
                test_state = torch.tensor(
                    test_data.iloc[:, :-4].values, dtype=torch.float32
                )
                test_action = torch.tensor(
                    test_data.iloc[:, -4:].values, dtype=torch.float32
                )

                test_output = self.__policy_network(test_state)
                test_loss_value = loss(test_output, test_action.argmax(dim=1))

                print(f"Test Loss: {test_loss_value.item()}")

            if verbose:
                print(f"Episode: {episode}, Loss: {loss_value.item()}")

        ########################################################################
        # Testing the trained model
        ########################################################################
        partial_steps = np.random.rand(num_episodes)

        for i_episode in range(5):
            losses = []

            if verbose:
                print(f"Episode {i_episode + 1}/{num_episodes}")

            sim = MercedesRSTranslator(
                selected_driver=self.selected_driver,
                seed=np.random.randint(0, 1_000_000),
                allowed_years=allowed_years,
                allowed_tracks=allowed_tracks,
                disable_safety_car=disable_safety_car,
                verbose=verbose,
                logger=self._logger,
            )

            track_details = sim.initialise_random_simulation()

            partial_step = partial_steps[i_episode] * track_details.TotalLaps

            state = sim.step(
                step=(
                    partial_step if train_partial_simulations else simulation_step_size
                ),
            )

            state_tensor = state.to_tensor()
            self._logger.log(f"                      {state}")

            while not state.terminal:
                agent_action_tensor = self.__policy_network(state_tensor)
                agent_action = SimpleRaceStrategy(
                    torch.argmax(agent_action_tensor).item()
                )

                next_state = sim.step(step=simulation_step_size)

                expert_action = MercedesLinearModel.infer_simple_race_strategy(
                    state=state,
                    next_state=next_state,
                )
                expert_action_tensor = expert_action.to_tensor()

                # FIXME: REMOVE ONCE FIXED (Sometimes the simulations get stuck)
                if next_state.race_progress == state.race_progress:
                    if verbose:
                        self._logger.log("SIMULATION STUCK", title="FAILURE")
                    break

                l = loss(agent_action_tensor, expert_action_tensor)
                losses.append(l.item())

                if verbose:
                    self._logger.log(
                        f"{agent_action:<10} {expert_action:<10} {next_state}"
                    )

                state = next_state
                state_tensor = next_state.to_tensor()

    def explain_feature_importance(
        self,
        state: UnifiedRaceState,
        show_plot: bool = False,
    ) -> dict:
        pass

    def predict(
        self,
        state: UnifiedRaceState,
    ) -> UnifiedRaceStrategy:
        """Predict the best strategy for the given race state

        Args:
            state (UnifiedRaceState): The race state

        Returns:
            UnifiedRaceStrategy: The predicted strategy
        """
        with torch.no_grad():
            output = self.__policy_network(state.to_tensor())
            return SimpleRaceStrategy(output.argmax().item())

    def predict_q_values(
        self,
        state: UnifiedRaceState,
    ) -> np.ndarray:
        """Predict the Q-values for the given race state

        Args:
            state (UnifiedRaceState): The race state

        Returns:
            np.ndarray: The Q-values
        """
        raise NotImplementedError

    def save_model(
        self,
        file_name: str = "Saved Models/irl_model",
    ) -> None:
        super()._save_model(
            model_type=IRLModel,
            checkpoints={
                "policy_network": self.__policy_network,
            },
            file_name=file_name,
        )

    @staticmethod
    def load_model(
        file_name: str,
    ) -> "IRLModel":
        checkpoint = torch.load(f"{file_name}")
        model = IRLModel(
            selected_driver=checkpoint["selected_driver"],
            name=checkpoint["name"],
            policy_network=checkpoint["policy_network"],
        )
        return model
