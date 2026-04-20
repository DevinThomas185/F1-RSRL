from abc import ABCMeta, abstractmethod
from collections import namedtuple
from copy import deepcopy
from datetime import datetime
from matplotlib import colors, pyplot as plt
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from timeshap.wrappers import TorchModelWrapper
from timeshap.utils import calc_avg_event
from timeshap.explainer import calc_local_report
import shap
import torch

from Classes.Enums import Track, TrackDetails
import Classes.Colours as Colours
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceState.RaceStateUtilities import (
    inverse_scale_gap_ahead,
    inverse_scale_gap_behind,
    inverse_scale_gap_to_leader,
    inverse_scale_last_lap_to_reference,
    inverse_scale_position,
    inverse_scale_stint_length,
    inverse_scale_tyre_degradation,
)
from Classes.RaceStrategy.BaseRaceStrategy import BaseRaceStrategy
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.ConsoleLogger import ConsoleLogger
import plotting

from Classes.Errors import (
    BaseSimulationError,
    SimulationStuckError,
    SafetyCarDeployedError,
    InvalidActionError,
    PitstopNotAppliedError,
    LapAlreadyCompleteError,
    StopLapOutsideRangeError,
)

from Explanation.RecurrentExplainerWrapper import RecurrentExplainerWrapper
import Models.model_utilities as utils
from confidential.MercedesRSTranslator import MercedesRSTranslator

StateTransition = namedtuple(
    "StateTransition",
    [
        "state",
        "action",
        "reward",
        "next_state",
    ],
)


