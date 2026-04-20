import numpy as np
import torch
from torch import nn
import matplotlib.pyplot as plt

from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.UnifiedRaceStrategy import UnifiedRaceStrategy
from Classes.ConsoleLogger import ConsoleLogger

from Classes.PracticeSimulation import PracticeSimulation

from Models.StrategyRLModel import StrategyRLModel
from Models.ReplayBuffer import ReplayBuffer
import Models.model_utilities as utils


class PracticeDQNModel(StrategyRLModel):
    __slots__ = [
        "__policy_network",
        "__target_network",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str = "DQNModel",
        policy_network: nn.Module | None = None,
        target_network: nn.Module | None = None,
        logger: ConsoleLogger = ConsoleLogger(),
    ) -> None:
        super().__init__(selected_driver, name, logger)

        self.__policy_network = policy_network
        self.__target_network = target_network

    ############################################################################
    # Training Methods
    ############################################################################
    def train(
        self,
        num_episodes: int,
        filter_invalid_actions: bool = True,
        verbose: bool = False,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.99,
        min_epsilon: float = 0.1,
        gamma: float = 0.99,
        tau: float = 1.0,
        learning_rate: float = 0.001,
        weight_decay: float = 0.0,
        replay_buffer_size: int = 10_000,
        replay_buffer_sample_size: int = 32,
        episodes_to_update_target: int = 10,
        optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
    ) -> None:
        """Train the DQN model

        Args:
            num_episodes (int): The number of simulations to train the model
            simulation_step_size (float, optional): How much to step through a race each step. Defaults to 1.0.
            train_partial_simulations (bool, optional): Whether or not to train on partial simulations. Defaults to False.
            disable_safety_car (bool, optional): Whether or not to disable the safety car. Defaults to False.
            allowed_years (list[str], optional): The years to train the model on. Defaults to [].
            allowed_tracks (list[Track], optional): The tracks to train the model on. Defaults to [].
            reward_function (callable, optional): The reward function to use. Defaults to basic_reward.
            verbose (bool, optional): Whether or not to print outputs. Defaults to False.
            epsilon (float, optional): Exploration parameter epsilon. Defaults to 1.0.
            epsilon_decay (float, optional): How much to anneal epsilon. Defaults to 0.99.
            min_epsilon (float, optional): Minimum level of exploration. Defaults to 0.1.
            gamma (float, optional): The discount factor. Defaults to 0.99.
            tau (float, optional): The soft update parameter. Defaults to 0.001.
            learning_rate (float, optional): The learning rate. Defaults to 0.001.
            weight_decay (float, optional): Weight decay of the optimiser. Defaults to 0.0.
            replay_buffer_size (int, optional): Size of the replay buffer. Defaults to 10_000.
            replay_buffer_sample_size (int, optional): Size of the batch to sample from the replay buffer. Defaults to 32.
            episodes_to_update_target (int, optional): How many episodes before updating the target policy network. Defaults to 10.
            optimiser_type (torch.optim.Optimizer, optional): The type of the optimiser. Defaults to torch.optim.Adam.
        """

        optimiser = optimiser_type(
            self.__policy_network.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )

        replay_buffer = ReplayBuffer(replay_buffer_size)

        total_rewards = []

        for i_episode in range(num_episodes):
            self._logger.log(f"{self.name} | Episode {i_episode+1} of {num_episodes}")

            total_reward = 0

            sim = PracticeSimulation()

            state = sim.step()

            state_tensor = state.to_tensor()
            if verbose:
                self._logger.log(f"                    {state}")

            while not state.terminal:
                action, _ = utils.simple_strategy_epsilon_greedy(
                    epsilon=epsilon,
                    policy=self.__policy_network,
                    state=state,
                    state_tensor=state_tensor,
                    filter_invalid_actions=filter_invalid_actions,
                )

                next_state = sim.step(strategy=action)

                reward = sim.get_reward()
                total_reward = reward + gamma * total_reward

                if verbose:
                    self._logger.log(f"{action:<10} {reward:<8.2f} {next_state}")

                next_state_tensor = next_state.to_tensor()
                reward_tensor = torch.tensor([reward])
                action_tensor = torch.tensor([action.value])
                done_tensor = torch.tensor([state.terminal])

                replay_buffer.push(
                    [
                        state_tensor,
                        action_tensor,
                        next_state_tensor,
                        reward_tensor,
                        done_tensor,
                    ]
                )

                if state.position == 7:
                    print(state.position, action, next_state.position)

                state = next_state
                state_tensor = next_state_tensor

                # Perform one step of the optimization (on the policy network)
                if len(replay_buffer) >= replay_buffer_sample_size:
                    transitions = replay_buffer.sample(replay_buffer_sample_size)
                    state_batch, action_batch, next_state_batch, reward_batch, dones = (
                        torch.stack(x) for x in zip(*transitions)
                    )

                    # Compute loss
                    loss = self.__loss(
                        states=state_batch,
                        actions=action_batch,
                        rewards=reward_batch,
                        next_states=next_state_batch,
                        dones=dones,
                        gamma=gamma,
                    )

                    optimiser.zero_grad()
                    loss.backward()
                    optimiser.step()

                epsilon = max(epsilon * epsilon_decay, min_epsilon)

            # Update the target network, copying all weights and biases in DQN
            if i_episode % episodes_to_update_target == 0:
                utils.soft_update(
                    source_network=self.__policy_network,
                    target_network=self.__target_network,
                    tau=tau,
                )

            with torch.no_grad():
                print(
                    torch.round(
                        self.__policy_network(
                            torch.tensor(
                                [
                                    [0.0],
                                    [1.0],
                                    [2.0],
                                    [3.0],
                                    [4.0],
                                    [5.0],
                                    [6.0],
                                    [7.0],
                                    [8.0],
                                ]
                            )
                        ),
                        decimals=2,
                    )
                )

            total_rewards.append(total_reward)
            if verbose:
                self._logger.log(f"{total_reward}\n\n", title="FINISH")

        plt.plot(total_rewards)
        plt.xlabel("Episode")
        plt.ylabel("Total Rewards")
        plt.title("DQNModel - Total Rewards over Episodes")
        plt.show()

    def __loss(
        self,
        states: torch.Tensor,
        actions: torch.Tensor,
        rewards: torch.Tensor,
        next_states: torch.Tensor,
        dones: torch.Tensor,
        gamma: float,
    ) -> torch.Tensor:
        q_values = self.__policy_network(states).gather(1, actions).reshape(-1)

        with torch.no_grad():
            next_q_values = self.__target_network(next_states).max(1).values

        expected_q_values = rewards.reshape(-1) + (
            gamma * next_q_values * ~(dones).reshape(-1)
        )

        return nn.functional.huber_loss(q_values, expected_q_values)

    ############################################################################
    # Explanation Methods
    ############################################################################
    def explain_feature_importance(
        self,
        state: UnifiedRaceState,
        show_plot: bool = False,
    ) -> dict:
        pass

    ############################################################################
    # Prediction Methods
    ############################################################################
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
        _, greedy_action = utils.simple_strategy_epsilon_greedy(
            epsilon=0.0,
            policy=self.__policy_network,
            state=state,
        )
        return greedy_action

    def predict_q_values(
        self,
        state: UnifiedRaceState,
    ) -> np.ndarray:
        """Predict the Q-values for the given race state

        Args:
            state (UnifiedRaceState): The race state

        Returns:
            np.ndarray: The predicted Q-values
        """
        raise NotImplementedError

    ############################################################################
    # Save/Load Methods
    ############################################################################
    def save_model(
        self,
        file_name: str = "Saved Models/practice_dqn_model",
    ) -> None:
        super()._save_model(
            model_type=PracticeDQNModel,
            checkpoints={
                "policy_network": self.__policy_network,
                "target_network": self.__target_network,
            },
            file_name=file_name,
        )

    @staticmethod
    def load_model(
        file_name: str,
    ) -> "PracticeDQNModel":
        checkpoint = torch.load(f"{file_name}")
        model = PracticeDQNModel(
            selected_driver=checkpoint["selected_driver"],
            name=checkpoint["name"],
            policy_network=checkpoint["policy_network"],
            target_network=checkpoint["target_network"],
        )
        return model
