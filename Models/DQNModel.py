import numpy as np
from sklearn.tree import DecisionTreeClassifier
from termcolor import colored
import torch
from torch import nn

from Architectures.QNetwork import QNetwork
from Classes.Enums import Track
from Classes.Errors import BaseSimulationError
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.RaceStrategy.UnifiedRaceStrategy import UnifiedRaceStrategy
from Classes.ConsoleLogger import ConsoleLogger

from Models.StrategyRLModel import StrategyRLModel
from Models.ReplayBuffer import ReplayBuffer
import Models.model_utilities as utils

from confidential.MercedesRSTranslator import MercedesRSTranslator

from RewardFunctions.RewardFunctions import basic_reward


class DQNModel(StrategyRLModel):
    __slots__ = [
        "__policy_network",
        "__target_network",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str = "DQNModel",
        device: str = "cpu",
        policy_network: nn.Module | None = None,
        target_network: nn.Module | None = None,
        decision_tree: DecisionTreeClassifier | None = None,
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

        if policy_network is None:
            self.__policy_network = QNetwork(
                UnifiedRaceState.size(), len(SimpleRaceStrategy)
            ).to(self._device)
        else:
            self.__policy_network = policy_network.to(device)

        if target_network is None:
            self.__target_network = QNetwork(
                UnifiedRaceState.size(), len(SimpleRaceStrategy)
            ).to(self._device)
        else:
            self.__target_network = target_network.to(device)

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
        learning_rate: float = 0.001,
        weight_decay: float = 0.0,
        replay_buffer_size: int = 10_000,
        replay_buffer_sample_size: int = 32,
        episodes_to_update_target: int = 10,
        optimiser_type: torch.optim.Optimizer = torch.optim.Adam,
        add_loss_noise: bool = False,
        generate_plots: bool = False,
    ) -> None:
        """Train the DQN model

        Args:
            num_episodes (int): The number of simulations to train the model
            seed (int, optional): The RNG seed. Defaults to 0.
            fixed_seed (bool, optional): A fixed seed will cause each episode to be the exact same simulation. Defaults to False.
            simulation_step_size (float, optional): How much to step through a race each step. Defaults to 1.0.
            filter_invalid_actions (bool, optional): Whether or not to filter out invalid actions. Defaults to False.
            checkpointing_details (dict[str, any], optional): Checkpointing parameters. Defaults to None.
            verbose (bool, optional): Whether or not to print outputs. Defaults to False.
            epsilon (float, optional): Exploration parameter epsilon. Defaults to 1.0.
            epsilon_decay (float, optional): How much to anneal epsilon. Defaults to 0.99.
            min_epsilon (float, optional): Minimum level of exploration. Defaults to 0.1.
            gamma (float, optional): The discount factor. Defaults to 0.99.
            learning_rate (float, optional): The learning rate. Defaults to 0.001.
            weight_decay (float, optional): Weight decay of the optimiser. Defaults to 0.0.
            replay_buffer_size (int, optional): Size of the replay buffer. Defaults to 10_000.
            replay_buffer_sample_size (int, optional): Size of the batch to sample from the replay buffer. Defaults to 32.
            episodes_to_update_target (int, optional): How many episodes before updating the target policy network. Defaults to 10.
            optimiser_type (torch.optim.Optimizer, optional): The type of the optimiser. Defaults to torch.optim.Adam.
            add_loss_noise (bool, optional): Whether or not to add noise to the states in loss calculations. Defaults to False.
            generate_plots (bool, optional): Whether or not to generate plots. Defaults to False.
        """
        np.random.seed(seed)

        # Move the model to the GPU if available
        self.__policy_network.to(self._device)
        self.__target_network.to(self._device)

        # Setup checkpointing
        self._setup_checkpointing(checkpointing_details)
        self._save_training_parameters(locals())

        # Model Setup
        optimiser = optimiser_type(
            self.__policy_network.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )
        if self._number_of_episodes_trained > 0:
            self.load_optimiser_state(optimiser)

        # Duplicate the policy network to create the target network
        utils.hard_update(self.__policy_network, self.__target_network)
        self.__target_network.eval()

        replay_buffer = ReplayBuffer(replay_buffer_size)

        total_rewards = []
        total_losses = []

        i_episode = 1 + self._number_of_episodes_trained
        end_episode = num_episodes + self._number_of_episodes_trained

        # Training Loop
        while i_episode <= end_episode:
            episode_transitions = []

            self._logger.log(
                message=f"{self.name} | Episode {i_episode} of {num_episodes} | Epsilon {epsilon:.2f}",
                verbose=verbose,
            )

            total_reward = 0
            loss_and_steps = (0, 0)

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
                    policy=self.__policy_network,
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
                total_reward = reward + gamma * total_reward

                colour = "green" if action == greedy_action else "red"
                self._logger.log(
                    message=f"{colored(f'{action:<10}', colour)} {reward:<8.2f} {next_state}",
                    verbose=verbose,
                )

                # Log the exception (we do this so that we print the final state and action, and then log the failure)
                if exception is not None:
                    self._handle_simulation_error(exception, verbose)

                action_tensor = torch.tensor([action.value]).to(self._device)
                reward_tensor = torch.tensor([reward]).to(self._device)
                next_state_tensor = next_state.to_tensor().to(self._device)
                done_tensor = torch.tensor([next_state.terminal]).to(self._device)

                episode_transitions.append(
                    [
                        state_tensor,
                        action_tensor,
                        reward_tensor,
                        next_state_tensor,
                        done_tensor,
                    ]
                )

                state = next_state
                state_tensor = next_state_tensor

                # Perform one step of the optimisation (on the policy network)
                if len(replay_buffer) >= replay_buffer_sample_size:
                    transitions = replay_buffer.sample(replay_buffer_sample_size)
                    (
                        state_batch,
                        action_batch,
                        reward_batch,
                        next_state_batch,
                        dones_batch,
                    ) = (torch.stack(x).to(self._device) for x in zip(*transitions))

                    # Compute loss
                    loss = self.__loss(
                        states=state_batch,
                        actions=action_batch,
                        rewards=reward_batch,
                        next_states=next_state_batch,
                        dones=dones_batch,
                        gamma=gamma,
                        add_noise=add_loss_noise,
                    )

                    l, s = loss_and_steps
                    loss_and_steps = (l + loss.item(), s + 1)

                    optimiser.zero_grad()
                    loss.backward()
                    optimiser.step()

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

            # Update the target network, copying all weights and biases in DQN
            if i_episode % episodes_to_update_target == 0:
                utils.hard_update(
                    source_network=self.__policy_network,
                    target_network=self.__target_network,
                )

            # Decay exploration parameter, epsilon
            epsilon = max(epsilon * epsilon_decay, min_epsilon)

            # Append the total reward
            total_rewards.append(total_reward)

            # Append the total loss
            total_losses.append(
                loss_and_steps[0] / loss_and_steps[1] if loss_and_steps[1] > 0 else 0
            )

            # Plot the race if episode reaches the end
            if state.race_progress == 1 and state.terminal and generate_plots:
                sim.plot_race()

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

            # Checkpoint the model
            self._save_checkpoint(i_episode, optimiser)

            # The episode is complete and not disregarded, so we move to the next one
            i_episode += 1
            self._number_of_episodes_trained += 1

        if generate_plots:
            self._plot_total_rewards(total_rewards)
            self._plot_losses(total_losses)

    def __loss(
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

        q_values = (
            self.__policy_network(states, device=self._device)
            .gather(1, actions)
            .reshape(-1)
        )

        next_q_values = (
            self.__target_network(next_states, device=self._device).max(1).values
        )

        expected_q_values = rewards.reshape(-1) + (
            gamma * next_q_values * ~(dones).reshape(-1)
        )

        return nn.functional.huber_loss(q_values, expected_q_values)

    ############################################################################
    # Explainability Functions
    ############################################################################
    def explain_feature_importance(
        self,
        state: UnifiedRaceState,
        show_plot: bool = False,
    ) -> dict:
        return self._explain_feature_importance(state, self.__policy_network, show_plot)

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
            policy=self.__policy_network,
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
        with torch.no_grad():
            q_values = self.__policy_network(
                x=state.to_tensor(),
                device="cuda" if torch.cuda.is_available() else "cpu",
            )
        return q_values.cpu().numpy()

    ############################################################################
    # Model Saving and Loading
    ############################################################################
    def save_model(
        self,
        file_name: str = "Saved Models/dqn_model",
    ) -> None:
        super()._save_model(
            model_type=DQNModel,
            checkpoints={
                "policy_network": self.__policy_network,
                "target_network": self.__target_network,
            },
            file_name=file_name,
        )

    @staticmethod
    def load_model(
        file_name: str,
    ) -> "DQNModel":
        device = "cuda" if torch.cuda.is_available() else "cpu"
        checkpoint = torch.load(f"{file_name}", map_location=device)
        model = DQNModel(
            selected_driver=checkpoint.get("selected_driver", 44),
            name=checkpoint.get("name", "DQNModel"),
            device=device,
            decision_tree=checkpoint.get("decision_tree", None),
            number_of_episodes_trained=checkpoint.get("number_of_episodes_trained", 0),
            disable_safety_car=checkpoint.get("disable_safety_car", False),
            allowed_years=checkpoint.get("allowed_years", []),
            allowed_tracks=checkpoint.get("allowed_tracks", []),
            reward_function=checkpoint.get("reward_function", basic_reward),
            policy_network=checkpoint["policy_network"],
            target_network=checkpoint["target_network"],
        )
        return model
