import multiprocessing as mp
import time
from matplotlib import pyplot as plt
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch
from Classes.ConsoleLogger import ConsoleLogger
from Classes.Enums import Track
from Classes.Errors import BaseSimulationError
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Architectures.RecurrentActorCritic import RecurrentActorCritic, ACNet
from Models.StrategyRLModel import StrategyRLModel
from ParallelModels.SharedAdam import SharedAdam
from confidential.MercedesRSTranslator import MercedesRSTranslator
import Models.model_utilities as utils
from RewardFunctions.RewardFunctions import basic_reward


class A3CModel(StrategyRLModel):
    __slots__ = [
        "__global_network",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str = "A3CModel",
        device: str = "cpu",
        global_network: nn.Module | None = None,
        logger: ConsoleLogger = ConsoleLogger(),
        number_of_episodes_trained: int = 0,
        disable_safety_car: bool = False,
        allowed_years: list[str] = [],
        allowed_tracks: list[str] = [],
        reward_function: callable = basic_reward,
    ) -> None:
        super().__init__(
            selected_driver=selected_driver,
            name=name,
            device=device,
            decision_tree=None,
            logger=logger,
            number_of_episodes_trained=number_of_episodes_trained,
            is_recurrent=False,
            disable_safety_car=disable_safety_car,
            allowed_years=allowed_years,
            allowed_tracks=allowed_tracks,
            reward_function=reward_function,
        )

        if global_network is None:
            self.__global_network = ACNet(
                UnifiedRaceState.size(), len(SimpleRaceStrategy)
            ).to(device)
        else:
            self.__global_network = global_network

    ############################################################################
    # Training Methods
    ############################################################################
    def train(
        self,
        min_episodes: int,
        simulation_step_size: float = 1.0,
        checkpointing_details: dict[str, any] | None = None,
        gamma: float = 0.99,
        value_loss_coef: float = 0.5,
        max_grad_norm: float = 50,
        learning_rate: float = 0.001,
        weight_decay: float = 0.001,
        generate_plots: bool = False,
    ) -> None:
        # Set device
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Setup checkpointing
        self._setup_checkpointing(checkpointing_details)
        # TODO: Move this to be in setup_checkpointing
        self._save_training_parameters(locals())

        hidden_size = 256
        num_layers = 1
        self.__global_network.share_memory()
        optimiser = SharedAdam(
            self.__global_network.parameters(),
            lr=learning_rate,
            weight_decay=weight_decay,
        )
        global_ep, global_ep_r, res_queue = (
            mp.Value("i", 1),
            mp.Value("d", 0.0),
            mp.Queue(),
        )

        # Create simulation runners
        simulation_runners = [
            SimulationTrainer(
                runner_id=i,
                device=device,
                global_network=self.__global_network,
                hidden_size=hidden_size,
                num_layers=num_layers,
                optimiser=optimiser,
                global_ep=global_ep,
                global_ep_r=global_ep_r,
                res_queue=res_queue,
                min_episodes=min_episodes,
                simulation_step_size=simulation_step_size,
                selected_driver=self.selected_driver,
                allowed_years=self._allowed_years,
                allowed_tracks=self._allowed_tracks,
                logger=self._logger,
                reward_function=self._reward_function,
                disable_safety_car=self._disable_safety_car,
                gamma=gamma,
                value_loss_coef=value_loss_coef,
                max_grad_norm=max_grad_norm,
            )
            # for i in range(1, mp.cpu_count() + 1)
            for i in range(1, 3)
        ]

        # Start simulation runners
        [runner.start() for runner in simulation_runners]

        simulation_tester = SimulationTester(
            runner_id=0,
            global_ep=global_ep,
            min_episodes=min_episodes,
            device=device,
            global_network=self.__global_network,
            hidden_size=hidden_size,
            num_layers=num_layers,
            selected_driver=self.selected_driver,
            simulation_step_size=simulation_step_size,
            disable_safety_car=self._disable_safety_car,
            allowed_years=self._allowed_years,
            allowed_tracks=self._allowed_tracks,
            logger=self._logger,
            reward_function=self._reward_function,
        )
        simulation_tester.start()

        # If we know the runners are still running, we can check for the minimum number of episodes
        while global_ep.value <= min_episodes:
            self._save_checkpoint(global_ep.value, optimiser)

        # Plot
        res = []
        while True:
            r = res_queue.get()
            if r is not None:
                res.append(r)
            else:
                break

        [runner.join() for runner in simulation_runners]
        simulation_tester.join()

        if generate_plots:
            plt.plot(res)
            plt.ylabel("Moving average of episode reward")
            plt.xlabel("Episode")
            plt.show()

    ############################################################################
    # Explanation Methods
    ############################################################################
    def explain_feature_importance(
        self,
        state: UnifiedRaceState,
        show_plot: bool = False,
    ) -> dict:
        """Explain the feature importance of the model

        Args:
            state (UnifiedRaceState): The state to explain
            show_plot (bool, optional): Whether to show the plot. Defaults to False.

        Returns:
            dict: The feature importance dictionary
        """
        raise NotImplementedError

    ############################################################################
    # Prediction Methods
    ############################################################################
    def predict(
        self,
        state: UnifiedRaceState,
    ) -> SimpleRaceStrategy:
        with torch.no_grad():
            state_tensor = state.to_tensor().to(
                "cuda" if torch.cuda.is_available() else "cpu"
            )
            action = SimpleRaceStrategy(self.__global_network.max_action(state_tensor))
        return action

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
        file_name: str = "Saved Models/model",
    ) -> None:
        super()._save_model(
            model_type=A3CModel,
            checkpoints={
                "global_network": self.__global_network,
            },
            file_name=file_name,
        )

    @staticmethod
    def load_model(
        file_name: str,
    ) -> "A3CModel":
        checkpoint = torch.load(f"{file_name}")
        model = A3CModel(
            selected_driver=checkpoint["selected_driver"],
            name=checkpoint["name"],
            device=checkpoint["device"],
            number_of_episodes_trained=checkpoint["number_of_episodes_trained"],
            global_network=checkpoint["global_network"],
        )
        return model


