from datetime import datetime
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import torch
from torch import nn
import matplotlib.pyplot as plt
from copy import deepcopy
from termcolor import colored

from Classes.Enums import Track
from Classes.Errors import BaseSimulationError
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.UnifiedRaceStrategy import UnifiedRaceStrategy
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.RaceStrategy.BlankRaceStrategy import BlankRaceStrategy
from Classes.ConsoleLogger import ConsoleLogger
from Architectures.ActorCritic import Actor, Critic

from Models.StrategyRLModel import StrategyRLModel
from Models.ReplayBuffer import ReplayBuffer
import Models.model_utilities as utils

from confidential.MercedesRSTranslator import MercedesRSTranslator

from RewardFunctions.RewardFunctions import basic_reward, FAILURE_PENALTY


class DDPGModel(StrategyRLModel):
    __slots__ = [
        "__actor_network",
        "__actor_target_network",
        "__critic_network",
        "__critic_target_network",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str = "DDPGModel",
        device: str = "cpu",
        decision_tree: DecisionTreeClassifier | None = None,
        actor_network: nn.Module | None = None,
        critic_network: nn.Module | None = None,
        logger: ConsoleLogger = ConsoleLogger(),
        number_of_episodes_trained: int = 0,
        disable_safety_car: bool = False,
        allowed_years: list[str] = [],
        allowed_tracks: list[Track] = [],
        reward_function: callable = basic_reward,
    ) -> None:
        super().__init__(
            selected_driver=selected_driver,
            name=name,
            device=device,
            decision_tree=decision_tree,
            logger=logger,
            number_of_episodes_trained=number_of_episodes_trained,
            is_recurrent=False,
            disable_safety_car=disable_safety_car,
            allowed_years=allowed_years,
            allowed_tracks=allowed_tracks,
            reward_function=reward_function,
        )

        if actor_network is None:
            self.__actor_network = Actor(
                UnifiedRaceState.size(), len(SimpleRaceStrategy)
            ).to(self._device)
        else:
            self.__actor_network = actor_network.to(self._device)
        self.__actor_target_network = deepcopy(actor_network)
        self.__actor_target_network.to(self._device)

        if critic_network is None:
            self.__critic_network = Critic(
                UnifiedRaceState.size(), len(SimpleRaceStrategy)
            ).to(self._device)
        else:
            self.__critic_network = critic_network.to(self._device)
        self.__critic_target_network = deepcopy(critic_network)
        self.__critic_target_network.to(self._device)

    ############################################################################
    # Training Methods
    ############################################################################
    def train(
        self,
        num_episodes: int,
        seed: int = 0,
        fixed_seed: bool = False,
        simulation_step_size: float = 1.0,
        filter_invalid_actions: bool = False,
        checkpointing_details: dict[str, any] | None = None,
        verbose: bool = False,
        epsilon: float = 1.0,
        epsilon_decay: float = 0.99,
        min_epsilon: float = 0.1,
        gamma: float = 0.99,
        tau: float = 0.01,
        actor_learning_rate: float = 0.001,
        critic_learning_rate: float = 0.001,
        actor_weight_decay: float = 0.0,
        critic_weight_decay: float = 0.0,
        replay_buffer_size: int = 10_000,
        replay_buffer_sample_size: int = 32,
        actor_optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
        critic_optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
        add_loss_noise: bool = False,
        generate_plots: bool = False,
    ) -> None:
        """Train the DDPG model

        Args:
            num_episodes (int): The number of simulations to train the model
            seed (int, optional): The RNG seed. Defaults to 0.
            fixed_seed (bool, optional): A fixed seed will cause each episode to be the exact same simulation. Defaults to False.
            simulation_step_size (float, optional): How much to step through a race each step. Defaults to 1.0.
            verbose (bool, optional): Whether or not to print outputs. Defaults to False.
            epsilon (float, optional): The epsilon value for the epsilon greedy policy. Defaults to 1.0.
            epsilon_decay (float, optional): The decay rate for epsilon. Defaults to 0.99.
            min_epsilon (float, optional): The minimum value for epsilon. Defaults to 0.1.
            gamma (float, optional): The discount factor. Defaults to 0.99.
            tau (float, optional): The soft update factor. Defaults to 0.001.
            actor_learning_rate (float, optional): The learning rate for the actor network. Defaults to 0.001.
            critic_learning_rate (float, optional): The learning rate for the critic network. Defaults to 0.001.
            actor_weight_decay (float, optional): The weight decay for the actor network. Defaults to 0.0.
            critic_weight_decay (float, optional): The weight decay for the critic network. Defaults to 0.0.
            replay_buffer_size (int, optional): The size of the replay buffer. Defaults to 10_000.
            replay_buffer_sample_size (int, optional): The size of the replay buffer sample. Defaults to 32.
            actor_optimiser_type (torch.optim.Optimizer, optional): The optimiser for the actor network. Defaults to torch.optim.Adam.
            critic_optimiser_type (torch.optim.Optimizer, optional): The optimiser for the critic network. Defaults to torch.optim.Adam.
            add_loss_noise (bool, optional): Whether or not to add noise to the states in loss calculations. Defaults to False.
            generate_plots (bool, optional): Whether or not to generate plots. Defaults to False.
        """
        np.random.seed(seed)

        # Move the models to the GPU if available
        self.__actor_network.to(self._device)
        self.__actor_target_network.to(self._device)
        self.__critic_network.to(self._device)
        self.__critic_target_network.to(self._device)

        # Setup checkpointing
        self._setup_checkpointing(checkpointing_details)
        self._save_training_parameters(locals())

        # Model Setup
        actor_optimiser = actor_optimiser_type(
            self.__actor_network.parameters(),
            lr=actor_learning_rate,
            weight_decay=actor_weight_decay,
        )

        critic_optimiser = critic_optimiser_type(
            self.__critic_network.parameters(),
            lr=critic_learning_rate,
            weight_decay=critic_weight_decay,
        )

        # Duplicate the model for the target networks
        utils.hard_update(self.__actor_network, self.__actor_target_network)
        utils.hard_update(self.__critic_network, self.__critic_target_network)

        replay_buffer = ReplayBuffer(replay_buffer_size)

        total_rewards = []
        actor_total_losses = []
        critic_total_losses = []

        for i_episode in range(num_episodes):
            episode_transitions = []

            self._logger.log(
                message=f"{self.name} | Episode {i_episode+1} of {num_episodes} | Epsilon {epsilon:.2f}",
                verbose=verbose,
            )

            total_reward = 0
            actor_loss_and_steps = (0, 0)
            critic_loss_and_steps = (0, 0)

            sim = MercedesRSTranslator(
                selected_driver=self.selected_driver,
                seed=seed if fixed_seed else np.random.randint(0, 1_000_000),
                allowed_years=self._allowed_years,
                allowed_tracks=self._allowed_tracks,
                disable_safety_car=self._disable_safety_car,
                verbose=verbose,
                logger=self._logger,
            )

            track_details, state = sim.initialise_random_simulation()
            state_tensor = state.to_tensor().to(self._device)

            self._logger.log(
                message=f"                    {state}",
                verbose=verbose,
            )

            while not state.terminal:
                action, greedy_action = utils.simple_strategy_epsilon_greedy(
                    epsilon=epsilon,
                    policy=self.__actor_network,
                    state=state,
                    state_tensor=state_tensor,
                    filter_invalid_actions=filter_invalid_actions,
                    device=self._device,
                )

                try:
                    exception = None
                    next_state = sim.step(
                        step=simulation_step_size,
                        strategy=action,
                    )

                except BaseSimulationError as e:
                    exception = e
                    next_state = state
                    next_state.terminal = True

                reward = self._reward_function(state, action, next_state)
                total_reward += reward + gamma * total_reward

                colour = "green" if action == greedy_action else "red"
                self._logger.log(
                    message=f"{colored(f'{action:<10}', colour)} {reward:<8.2f} {next_state}",
                    verbose=verbose,
                )

                # Log the exception (we do this so that we print the final state and action, and then log the failure)
                if exception is not None:
                    self._handle_simulation_error(exception, verbose)

                action_tensor = torch.nn.functional.one_hot(
                    torch.tensor(action.value),
                    num_classes=len(SimpleRaceStrategy),
                ).to(self._device)
                reward_tensor = torch.tensor([reward]).to(self._device)
                next_state_tensor = next_state.to_tensor().to(self._device)
                done_tensor = torch.tensor([next_state.terminal]).to(self._device)

                replay_buffer.push(
                    [
                        state_tensor,
                        action_tensor,
                        next_state_tensor,
                        reward_tensor,
                        done_tensor,
                    ]
                )

                state = next_state
                state_tensor = next_state_tensor

                # Perform one step of optimisation on actor and critic networks
                if len(replay_buffer) >= replay_buffer_sample_size:
                    transitions = replay_buffer.sample(replay_buffer_sample_size)
                    state_batch, action_batch, next_state_batch, reward_batch, dones = (
                        torch.stack(x).to(self._device) for x in zip(*transitions)
                    )

                    # Compute loss
                    critic_loss = self.__critic_loss(
                        states=state_batch,
                        actions=action_batch,
                        rewards=reward_batch,
                        next_states=next_state_batch,
                        dones=dones,
                        gamma=gamma,
                        add_noise=add_loss_noise,
                    )
                    cl, cs = critic_loss_and_steps
                    critic_loss_and_steps = (cl + critic_loss.item(), cs + 1)

                    critic_optimiser.zero_grad()
                    critic_loss.backward()
                    critic_optimiser.step()

                    actor_loss = self.__actor_loss(state_batch, add_loss_noise)
                    al, as_ = actor_loss_and_steps
                    actor_loss_and_steps = (al + actor_loss.item(), as_ + 1)

                    actor_optimiser.zero_grad()
                    actor_loss.backward()
                    actor_optimiser.step()

            # Some errors cause the episode to be unusable, if so, we do not add
            # it to the replay buffer, so that the model does not learn from it.
            # We continue and try another episode.
            if exception is not None and exception.simulator_at_fault:
                self._logger.log(
                    message="\n\n",
                    verbose=verbose,
                )
                continue
            else:
                replay_buffer.push_list(episode_transitions)

            # Update the target networks
            utils.soft_update(
                source_network=self.__actor_network,
                target_network=self.__actor_target_network,
                tau=tau,
            )
            utils.soft_update(
                source_network=self.__critic_network,
                target_network=self.__critic_target_network,
                tau=tau,
            )

            # Decay exploration paramater, epsilon
            epsilon = max(epsilon * epsilon_decay, min_epsilon)

            # Append the total reward
            total_rewards.append(total_reward)

            # Append the total losses
            actor_total_losses.append(
                actor_loss_and_steps[0] / actor_loss_and_steps[1]
                if actor_loss_and_steps[1] > 0
                else 0
            )
            critic_total_losses.append(
                critic_loss_and_steps[0] / critic_loss_and_steps[1]
                if critic_loss_and_steps[1] > 0
                else 0
            )

            # Log final outputs for this simulation
            self._logger.log(
                message=sim.get_pitstops(self.selected_driver),
                title="PITSTOPS",
                verbose=verbose,
            )
            self._logger.log(
                message=f"{total_reward}\n\n",
                title="FINISH",
                verbose=verbose,
            )

            # Checkpoint the model # TODO: Save both optimisers
            self._save_checkpoint(i_episode, actor_optimiser)

        if generate_plots:
            self._plot_total_rewards(total_rewards)
            self._plot_losses(actor_total_losses)
            self._plot_losses(critic_total_losses)

    def __actor_loss(
        self,
        states: torch.Tensor,
        add_noise: bool = True,
    ) -> torch.Tensor:
        if add_noise:
            states = utils.add_gaussian_noise(states)

        actions = self.__actor_network(states, self._device)
        critic_values = self.__critic_network(states, actions, self._device)
        return -critic_values.mean()

    def __critic_loss(
        self,
        states: torch.Tensor,
        actions: torch.Tensor,
        rewards: torch.Tensor,
        next_states: torch.Tensor,
        dones: torch.Tensor,
        gamma: float,
        add_noise: bool = True,
    ) -> torch.Tensor:
        if add_noise:
            states = utils.add_gaussian_noise(states)
            next_states = utils.add_gaussian_noise(next_states)

        next_actions = self.__actor_target_network(next_states, self._device)
        next_q_values = self.__critic_target_network(
            next_states, next_actions, self._device
        )
        target_q_values = rewards + (gamma * next_q_values * ~(dones))
        predicted_q_values = self.__critic_network(states, actions, self._device)
        return nn.functional.mse_loss(predicted_q_values, target_q_values)

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
    ) -> UnifiedRaceStrategy:
        """Predict the best strategy for the given race state

        Args:
            state (UnifiedRaceState): The race state

        Returns:
            UnifiedRaceStrategy: The predicted strategy
        """
        _, greedy_action = utils.simple_strategy_epsilon_greedy(
            epsilon=0.0,
            policy=self.__actor_network,
            state=state,
            device="cuda" if torch.cuda.is_available() else "cpu",
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
            np.ndarray: The Q-values
        """
        raise NotImplementedError

    ############################################################################
    # Model Saving and Loading
    ############################################################################
    def save_model(
        self,
        file_name: str = "Saved Models/ddpg_model",
    ) -> None:
        super()._save_model(
            model_type=DDPGModel,
            checkpoints={
                "actor_network": self.__actor_network,
                "critic_network": self.__critic_network,
            },
            file_name=file_name,
        )

    @staticmethod
    def load_model(
        file_name: str,
    ) -> "DDPGModel":
        checkpoint = torch.load(f"{file_name}")
        model = DDPGModel(
            selected_driver=checkpoint.get("selected_driver", 44),
            name=checkpoint.get("name", "DDPGModel"),
            device=checkpoint.get("device", "cpu"),
            decision_tree=checkpoint.get("decision_tree", None),
            number_of_episodes_trained=checkpoint.get("number_of_episodes_trained", 0),
            disable_safety_car=checkpoint.get("disable_safety_car", False),
            allowed_years=checkpoint.get("allowed_years", []),
            allowed_tracks=checkpoint.get("allowed_tracks", []),
            reward_function=checkpoint.get("reward_function", basic_reward),
            actor_network=checkpoint["actor_network"],
            critic_network=checkpoint["critic_network"],
        )
        return model