class StrategyRLModel(metaclass=ABCMeta):
    __slots__ = [
        "selected_driver",
        "name",
        "_device",
        "_logger",
        "_number_of_episodes_trained",
        "__is_recurrent",
        # Model Simulation Parameters
        "_disable_safety_car",
        "_allowed_years",
        "_allowed_tracks",
        "_reward_function",
        # Checkpointing
        "__checkpoint_model",
        "__checkpoint_frequency",
        "__checkpoint_directory",
        "__checkpoint_name",
        # Feature Importance
        "__exp_fi_background_data",
        # Decision Trees
        "__decision_tree",
        # Counterfactuals
        "__decision_bounds",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str,
        device: str,
        decision_tree: DecisionTreeClassifier | None,
        logger: ConsoleLogger,
        number_of_episodes_trained: int,
        is_recurrent: bool,
        disable_safety_car: bool,
        allowed_years: list[str],
        allowed_tracks: list[Track],
        reward_function: callable,
    ):
        self.name = name
        self.selected_driver = selected_driver
        self._number_of_episodes_trained = number_of_episodes_trained
        # GPU if available, else CPU
        self.__decision_tree = decision_tree
        self._device = device if torch.cuda.is_available() else "cpu"
        self._logger = logger
        self.__is_recurrent = is_recurrent

        # Checkpointing
        self.__checkpoint_model = False
        self.__checkpoint_frequency = 1
        self.__checkpoint_directory = (
            f"Saved Models/{self.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        )
        self.__checkpoint_name = self.name

        # Model Simulation Parameters
        self.set_model_simulation_parameters(
            disable_safety_car=disable_safety_car,
            allowed_years=allowed_years,
            allowed_tracks=allowed_tracks,
            reward_function=reward_function,
        )

        # Explanation
        self.__exp_fi_background_data = None

        # Counterfactuals
        self.__decision_bounds = None

    def set_model_simulation_parameters(
        self,
        disable_safety_car: bool,
        allowed_years: list[str],
        allowed_tracks: list[Track],
        reward_function: callable,
    ) -> None:
        """Set the model simulation parameters, for use with models that were
        trained before the simulation parameters were set.

        Args:
            disable_safety_car (bool): Whether or not to disable the safety car
            allowed_years (list[str]): The allowed years
            allowed_tracks (list[Track]): The allowed tracks
            reward_function (callable): The reward function
        """
        self._disable_safety_car = disable_safety_car
        self._allowed_years = allowed_years
        self._allowed_tracks = allowed_tracks
        self._reward_function = reward_function

    ############################################################################
    # Checkpointing Methods
    ############################################################################
    def _setup_checkpointing(
        self,
        checkpointing_details: dict[str, any] | None = None,
    ) -> None:
        self.__checkpoint_model = checkpointing_details is not None

        if self.__checkpoint_model:
            self.__checkpoint_frequency = checkpointing_details.get(
                "checkpoint_frequency", self.__checkpoint_frequency
            )
            self.__checkpoint_directory = checkpointing_details.get(
                "checkpoint_directory", self.__checkpoint_directory
            )
            self.__checkpoint_name = checkpointing_details.get(
                "checkpoint_name", self.__checkpoint_name
            )
            utils.create_directory(self.__checkpoint_directory)

    def _save_checkpoint(
        self,
        episode_number: int,
        optimiser: torch.optim.Optimizer,
    ) -> None:
        if (
            self.__checkpoint_model
            and episode_number % self.__checkpoint_frequency == 0
        ):
            old_name = self.name
            self.name = self.name + f"_CP{episode_number}"
            self.save_model(
                file_name=f"{self.__checkpoint_directory}/{self.__checkpoint_name}_CP{episode_number}"
            )
            self.name = old_name

            self.save_optimiser_state(optimiser)

    ############################################################################
    # Training Methods
    ############################################################################
    @abstractmethod
    def train(
        self,
    ) -> None:
        """Train the model"""
        raise NotImplementedError

    def _save_training_parameters(
        self,
        training_parameters: dict[str, any],
    ) -> None:
        training_parameters = {k: str(v) for k, v in training_parameters.items()}
        if self.__checkpoint_model:
            file_name = f"{self.__checkpoint_directory}/training_parameters"
            utils.save_json(
                training_parameters,
                file_name,
            )

    def _handle_simulation_error(
        self,
        exception: BaseSimulationError,
        verbose: bool,
    ) -> None:
        if isinstance(exception, SimulationStuckError):
            exception_message = "SIMULATION STUCK"
        elif isinstance(exception, SafetyCarDeployedError):
            exception_message = f"SAFETY CAR DEPLOYED TOO MANY TIMES - {exception.num_vsc_laps} VSC, {exception.num_fsc_laps} FSC"
        elif isinstance(exception, InvalidActionError):
            exception_message = f"INVALID ACTION SELECTED - {exception.type}"
        elif isinstance(exception, PitstopNotAppliedError):
            exception_message = f"PITSTOP NOT APPLIED - L{exception.lap_number:.2f}"
        elif isinstance(exception, LapAlreadyCompleteError):
            exception_message = f"LAP ALREADY COMPLETE - L{exception.lap_number:.2f}"
        elif isinstance(exception, StopLapOutsideRangeError):
            exception_message = f"STOP LAP OUTSIDE RANGE - L{exception.stop_lap:.2f}"

        self._logger.log(
            message=exception_message,
            title="FAILURE",
            verbose=verbose,
        )

    def train_viper(
        self,
        max_depth: int = 6,
        max_iters: int = 5,
        max_samples: int = 10,
        is_reweight: bool = False,
        n_batch_rollouts: int = 20,
        n_test_rollouts: int = 20,
        verbose: bool = False,
        generate_plots: bool = False,
    ) -> None:
        def get_rollout(model):
            rollout = []
            sim = MercedesRSTranslator(
                selected_driver=self.selected_driver,
                seed=np.random.randint(0, 1_000_000),
                allowed_years=self._allowed_years,
                allowed_tracks=self._allowed_tracks,
                disable_safety_car=self._disable_safety_car,
            )
            _, state = sim.initialise_random_simulation()
            if isinstance(model, StrategyRLModel) and model.__is_recurrent:
                model.reset_h()

            while not state.terminal:
                try:
                    if isinstance(model, DecisionTreeClassifier):
                        s = UnifiedRaceState.to_tensor_dataframe([state])
                        action = SimpleRaceStrategy(model.predict(s))
                    else:
                        action = model.predict(state)
                    next_state = sim.step(strategy=action)
                    reward = self._reward_function(state, action, next_state)
                    rollout.append((state, action, reward))
                    state = next_state
                except BaseSimulationError as e:
                    if not e.simulator_at_fault:
                        rollout.append((state, action, -1000))
                    break
            return rollout

        def get_rollouts(model):
            rollouts = []
            while len(rollouts) < n_batch_rollouts:
                rollouts.extend(get_rollout(model))
            return rollouts

        def sample(
            obss, acts, q_vals
        ) -> tuple[list[UnifiedRaceState], list[BaseRaceStrategy], list[np.ndarray]]:
            ps = np.max(q_vals, axis=1) - np.min(q_vals, axis=1)
            ps = ps / np.sum(ps)

            if is_reweight:
                idxs = np.random.choice(
                    len(obss), size=min(max_samples, np.sum(ps > 0)), p=ps
                )
            else:
                idxs = np.random.choice(
                    len(obss), size=min(max_samples, np.sum(ps > 0)), replace=False
                )

            return (
                [obss[i] for i in idxs],
                [acts[i] for i in idxs],
                [q_vals[i] for i in idxs],
            )

        def test_student(student):
            cum_rew = 0
            for _ in range(n_test_rollouts):
                student_trace = get_rollout(student)
                cum_rew += sum((r for _, _, r in student_trace))
            return cum_rew / n_test_rollouts

        def identify_best_policy(students):
            self._logger.log(f"Initial policy count: {len(students)}", verbose=verbose)
            while len(students) > 1:
                students = sorted(students, key=lambda x: x[1], reverse=True)
                n_students = int((len(students) + 1) / 2)
                self._logger.log(f"Number of students: {n_students}", verbose=verbose)

                new_students = []
                for i in range(n_students):
                    student, rew = students[i]
                    new_rew = test_student(student)
                    new_students.append((student, new_rew))
                    self._logger.log(f"Reward: {rew} -> {new_rew}", verbose=verbose)

                students = new_students

            if len(students) != 1:
                raise ValueError("Error in identifying the best policy")

            return students[0][0]

        self.__decision_tree = DecisionTreeClassifier(max_depth=max_depth)

        obss, acts, qs = [], [], []
        students = []
        train_and_test_accuracies = {
            "train": {},
            "test": {},
        }

        trace = get_rollouts(self)
        obss.extend((o for o, _, _ in trace))
        acts.extend((a for _, a, _ in trace))
        if self.__is_recurrent:
            self.reset_h()
        qs.extend((self.predict_q_values(o) for o, _, _ in trace))

        for i in range(max_iters):
            self._logger.log(f"Iteration {i + 1}", verbose=verbose)

            # Train from a random subset of aggregated data
            cur_obss, cur_acts, cur_qs = sample(obss, acts, qs)
            self._logger.log(
                f"Training student with {len(cur_obss)} points", verbose=verbose
            )

            X = UnifiedRaceState.to_tensor_dataframe(cur_obss)
            Y = pd.DataFrame(a.value for a in cur_acts)
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

            self.__decision_tree.fit(X_train, Y_train)
            train_accuracy = self.__decision_tree.score(X_train, Y_train)
            test_accuracy = self.__decision_tree.score(X_test, Y_test)
            self._logger.log(
                f"Train Accuracy: {train_accuracy}",
                verbose=verbose,
            )
            self._logger.log(
                f"Test Accuracy: {test_accuracy}",
                verbose=verbose,
            )

            train_and_test_accuracies["train"][i] = train_accuracy
            train_and_test_accuracies["test"][i] = test_accuracy

            # Generate trace using student
            student_trace = get_rollouts(self.__decision_tree)
            student_obss = [o for o, _, _ in student_trace]

            # Query the oracle for supervision
            if self.__is_recurrent:
                self.reset_h()
            teacher_qs = [self.predict_q_values(o) for o in student_obss]
            if self.__is_recurrent:
                self.reset_h()
            teacher_acts = [self.predict(o) for o in student_obss]

            # Add the augmented state-action pairs back to aggregate
            obss.extend((o for o in student_obss))
            acts.extend(teacher_acts)
            qs.extend(teacher_qs)

            # Estimate the reward
            cur_rew = sum((r for _, _, r in student_trace)) / n_batch_rollouts
            self._logger.log(f"Student reward: {cur_rew}", verbose=verbose)

            students.append((deepcopy(self.__decision_tree), cur_rew))

        self.__decision_tree = identify_best_policy(students)

        if generate_plots:
            plt.plot(
                list(train_and_test_accuracies["train"].keys()),
                list(train_and_test_accuracies["train"].values()),
                label="Train Accuracy",
            )
            plt.plot(
                list(train_and_test_accuracies["test"].keys()),
                list(train_and_test_accuracies["test"].values()),
                label="Test Accuracy",
            )
            plt.xlabel("Iteration")
            plt.ylabel("Accuracy")
            plt.title("Train and Test Accuracy over Iterations")
            plt.legend()
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
            state (UnifiedRaceState): The state being explained
            show_plot (bool, optional): Whether or not to display the plot. Defaults to False.
        """
        raise NotImplementedError

    def _explain_feature_importance(
        self,
        state: UnifiedRaceState,
        network: torch.nn.Module,
        show_plot: bool,
    ) -> None:
        network.eval()

        if self.__exp_fi_background_data is None:
            self.__exp_fi_background_data = torch.from_numpy(
                pd.read_csv("Datasets/expert_dataset_tensor.csv").values
            ).to(torch.float32)[:, :-4]

        state_tensor = state.to_tensor().unsqueeze(0)
        explainer = shap.DeepExplainer(network, self.__exp_fi_background_data)
        shapley_values = explainer.shap_values(state.to_tensor().unsqueeze(0))
        class_names = SimpleRaceStrategy.get_class_names()
        feature_names = UnifiedRaceState.get_tensor_feature_names()

        if show_plot:
            shap.summary_plot(
                shap_values=shapley_values,
                features=state_tensor,
                feature_names=feature_names,
                class_names=class_names,
            )

        return {
            "shap_values": shapley_values,
            "features": state_tensor,
            "feature_names": feature_names,
            "class_names": class_names,
        }

    def _explain_feature_importance_recurrent(
        self,
        states: list[UnifiedRaceState],
        actions: list[BaseRaceStrategy],
        network: torch.nn.Module,
        show_plot: bool,
    ) -> None:
        network.eval()

        if self.__exp_fi_background_data is None:
            self.__exp_fi_background_data = pd.read_csv(
                "Datasets/expert_dataset_tensor_episodal.csv"
            )
            self.__exp_fi_background_data = self.__exp_fi_background_data.iloc[:, :-4]

        network_wrapped = TorchModelWrapper(RecurrentExplainerWrapper(network))
        f_hs = lambda x, y=None: network_wrapped.predict_last_hs(x, y)

        model_features = UnifiedRaceState.get_tensor_feature_names()

        average_event = calc_avg_event(
            self.__exp_fi_background_data,
            numerical_feats=model_features,
            categorical_feats=[],
        )

        states_df = pd.DataFrame(
            data=[state.to_tensor().numpy() for state in states],
            columns=UnifiedRaceState.get_tensor_feature_names(),
        )

        states_df = np.expand_dims(states_df.to_numpy().copy(), axis=0)

        plot_feats = {v: v for v in model_features}

        pruning_dict = {"tol": 0.025}
        event_dict = {"rs": 42, "nsamples": 32000}
        feature_dict = {
            "rs": 42,
            "nsamples": 32000,
            "feature_names": model_features,
            "plot_features": plot_feats,
        }
        cell_dict = {"rs": 42, "nsamples": 32000, "top_x_feats": 2, "top_x_events": 2}

        coal_plot_data, event_data, feature_data, cell_data = calc_local_report(
            f_hs,
            states_df,
            pruning_dict,
            event_dict,
            feature_dict,
            cell_dict,
            average_event,
        )

        if show_plot:
            plotting.plot_feature_importance(
                states[-1], feature_data["Feature"], feature_data["Shapley Value"]
            )
            plotting.plot_lap_importance(actions, event_data["Shapley Value"])

        return {
            # "feature_importance": {
            #     "feature_names": feature_data["Feature"],
            #     "shapley_values": feature_data["Shapley Value"],
            # },
            # "lap_importance": {
            #     "actions": actions,
            #     "shapley_values": event_data["Shapley Value"],
            # }
            "shap_values": feature_data["Shapley Value"].tolist(),
            "feature_names": feature_data["Feature"].tolist(),
        }

    ############################################################################
    # Decision Tree Methods
    ############################################################################
    def generate_decision_bounds(
        self,
        current_node: int = 0,
        current_bounds: dict[str, any] | None = None,
    ) -> list[tuple[dict[str, any], float]]:
        found_boundaries = []

        continuous_bounds = UnifiedRaceState.get_continuous_feature_bounds()
        ordinal_values = UnifiedRaceState.get_ordinal_feature_values()
        categorical_values = UnifiedRaceState.get_categorical_feature_values()

        if current_bounds is None:
            current_bounds = {"decision": None}

        ###########
        # Leaf node
        ###########
        if self.__decision_tree.tree_.feature[current_node] == -2:
            current_bounds["decision"] = SimpleRaceStrategy(
                self.__decision_tree.classes_[
                    self.__decision_tree.tree_.value[current_node].argmax()
                ]
            )
            return [(current_bounds, 0)]

        ###############
        # Non-leaf node
        ###############
        feature_index = self.__decision_tree.tree_.feature[current_node]
        threshold = self.__decision_tree.tree_.threshold[current_node]
        feature_name = UnifiedRaceState.get_tensor_feature_names()[feature_index]

        # Copy the current bounds for the left and right children
        right_bounds = deepcopy(current_bounds)
        left_bounds = deepcopy(current_bounds)

        ### Update bounds
        # Continuous feature
        if feature_name in continuous_bounds:
            if feature_name in current_bounds:
                min_bound, max_bound = current_bounds[feature_name]
            else:
                min_bound, max_bound = continuous_bounds[feature_name]
            right_bounds[feature_name] = (threshold, max_bound)
            left_bounds[feature_name] = (min_bound, threshold)

        # Ordinal feature
        if feature_name in ordinal_values:
            pass

        # Categorical feature (binary)
        if feature_name in categorical_values:
            left_bounds[feature_name] = ["False"]
            right_bounds[feature_name] = ["True"]

        # Categorical feature (multi)
        for category in categorical_values:
            # If feature_name is an enum of another feature 'category'
            if feature_name in categorical_values[category]:
                if category in current_bounds:
                    current_allowed_values = current_bounds[category]
                else:
                    current_allowed_values = categorical_values[category]
                left_allowed_values = deepcopy(current_allowed_values)
                if feature_name in current_allowed_values:
                    left_allowed_values.remove(feature_name)
                left_bounds[category] = left_allowed_values
                right_bounds[category] = [feature_name]

        # Go left
        found_boundaries.extend(
            self.generate_decision_bounds(
                self.__decision_tree.tree_.children_left[current_node],
                left_bounds,
            )
        )

        # Go right
        found_boundaries.extend(
            self.generate_decision_bounds(
                self.__decision_tree.tree_.children_right[current_node],
                right_bounds,
            )
        )

        return found_boundaries

    def calculate_distance_to_decision_bounds(
        self,
        state: UnifiedRaceState,
        weightings: dict[str, float] = {},
    ) -> tuple[dict[str, any], float]:
        continuous_bounds = UnifiedRaceState.get_continuous_feature_bounds()
        ordinal_values = UnifiedRaceState.get_ordinal_feature_values()
        categorical_values = UnifiedRaceState.get_categorical_feature_values()

        sc_conv = {
            "Vsc": "Virtual Safety Car",
            "Fsc": "Full Safety Car",
            "Nsc": "No Safety Car",
        }

        if self.__decision_bounds is None:
            self.__decision_bounds = self.generate_decision_bounds()

        state_df = state.all_to_dataframe()

        new_decision_bounds = []

        # Get the closest counterfactual
        for db, _ in self.__decision_bounds:

            db_distance = 0
            for feature_name, bounds in db.items():
                # Ignore the decision key
                if feature_name == "decision":
                    continue
                
                feature_distance = 0

                race_val = state_df[feature_name].values[0]

                # Continuous feature
                if feature_name in continuous_bounds.keys():
                    feature_min, feature_max = continuous_bounds[feature_name]
                    feature_range = feature_max - feature_min
                    min_val, max_val = bounds

                    # If outside the bounds, add the distance
                    if race_val < min_val:
                        feature_distance += (min_val - race_val) / feature_range
                    elif race_val > max_val:
                        feature_distance += (race_val - max_val) / feature_range

                # Categorical / Ordinal feature
                else:
                    # If, for this feature, we have not currently got an allowed
                    # value in the given race state, we add to the distance
                    feature_value_string = str(race_val).title()
                    if (
                        sc_conv.get(feature_value_string, feature_value_string)
                        not in bounds
                    ):
                        num_possible_values = len(categorical_values[feature_name])
                        num_allowed_values = len(bounds)
                        dist_per_value = 1 / num_possible_values

                        # Distance for more allowed values is smaller than for less allowed values
                        feature_distance = dist_per_value * (
                            num_possible_values - num_allowed_values
                        )
                
                # Weight the distance
                db_distance += weightings.get(feature_name, 1) * feature_distance


            new_decision_bounds.append((db, db_distance))

        # Sort the counterfactuals by distance
        new_decision_bounds.sort(key=lambda x: x[1])
        self.__decision_bounds = new_decision_bounds

    def has_decision_tree(
        self,
    ) -> bool:
        return self.__decision_tree is not None

    ############################################################################
    # Plotting Methods
    ############################################################################
    def _plot_total_rewards(
        self,
        total_rewards,
    ) -> None:
        plt.plot(range(1, len(total_rewards) + 1), total_rewards)
        plt.xlabel("Episode")
        plt.ylabel("Total Rewards")
        plt.title(f"{self.name} - Total Rewards over Episodes")
        plt.show()

    def _plot_losses(
        self,
        losses,
    ) -> None:
        plt.plot(range(1, len(losses) + 1), losses)
        plt.xlabel("Episode")
        plt.ylabel("Total Losses")
        plt.title(f"{self.name} - Total Losses over Episodes")
        plt.show()

    def plot_decision_tree(
        self,
        state: UnifiedRaceState | None = None,
        ax: plt.Axes | None = None,
        dark_mode: bool = False,
    ) -> None:
        # Create a plot
        if self.__decision_tree is None:
            return

        if ax is None:
            fig, ax = plt.subplots(figsize=(20, 10))

        background_colour = (
            Colours.DARK_BACKGROUND_COLOUR
            if dark_mode
            else Colours.LIGHT_BACKGROUND_COLOUR
        )
        text_colour = (
            Colours.LIGHT_TEXT_COLOUR if dark_mode else Colours.DARK_TEXT_COLOUR
        )

        feature_names = UnifiedRaceState.get_tensor_feature_names()
        class_names = SimpleRaceStrategy.get_class_names()
        state = state.to_tensor().numpy() if state is not None else None

        # Recursively plot the tree
        def recurse(node, depth, x=0, y=1.0, dx=0.1, dy=0.1, is_path_node=True):
            if self.__decision_tree.tree_.feature[node] != -2:  # Not a leaf node
                feature_index = self.__decision_tree.tree_.feature[node]
                name = feature_names[feature_index]
                threshold = self.__decision_tree.tree_.threshold[node]
                decision = f"{name} <= {threshold:.2f}"
            else:  # Leaf node
                class_idx = self.__decision_tree.classes_[
                    self.__decision_tree.tree_.value[node].argmax()
                ]
                decision = class_names[class_idx]

            chosen_path = is_path_node and state is not None

            # Determine color based on path
            fc = colors.to_rgba(background_colour)
            if chosen_path:
                ec = colors.to_rgba("red")
            else:
                ec = colors.to_rgba(text_colour)

            ax.text(
                x,
                y,
                decision,
                ha="center",
                va="center",
                color=text_colour,
                bbox=dict(facecolor=fc, edgecolor=ec),
                size=15.0,
            )

            if self.__decision_tree.tree_.feature[node] != -2:  # Not a leaf node
                # Left child
                left_child = self.__decision_tree.tree_.children_left[node]
                left_color = (
                    "red"
                    if state is not None
                    and state[feature_index] <= threshold
                    and is_path_node
                    else text_colour
                )
                ax.plot([x, x - dx], [y, y - dy], left_color)
                left_path_node = (
                    is_path_node
                    and state is not None
                    and state[feature_index] <= threshold
                )
                recurse(
                    left_child, depth + 1, x - dx, y - dy, dx / 2, dy, left_path_node
                )

                # Right child
                right_child = self.__decision_tree.tree_.children_right[node]
                right_color = (
                    "red"
                    if state is not None
                    and state[feature_index] > threshold
                    and is_path_node
                    else text_colour
                )
                ax.plot(
                    [x, x + dx],
                    [y, y - dy],
                    right_color,
                )
                right_path_node = (
                    is_path_node
                    and state is not None
                    and state[feature_index] > threshold
                )
                recurse(
                    right_child, depth + 1, x + dx, y - dy, dx / 2, dy, right_path_node
                )

        # Start the recursion from the root node
        recurse(0, 0)
        ax.axis("off")
        plt.show()

    def plot_decision_path_bounds(
        self,
        state: UnifiedRaceState | None = None,
        new_bounds: dict[str, any] | None = None,
        ax: plt.Axes | None = None,
        dark_mode: bool = False,
    ) -> None:
        feature_names = UnifiedRaceState.get_feature_names()
        continuous_features = UnifiedRaceState.get_all_continuous_feature_names()
        continuous_bounds = UnifiedRaceState.get_continuous_feature_bounds()
        categorical_features = UnifiedRaceState.get_all_categorical_feature_names()
        categorical_values = UnifiedRaceState.get_categorical_feature_values()

        background_colour = (
            Colours.DARK_BACKGROUND_COLOUR
            if dark_mode
            else Colours.LIGHT_BACKGROUND_COLOUR
        )
        text_colour = (
            Colours.LIGHT_TEXT_COLOUR if dark_mode else Colours.DARK_TEXT_COLOUR
        )
        primary_colour = (
            Colours.DARK_PRIMARY_COLOUR if dark_mode else Colours.PRIMARY_COLOUR
        )
        secondary_colour = (
            Colours.DARK_SECONDARY_COLOUR if dark_mode else Colours.SECONDARY_COLOUR
        )
        secondary_tertiary_colour = (
            Colours.DARK_SECONDARY_TERTIARY_COLOUR
            if dark_mode
            else Colours.SECONDARY_TERTIARY_COLOUR
        )
        tertiary_colour = (
            Colours.DARK_TERTIARY_COLOUR if dark_mode else Colours.TERTIARY_COLOUR
        )

        ax.set_facecolor(background_colour)
        plotting.set_ax_colours(ax, text_colour)

        # Get the state values
        if state is not None:
            state_df = state.all_to_dataframe()

        # Number of features
        n_features = len(feature_names)

        # Plotting
        if ax is None:
            _, ax = plt.subplots(figsize=(10, 6))

        # Set background colour
        # ax.set_facecolor(Colours.BACKGROUND_COLOUR)

        # Set y-ticks to feature names
        ax.set_yticks(np.arange(n_features))
        ax.set_yticklabels(reversed(feature_names), fontsize=plotting.TITLE_SIZE)

        # Length of each bar (arbitrary but consistent)
        bar_length = 1.0

        # Convert category name for just safety car status (since enum name is not the string name)
        sc_conv = {
            "No Safety Car": "Nsc",
            "Virtual Safety Car": "Vsc",
            "Full Safety Car": "Fsc",
        }

        # Plot bars for continuous features
        for i, feature in enumerate(reversed(feature_names)):
            if feature in continuous_features:
                min_val, max_val = continuous_bounds[feature]

                # Markers at min and max values
                line_length = 0.8
                ymin = i - line_length / 2
                ymax = i + line_length / 2

                ax.vlines(x=0, ymin=ymin, ymax=ymax, color=text_colour)
                ax.vlines(x=bar_length, ymin=ymin, ymax=ymax, color=text_colour)

                # Add text annotations for min and max values
                ax.text(
                    -0.05,
                    i,
                    f"{min_val}",
                    va="center",
                    ha="right",
                    color=text_colour,
                    fontsize=plotting.TICK_SIZE,
                )
                ax.text(
                    bar_length + 0.05,
                    i,
                    f"{max_val}",
                    va="center",
                    ha="left",
                    color=text_colour,
                    fontsize=plotting.TICK_SIZE,
                )

                if state is not None:
                    state_val = state_df[feature].values[0]
                    normalised_state_val = (
                        (state_val - min_val) / (max_val - min_val) * bar_length
                    )
                    ax.plot(
                        normalised_state_val,
                        i,
                        color=tertiary_colour,
                        marker="o",
                    )
                    ax.text(
                        normalised_state_val - 0.05,
                        i,
                        f"{round(state_val, 2)}",
                        va="center",
                        ha="center",
                        color=text_colour,
                        fontsize=plotting.TICK_SIZE,
                    )

                if new_bounds is not None and feature in new_bounds:
                    # Constrained bounds
                    new_min, new_max = new_bounds[feature]
                    normalised_new_min = (
                        (new_min - min_val) / (max_val - min_val) * bar_length
                    )
                    normalised_new_max = (
                        (new_max - min_val) / (max_val - min_val) * bar_length
                    )
                    if new_min != min_val:
                        ax.text(
                            normalised_new_min - 0.02,
                            i,
                            f"{round(new_min, 2)}",
                            va="center",
                            ha="right",
                            color=text_colour,
                            fontsize=plotting.TICK_SIZE,
                        )
                    if new_max != max_val:
                        ax.text(
                            normalised_new_max + 0.02,
                            i,
                            f"{round(new_max, 2)}",
                            va="center",
                            ha="left",
                            color=text_colour,
                            fontsize=plotting.TICK_SIZE,
                        )

                    ax.barh(
                        i,
                        normalised_new_max - normalised_new_min,
                        left=normalised_new_min,
                        color=secondary_colour,
                        edgecolor=text_colour,
                    )
                else:
                    # Original bars
                    ax.barh(i, bar_length, color=primary_colour, edgecolor=text_colour)

            elif feature in categorical_features:
                categories = categorical_values[feature]
                num_categories = len(categories)
                bar_width = bar_length / num_categories

                for j, category in enumerate(categories):
                    category_name = category
                    category_title = sc_conv.get(category_name, category_name)

                    bar_colour = primary_colour

                    # If this bar is the current state value for this feature
                    bar_is_current_state_value = (
                        state is not None
                        and str(state_df[feature].values[0]).title() == category_title
                    )

                    # If this bar is a constrained value for this feature
                    bar_is_constrained_value = (
                        new_bounds is not None
                        and feature in new_bounds
                        and category in new_bounds[feature]
                    )

                    if bar_is_current_state_value and bar_is_constrained_value:
                        bar_colour = secondary_tertiary_colour
                    elif bar_is_constrained_value:
                        bar_colour = secondary_colour
                    elif bar_is_current_state_value:
                        bar_colour = tertiary_colour

                    ax.barh(
                        i,
                        bar_width,
                        left=j * bar_width,
                        color=bar_colour,
                        edgecolor=text_colour,
                    )
                    ax.text(
                        j * bar_width + bar_width / 2,
                        i,
                        category_name,
                        va="center",
                        ha="center",
                        color=text_colour,
                        fontsize=plotting.TICK_SIZE,
                    )
        # Remove x-axis
        ax.xaxis.set_visible(False)

        # Adjust xlim to leave space for annotations
        margin = 0.2
        ax.set_xlim(-margin, bar_length + margin)

        # Remove gridlines
        ax.grid(False)

        # Legend
        ax.legend(
            handles=[
                Patch(facecolor=primary_colour, label="Original Bounds"),
                Patch(facecolor=secondary_colour, label="Constrained Bounds"),
                Patch(
                    facecolor=secondary_tertiary_colour,
                    label="Both Constrained and Current State Value",
                ),
                Patch(facecolor=tertiary_colour, label="Current State Value"),
            ],
            ncol=4,
            loc="upper center",
            bbox_to_anchor=(0.4, 1.1),
            fontsize=plotting.TICK_SIZE,
        )

        # Show plot
        plt.show()

    def plot_counterfactual(
        self,
        index: int = 0,
        state: UnifiedRaceState | None = None,
        desired_actions: list[SimpleRaceStrategy] | None = None,
        ax: plt.Axes | None = None,
        dark_mode: bool = False,
    ) -> tuple[SimpleRaceStrategy, float, int] | None:
        temp_decision_bounds = []
        if state is not None:
            self.calculate_distance_to_decision_bounds(state=state)

            # If we have a desired action, only consider the counterfactuals that
            # result in the desired action
            if desired_actions is not None:
                for db, score in self.__decision_bounds:
                    if db["decision"] in desired_actions:
                        temp_decision_bounds.append((db, score))
            else:
                temp_decision_bounds = self.__decision_bounds

            cf, score = temp_decision_bounds[index]
        else:
            # If no state is given, just plot the bounds graph
            cf, score = None, 0

        self.plot_decision_path_bounds(
            state=state,
            new_bounds=cf,
            ax=ax,
            dark_mode=dark_mode,
        )

        if cf is not None:
            return cf["decision"], score, len(temp_decision_bounds)
        return None

    ############################################################################
    # Printing Methods
    ############################################################################

    def print_model_summary(
        self,
    ) -> None:
        self._logger.log(f"Model Name: {self.name}")
        self._logger.log(f"Selected Driver: {self.selected_driver}")
        self._logger.log(f"Device: {self._device}")
        self._logger.log(
            f"Number of Episodes Trained: {self._number_of_episodes_trained}"
        )
        self._logger.log(f"Disable Safety Car: {self._disable_safety_car}")
        self._logger.log(f"Allowed Years: {self._allowed_years}")
        self._logger.log(f"Allowed Tracks: {self._allowed_tracks}")
        self._logger.log(f"Reward Function: {self._reward_function}")

    def get_decision_path(
        self,
        state: UnifiedRaceState,
    ) -> str:
        state_tensor = state.to_tensor()
        feature_names = UnifiedRaceState.get_tensor_feature_names()
        continuous_features = UnifiedRaceState.get_continuous_tensor_feature_names()
        class_names = SimpleRaceStrategy.get_class_names()
        dp_string = ""

        # Get the decision path
        decision_path = self.__decision_tree.decision_path(
            UnifiedRaceState.to_tensor_dataframe([state])
        )

        for node_id in decision_path.indices:
            if self.__decision_tree.tree_.feature[node_id] != -2:
                feature_index = self.__decision_tree.tree_.feature[node_id]
                name = feature_names[feature_index]
                threshold = self.__decision_tree.tree_.threshold[node_id]

                # Determine the decision
                if state_tensor[feature_index] <= threshold:
                    # If the feature is continuous, then use the threshold,
                    # otherwise just use the feature name
                    if name in continuous_features:
                        decision = f"{name} <= {threshold:.3f}"
                    else:
                        decision = f"No {name}"
                else:
                    if name in continuous_features:
                        decision = f"{name} > {threshold:.3f}"
                    else:
                        decision = f"{name}"
            else:
                class_idx = self.__decision_tree.classes_[
                    self.__decision_tree.tree_.value[node_id].argmax()
                ]
                decision = f"\n{class_names[class_idx]}".upper()
            dp_string += f"{decision}\n"
        return dp_string

    def get_counterfactual(
        self,
        index: int = 0,
        state: UnifiedRaceState | None = None,
        desired_actions: list[SimpleRaceStrategy] | None = None,
        track_details: TrackDetails | None = None,
    ) -> tuple[str, float]:
        cf_string = ""
        temp_decision_bounds = []
        continuous_features = UnifiedRaceState.get_continuous_feature_names()
        categorical_features = UnifiedRaceState.get_categorical_feature_names()
        state_df = state.all_to_dataframe()

        sc_conv = {
            "Nsc": "No Safety Car",
            "Vsc": "Virtual Safety Car",
            "Fsc": "Full Safety Car",
        }

        feature_to_inverse_scale_function = {
            "Scaled Position": inverse_scale_position,
            "Scaled Gap Ahead": inverse_scale_gap_ahead,
            "Scaled Gap Behind": inverse_scale_gap_behind,
            "Scaled Gap To Leader": inverse_scale_gap_to_leader,
            "Scaled Tyre Degradation": inverse_scale_tyre_degradation,
            "Scaled Stint Length": inverse_scale_stint_length,
            "Scaled Last Lap To Reference": inverse_scale_last_lap_to_reference,
        }

        if state is not None:
            self.calculate_distance_to_decision_bounds(state=state)

            # If we have a desired action, only consider the counterfactuals that
            # result in the desired action
            if desired_actions is not None:
                for db, score in self.__decision_bounds:
                    if db["decision"] in desired_actions:
                        temp_decision_bounds.append((db, score))
            else:
                temp_decision_bounds = self.__decision_bounds

            cf, score = temp_decision_bounds[index]

            for feature, bounds in cf.items():
                if feature == "decision":
                    continue

                state_val = state_df[feature].values[0]
                feature_name = feature

                # Continuous feature
                if feature in continuous_features:
                    min_val, max_val = bounds

                    # If the feature is scaled, we want to invert the scaling to determine the difference
                    if feature in feature_to_inverse_scale_function.keys():
                        state_val = feature_to_inverse_scale_function[feature](
                            state_val
                        )
                        min_val = feature_to_inverse_scale_function[feature](min_val)
                        max_val = feature_to_inverse_scale_function[feature](max_val)
                        feature_name = feature.replace("Scaled ", "")

                    if state_val < min_val:
                        diff = round(min_val - state_val, 3)
                        # Special strings for certain features
                        if feature_name == "Position":
                            cf_string += (
                                f"Lose {diff} position{'s' if diff > 1 else ''}"
                            )
                        elif (
                            feature_name == "Race Progress"
                            and track_details is not None
                        ):
                            extra_laps = round(diff * track_details.TotalLaps, 3)
                            cf_string += f"Complete {extra_laps} more lap{'s' if extra_laps > 1 else ''}"
                        else:
                            cf_string += f"Increase {feature_name} by {diff}"
                        cf_string += "\n"

                    elif state_val > max_val:
                        diff = round(state_val - max_val, 3)
                        # Special strings for certain features
                        if feature_name == "Position":
                            cf_string += (
                                f"Gain {diff} position{'s' if diff > 1 else ''}"
                            )
                        elif (
                            feature_name == "Race Progress"
                            and track_details is not None
                        ):
                            extra_laps = round(diff * track_details.TotalLaps, 3)
                            cf_string += f"Complete {extra_laps} fewer lap{'s' if extra_laps > 1 else ''}"
                        else:
                            cf_string += f"Decrease {feature_name} by {diff}"
                        cf_string += "\n"

                # Categorical feature
                if feature in categorical_features:
                    sv = str(state_val).title()
                    state_val = sc_conv.get(sv, sv)
                    if state_val not in bounds:
                        cf_string += f"Change {feature_name} to {bounds}\n"

        return cf_string, score

    ############################################################################
    # Prediction Methods
    ############################################################################
    @abstractmethod
    def predict(
        self,
        state: UnifiedRaceState,
    ) -> BaseRaceStrategy:
        """Predict the best strategy for the given race state

        Args:
            state (UnifiedRaceState): The race state

        Returns:
            BaseRaceStrategy: The predicted strategy
        """
        raise NotImplementedError

    @abstractmethod
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

    def predict_decision_tree(
        self,
        state: UnifiedRaceState,
    ) -> SimpleRaceStrategy | None:
        if self.__decision_tree is not None:
            state_df = pd.DataFrame(
                [state.to_tensor().numpy()],
                columns=UnifiedRaceState.get_tensor_feature_names(),
            )
            return SimpleRaceStrategy(self.__decision_tree.predict(state_df).item())
        return None

    ############################################################################
    # Save/Load Methods
    ############################################################################
    @abstractmethod
    def save_model(
        self,
        file_name: str = "Saved Models/model",
    ) -> None:
        """Save the model to a file

        Args:
            file_name (str, optional): The file name. Defaults to "Saved Models/model".
        """
        raise NotImplementedError

    def _save_model(
        self,
        model_type,
        checkpoints,
        file_name,
    ) -> None:
        if not file_name.endswith(".pth"):
            file_name += ".pth"

        checkpoints["model_type"] = model_type
        checkpoints["selected_driver"] = self.selected_driver
        checkpoints["name"] = self.name
        checkpoints["device"] = self._device
        checkpoints["decision_tree"] = self.__decision_tree
        checkpoints["number_of_episodes_trained"] = self._number_of_episodes_trained
        checkpoints["disable_safety_car"] = self._disable_safety_car
        checkpoints["allowed_years"] = self._allowed_years
        checkpoints["allowed_tracks"] = self._allowed_tracks
        checkpoints["reward_function"] = self._reward_function
        torch.save(
            checkpoints,
            f"{file_name}",
        )

    @staticmethod
    def load_model(
        file_name: str,
    ) -> "StrategyRLModel":
        """Load a model from a file

        Args:
            file_name (str): The filename of the model to load.

        Returns:
            StrategyRLModel: The loaded model
        """
        # All models will be saved with their type, load that then return the
        # model type's load_model method
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model_type = torch.load(f"{file_name}", map_location=device)["model_type"]
        return model_type.load_model(file_name)

    def save_optimiser_state(
        self,
        optimiser: torch.optim.Optimizer,
    ) -> None:
        """Save the optimiser to a file

        Args:
            optimiser (torch.optim.Optimizer): The optimiser to save
            file_name (str): The filename of the optimiser to save
        """
        torch.save(
            optimiser.state_dict(), f"{self.__checkpoint_directory}/optimiser_state.pth"
        )

    def load_optimiser_state(
        self,
        optimiser: torch.optim.Optimizer,
    ) -> torch.optim.Optimizer:
        """Load the optimiser from a file

        Args:
            optimiser (torch.optim.Optimizer): The optimiser to load
            file_name (str): The filename of the optimiser to load

        Returns:

        """
        file_name = f"{self.__checkpoint_directory}/optimiser_state.pth"
        optimiser.load_state_dict(torch.load(file_name, map_location=self._device))
        return optimiser