class SimulationTrainer(mp.Process):

    def __init__(
        self,
        runner_id: int,
        device: str,
        global_network: nn.Module,
        hidden_size: int,
        num_layers: int,
        optimiser,
        global_ep: mp.Value,
        global_ep_r: mp.Value,
        res_queue: mp.Queue,
        selected_driver: int,
        min_episodes: int,
        simulation_step_size: float,
        disable_safety_car: bool,
        allowed_years: list[str],
        allowed_tracks: list[Track],
        logger: ConsoleLogger,
        reward_function: callable,
        gamma: float,
        value_loss_coef: float,
        max_grad_norm: float,
    ):
        super(SimulationTrainer, self).__init__()
        self.runner_id = runner_id
        self.optimiser = optimiser
        self.global_ep = global_ep
        self.global_ep_r = global_ep_r
        self.res_queue = res_queue
        self.device = device
        self.global_network = global_network
        self.local_network = ACNet(UnifiedRaceState.size(), len(SimpleRaceStrategy)).to(
            device
        )

        self.selected_driver = selected_driver

        self.min_episodes = min_episodes
        self.simulation_step_size = simulation_step_size
        self.disable_safety_car = disable_safety_car
        self.allowed_years = allowed_years
        self.allowed_tracks = allowed_tracks
        self.reward_function = reward_function
        self.gamma = gamma
        self.value_loss_coef = value_loss_coef
        self.max_grad_norm = max_grad_norm
        self.logger = logger

    def __train_one_episode(self):
        done = False

        buffer_s, buffer_a, buffer_r = [], [], []

        sim = MercedesRSTranslator(
            selected_driver=self.selected_driver,
            seed=np.random.randint(0, 1_000_000),
            allowed_years=self.allowed_years,
            allowed_tracks=self.allowed_tracks,
            disable_safety_car=self.disable_safety_car,
            verbose=False,
            logger=self.logger,
        )
        _, state = sim.initialise_random_simulation()
        state_tensor = state.to_tensor()

        self.local_network.load_state_dict(self.global_network.state_dict())

        ep_r = 0

        while not done:
            action = SimpleRaceStrategy(self.local_network.choose_action(state_tensor))

            try:
                next_state = sim.step(
                    step=self.simulation_step_size,
                    strategy=action,
                )
            except BaseSimulationError as e:
                # print(e)
                if e.simulator_at_fault:
                    return 0, 0, True, ""
                next_state = state
                next_state.terminal = True

            next_state_tensor = next_state.to_tensor().to(self.device)
            reward = self.reward_function(state, action, next_state)
            done = next_state.terminal

            ep_r += reward

            buffer_s.append(state_tensor)
            buffer_a.append(action.value)
            buffer_r.append(reward)

            state = next_state
            state_tensor = next_state_tensor

            # print(
            #     f"{action:<11} {reward:<6} P{next_state.position:<2} {next_state.race_progress:<4.2f} {next_state.current_tyre:<1} {str(pol.detach().numpy())} {val.item():.2f}"
            # )

        v_s_ = 0
        buffer_v_target = []
        for r in buffer_r[::-1]:
            v_s_ = r + self.gamma * v_s_
            buffer_v_target.append(v_s_)
        buffer_v_target.reverse()

        policy_loss, value_loss = self.local_network.loss_func(
            torch.vstack(buffer_s),
            torch.tensor(buffer_a),
            torch.tensor(buffer_v_target),
        )

        total_loss = (policy_loss + value_loss * self.value_loss_coef).mean()

        self.optimiser.zero_grad()
        total_loss.backward()
        self.__ensure_shared_grads()
        torch.nn.utils.clip_grad_norm_(
            self.local_network.parameters(), self.max_grad_norm
        )
        self.optimiser.step()

        return total_loss, ep_r, False, sim.get_pitstops(self.selected_driver)

    def __ensure_shared_grads(self):
        for lp, gp in zip(
            self.local_network.parameters(), self.global_network.parameters()
        ):
            if gp.grad is not None:
                return
            gp._grad = lp.grad

    def run(self):
        np.random.seed(self.runner_id)

        while self.global_ep.value <= self.min_episodes:
            total_loss, ep_r, failed_episode, tyre_strategy = self.__train_one_episode()

            if failed_episode:
                print(f"| {self.runner_id:<3} | Episode: {self.global_ep.value} FAILED")
            else:
                print(
                    f"| {self.runner_id:<3} | Episode: {self.global_ep.value} | Total Reward {ep_r} | Total Loss {total_loss.item():.3f} | {tyre_strategy}"
                )
                with self.global_ep.get_lock():
                    self.global_ep.value += 1
                with self.global_ep_r.get_lock():
                    if self.global_ep_r.value == 0.0:
                        self.global_ep_r.value = ep_r
                    else:
                        self.global_ep_r.value = (
                            self.global_ep_r.value * 0.99 + ep_r * 0.01
                        )
                self.res_queue.put(self.global_ep_r.value)

        self.res_queue.put(None)


class SimulationTester(mp.Process):
    def __init__(
        self,
        runner_id: int,
        global_ep: mp.Value,
        min_episodes: int,
        device: str,
        global_network: nn.Module,
        hidden_size: int,
        num_layers: int,
        selected_driver: int,
        simulation_step_size: float,
        disable_safety_car: bool,
        allowed_years: list[str],
        allowed_tracks: list[Track],
        logger: ConsoleLogger,
        reward_function: callable,
    ):
        super(SimulationTester, self).__init__()
        self.runner_id = runner_id
        self.global_ep = global_ep
        self.min_episodes = min_episodes
        self.device = device
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.global_network = global_network
        self.local_network = ACNet(UnifiedRaceState.size(), len(SimpleRaceStrategy))
        self.selected_driver = selected_driver
        self.simulation_step_size = simulation_step_size
        self.disable_safety_car = disable_safety_car
        self.allowed_years = allowed_years
        self.allowed_tracks = allowed_tracks
        self.logger = logger
        self.reward_function = reward_function
        self.__stop_testing = False

    def __test_one_episode(self):
        sim = MercedesRSTranslator(
            selected_driver=self.selected_driver,
            seed=np.random.randint(0, 1_000_000),
            allowed_years=self.allowed_years,
            allowed_tracks=self.allowed_tracks,
            disable_safety_car=self.disable_safety_car,
            verbose=False,
            logger=self.logger,
        )
        _, state = sim.initialise_random_simulation()
        state_tensor = state.to_tensor()

        # h_c = self.local_network.get_init_hidden_state(device=self.device)

        self.local_network.load_state_dict(self.global_network.state_dict())

        total_reward = 0

        while not state.terminal:
            with torch.no_grad():
                action = SimpleRaceStrategy(self.local_network.max_action(state_tensor))

            try:
                next_state = sim.step(
                    step=self.simulation_step_size,
                    strategy=action,
                )
            except BaseSimulationError as e:
                return 0, 0, e

            next_state_tensor = next_state.to_tensor().to(self.device)
            total_reward += self.reward_function(state, action, next_state)

            state = next_state
            state_tensor = next_state_tensor

        finishing_position = sim.get_finishing_position(self.selected_driver)

        return finishing_position, total_reward, None

    def run(self):
        np.random.seed(self.runner_id)
        start_time = time.time()
        while self.global_ep.value <= self.min_episodes:
            time_string = time.strftime(
                "%H:%M:%S", time.gmtime(time.time() - start_time)
            )
            finishing_position, reward, error = self.__test_one_episode()
            if error is None:
                # Report results and wait a minute before running the next episode
                print(f"TEST {time_string} | Reward: {reward} | P{finishing_position}")
                time.sleep(60)
            elif isinstance(error, BaseSimulationError) and error.simulator_at_fault:
                # Report an error and immediately run the next episode
                print(f"TEST {time_string} | Simulator Failure")
            else:
                # Report model failed and wait a minute before running the next episode
                print(f"TEST {time_string} | {error}")
                time.sleep(60)
