from collections import deque
import re
import sys
from matplotlib import pyplot as plt
import numpy as np
import torch
import pandas as pd

# Project imports
from Architectures.QNetwork import QNetwork
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.Enums import Track
import Classes.Colours as Colours
from Classes.ConsoleLogger import ConsoleLogger
from F123.F123Translator import F123Translator
from Models.DQNModel import DQNModel
from Models.DRQNModel import DRQNModel
from Models.MercedesProbabilisticModel import MercedesProbabilisticModel
from Models.StrategyRLModel import StrategyRLModel
from RewardFunctions.RewardFunctions import thomas_reward_2
import plotting

# PySide imports
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

# Plotting imports
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure


# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from GUI.ui_form import Ui_RL_Strategy_GUI
from confidential.MercedesRSTranslator import MercedesRSTranslator

DEFAULT_BARH_KEYS = [
    "Last Lap",
    "Gap To Leader",
    "Gap Behind",
    "Gap Ahead",
    "Tyre Degradation",
    "Current Tyre",
    "Lap Number",
    "Safety Car",
    "Position",
]
DEFAULT_BARH_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
DEFAULT_FI_EXP = {
    "shap_values": [1] * UnifiedRaceState.size(),
    "feature_names": UnifiedRaceState.get_tensor_feature_names(),
}

DARK_MODE = True


class F123ListenerThread(QThread):
    state_updated = Signal(UnifiedRaceState, SimpleRaceStrategy, dict)

    def __init__(
        self, udp_ip, udp_port, loaded_model: StrategyRLModel, race_plot_ax: plt.Axes
    ):
        super().__init__()
        self.__loaded_model = loaded_model
        self.__listening = False
        self.__udp_ip = udp_ip
        self.__udp_port = udp_port
        self.__fi_exp = DEFAULT_FI_EXP
        self.__sim = None
        self.__race_plot_ax = race_plot_ax

    def stop_listening(self):
        self.__listening = False
        if self.__sim is not None:
            self.__sim.stop_listening()

    def __plot_race_plot(self):
        self.__race_plot_ax.clear()
        self.__sim.plot_live_race(
            ax=self.__race_plot_ax,
            dark_mode=DARK_MODE,
        )
        self.__race_plot_ax.figure.canvas.draw()

    def run(self):
        self.__sim = F123Translator(udp_ip=self.__udp_ip, udp_port=self.__udp_port)
        self.__listening = True
        states: list[UnifiedRaceState] = []
        actions: list[SimpleRaceStrategy] = [SimpleRaceStrategy.NO_PIT]

        while self.__listening:
            state = self.__sim.step()

            # If there is no state received in the packet, continue
            if state is None:
                continue

            # If there is no state in the list, append the first state
            if states == []:
                states.append(state)

            # Append the state if there is a new lap
            into_next_lap = int(states[-1].partial_lap_number) < int(
                state.partial_lap_number
            )
            if into_next_lap:
                states.append(state)
                action = MercedesProbabilisticModel.infer_simple_race_strategy(
                    states[-1], state
                )
                actions.append(action)

                # Plot the race plot if we have moved into the next lap
                self.__plot_race_plot()

            if isinstance(self.__loaded_model, DRQNModel):
                # If on the first lap, or we have entered a new lap, recalculate the feature importance
                if into_next_lap and len(states) == len(actions):
                    try:
                        self.__fi_exp = self.__loaded_model.explain_feature_importance(
                            states, actions
                        )
                    except Exception as e:
                        print(e)
                        self.__fi_exp = DEFAULT_FI_EXP
            else:
                self.__fi_exp = self.__loaded_model.explain_feature_importance(state)
            prediction = self.__loaded_model.predict(state)
            self.state_updated.emit(state, prediction, self.__fi_exp)

        return 0


class ModelTrainerThread(QThread, ConsoleLogger):
    trained_model = Signal(DQNModel)
    console_updated = Signal(str)

    def __init__(self, model_parameters: dict):
        super().__init__()
        self.__model_parameters = model_parameters

    def log(self, message, title=None, verbose=True):
        if not verbose:
            return

        if title is None:
            self.console_updated.emit(message)
        else:
            self.console_updated.emit(f"[{title}] {message}")

    def run(self):
        policy_network = QNetwork(UnifiedRaceState.size(), len(SimpleRaceStrategy))
        target_network = QNetwork(UnifiedRaceState.size(), len(SimpleRaceStrategy))

        model = DQNModel(
            selected_driver=self.__model_parameters["selected_driver"],
            name=self.__model_parameters["name"],
            policy_network=policy_network,
            target_network=target_network,
            logger=self,
        )

        model.train(
            num_episodes=self.__model_parameters["num_episodes"],
            seed=self.__model_parameters["seed"],
            fixed_seed=self.__model_parameters["fixed_seed"],
            simulation_step_size=self.__model_parameters["simulation_step_size"],
            disable_safety_car=self.__model_parameters[
                "disable_safety_car"
            ],  # TODO: Add this in GUI
            allowed_years=self.__model_parameters[
                "allowed_years"
            ],  # TODO: Add this in GUI
            allowed_tracks=self.__model_parameters[
                "allowed_tracks"
            ],  # TODO: Add this in GUI
            reward_function=self.__model_parameters["reward_function"],
            verbose=self.__model_parameters["verbose"],
            epsilon=self.__model_parameters["epsilon"],
            epsilon_decay=self.__model_parameters["epsilon_decay"],
            min_epsilon=self.__model_parameters["min_epsilon"],
            gamma=self.__model_parameters["gamma"],
            learning_rate=self.__model_parameters["learning_rate"],
            weight_decay=self.__model_parameters["weight_decay"],
            replay_buffer_size=self.__model_parameters["replay_buffer_size"],
            replay_buffer_sample_size=self.__model_parameters[
                "replay_buffer_sample_size"
            ],
            episodes_to_update_target=self.__model_parameters[
                "episodes_to_update_target"
            ],
            optimiser_type=self.__model_parameters["optimiser_type"],
        )

        self.trained_model.emit(model)

        return 0


class RL_Strategy_GUI(QWidget):
    __slots__ = [
        # Model Deployment
        "__stopped_listening",
        "__listener_thread",
        "__loaded_model",
        "__last_state",
        "__current_sim",
        "__current_track_details",
        "__current_sim_states",
        "__current_sim_actions",
        "__next_model_action",
        # Feature Explanation
        "__fi_exp",
        "__fi_exp_canvas",
        "__fi_exp_ax",
        "__fi_exp_barh",
        # Decision Tree
        "__dt_canvas",
        "__dt_ax",
        # Counterfactual
        "__cf_index",
        "__cf_total",
        "__cf_canvas",
        "__cf_ax",
        # Race Plot
        "__rp_canvas",
        "__rp_ax",
        # Test Results
        "__all_test_results",
        "__current_test_results",
        "__ts_canvas",
        "__ts_ax",
        # Model Training
        "__model_trainer_thread",
        "__console_history",
        "__trained_model",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_RL_Strategy_GUI()
        self.ui.setupUi(self)
        self.setWindowTitle("Imperial X Mercedes - RL Strategy")

        ############################
        # Set GUI colours
        ############################
        background_colour = (
            Colours.DARK_BACKGROUND_COLOUR
            if DARK_MODE
            else Colours.LIGHT_BACKGROUND_COLOUR
        )
        text_colour = (
            Colours.LIGHT_TEXT_COLOUR if DARK_MODE else Colours.DARK_TEXT_COLOUR
        )

        ############################
        # Initialise local variables
        ############################
        self.__stopped_listening = True
        self.__listener_thread = None
        self.__loaded_model = None
        self.__last_state = None
        self.__current_sim = None
        self.__current_track_details = None
        self.__current_sim_states = []
        self.__current_sim_actions = []
        self.__next_model_action = SimpleRaceStrategy.NO_PIT

        self.__fi_exp = DEFAULT_FI_EXP

        self.__cf_index = 0
        self.__cf_total = 0

        self.__all_test_results = pd.read_csv("test_model_results.csv")
        self.__all_test_results.fillna("", inplace=True)
        self.__current_test_results = self.__all_test_results.copy()

        self.__model_trainer_thread = None
        self.__console_history = deque(maxlen=10)  # TODO: Make this longer
        self.__trained_model = None

        ###############
        # Set up images
        ###############
        imperial = QPixmap("./GUI/Images/imperial_w.png")
        self.ui.lbl_ImperialLogo.setPixmap(
            imperial.scaled(
                self.ui.lbl_ImperialLogo.width(),
                self.ui.lbl_ImperialLogo.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

        mercedes = QPixmap("./GUI/Images/mercedes_w.png.avif")
        self.ui.lbl_MercedesLogo.setPixmap(
            mercedes.scaled(
                self.ui.lbl_MercedesLogo.width(),
                self.ui.lbl_MercedesLogo.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

        ############################
        # Set up Feature Explanation
        ############################
        fi_exp_figure = Figure(figsize=(5, 3))
        self.__fi_exp_canvas = FigureCanvas(fi_exp_figure)
        self.ui.fe_layout.addWidget(self.__fi_exp_canvas)

        # Create subplot with position (0,0,1,1) to fill the entire figure
        self.__fi_exp_ax = fi_exp_figure.add_subplot(
            111, position=[0.1, 0.08, 0.8, 0.9]
        )
        self.__fi_exp_ax.tick_params(
            axis="both",
            colors=Colours.LIGHT_TEXT_COLOUR,
            which="major",
            labelsize=plotting.TICK_SIZE,
        )
        self.__fi_exp_ax.set_xlabel("Absolute SHAP Value", fontsize=plotting.TITLE_SIZE)
        self.__fi_exp_ax.margins(0)
        fi_exp_figure.set_facecolor(background_colour)
        self.__fi_exp_ax.set_facecolor(background_colour)
        plotting.set_ax_colours(self.__fi_exp_ax, text_colour)
        self.__fi_exp_barh = self.__fi_exp_ax.barh(
            DEFAULT_BARH_KEYS,
            DEFAULT_BARH_VALUES,
            color="white",
        )

        ############################
        # Set up Decision Tree
        ############################
        dt_figure = Figure(figsize=(5, 3))
        self.__dt_canvas = FigureCanvas(dt_figure)
        self.ui.dt_layout.addWidget(self.__dt_canvas)

        # Create subplot with position (0,0,1,1) to fill the entire figure
        self.__dt_ax = dt_figure.add_subplot(111, position=[0, 0, 1, 1])
        self.__dt_ax.tick_params(left=False, bottom=False)
        self.__dt_ax.get_yaxis().set_visible(False)
        self.__dt_ax.get_xaxis().set_visible(False)
        dt_figure.set_facecolor(background_colour)
        self.__dt_ax.margins(0)

        ############################
        # Set up Counterfactual
        ############################
        cf_figure = Figure(figsize=(5, 3))
        self.__cf_canvas = FigureCanvas(cf_figure)
        self.ui.cf_layout.addWidget(self.__cf_canvas)
        self.__cf_ax = cf_figure.add_subplot(111, position=[0.25, 0, 0.75, 0.9])
        self.__cf_ax.get_xaxis().set_visible(False)
        cf_figure.set_facecolor(background_colour)
        self.__cf_ax.margins(0)

        ###########################
        # Set up Race Plot
        ###########################
        rp_figure = Figure(figsize=(5, 3))
        self.__rp_canvas = FigureCanvas(rp_figure)
        self.ui.rp_layout.addWidget(self.__rp_canvas)
        self.__rp_ax = rp_figure.add_subplot(111, position=[0.05, 0.07, 0.8, 0.93])
        rp_figure.set_facecolor(background_colour)
        self.__rp_ax.margins(0)

        ###########################
        # Edit test results table
        ###########################
        # Set columns of table to evenly spread across width
        header = self.ui.table_TestResults.horizontalHeader()
        header.setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )  # Test Run
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Model Name
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Track
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Year
        header.setSectionResizeMode(
            4, QHeaderView.ResizeMode.Stretch
        )  # Finishing Position
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  # Tyre Strategy

        ###########################
        # Set up the tyre strategies figure
        ###########################
        ts_figure = Figure(figsize=(5, 3))
        self.__ts_canvas = FigureCanvas(ts_figure)
        self.ui.ts_layout.addWidget(self.__ts_canvas)
        self.__ts_ax = ts_figure.add_subplot(111, position=[0.07, 0.1, 0.8, 0.85])
        ts_figure.set_facecolor(background_colour)
        self.__ts_ax.margins(0)

        ###########################
        # Set up finishing position distribution plot
        ###########################
        fpd_figure = Figure(figsize=(4, 3))
        self.__fpd_canvas = FigureCanvas(fpd_figure)
        self.ui.fpd_layout.addWidget(self.__fpd_canvas)
        self.__fpd_ax = fpd_figure.add_subplot(111, position=[0.12, 0.12, 0.9, 0.9])
        fpd_figure.set_facecolor(background_colour)
        self.__fpd_ax.margins(0)

        # Set filter options
        name_filters = ["All"]
        models = self.__all_test_results["Model Name"].unique().tolist()
        models.sort()
        name_filters.extend(models)
        self.ui.cb_NameFilter.addItems(name_filters)
        track_filters = ["All"]
        track_filters.extend(self.__all_test_results["Track"].unique().tolist())
        self.ui.cb_TrackFilter.addItems(track_filters)
        year_filters = ["All"]
        sorted_string_years = [
            str(y) for y in sorted(self.__all_test_results["Year"].unique().tolist())
        ]
        year_filters.extend(sorted_string_years)
        self.ui.cb_YearFilter.addItems(year_filters)
        self.update_test_results_filters()

        ###########################
        # Connect signals and slots
        ###########################

        # Start stop button
        self.ui.btn_StartStop.clicked.connect(self.start_stop)

        # Load model for deployment
        self.ui.btn_LoadModel.clicked.connect(self.load_model)

        # Start training button
        self.ui.btn_StartTraining.clicked.connect(self.start_training)

        # Save trained model
        self.ui.btn_SaveModel.clicked.connect(self.save_model)

        # Update counterfactual on desired action box change
        self.ui.box_CFNoPit.stateChanged.connect(self.submit_counterfactual)
        self.ui.box_CFPitSoft.stateChanged.connect(self.submit_counterfactual)
        self.ui.box_CFPitMedium.stateChanged.connect(self.submit_counterfactual)
        self.ui.box_CFPitHard.stateChanged.connect(self.submit_counterfactual)

        # Select next counterfactual
        self.ui.btn_CFCandidateLess.clicked.connect(self.less_counterfactual)
        self.ui.btn_CFCandidateMore.clicked.connect(self.more_counterfactual)

        # Mercedes Race Simulation buttons
        self.ui.btn_ResetSimulation.clicked.connect(self.reset_simulation)
        self.ui.btn_StepModel.clicked.connect(self.step_model)
        self.ui.btn_StepDecisionTree.clicked.connect(self.step_decision_tree)
        self.ui.btn_NoPit.clicked.connect(self.step_no_pit)
        self.ui.btn_PitSoft.clicked.connect(self.step_pit_soft)
        self.ui.btn_PitMedium.clicked.connect(self.step_pit_medium)
        self.ui.btn_PitHard.clicked.connect(self.step_pit_hard)

        # Data source changer
        self.ui.cb_DataSource.currentIndexChanged.connect(self.change_data_source)

        # Deploy tab change
        self.ui.tabW_Deploy.currentChanged.connect(self.deploy_tab_changed)

        # Submit test results filters
        self.ui.sb_TestRunFilter.valueChanged.connect(self.update_test_results_filters)
        self.ui.cb_NameFilter.currentIndexChanged.connect(
            self.update_test_results_filters
        )
        self.ui.cb_TrackFilter.currentIndexChanged.connect(
            self.update_test_results_filters
        )
        self.ui.cb_YearFilter.currentIndexChanged.connect(
            self.update_test_results_filters
        )
        self.ui.sb_FinishingPositionFilter.valueChanged.connect(
            self.update_test_results_filters
        )
        self.ui.le_TyreStrategy.returnPressed.connect(self.update_test_results_filters)
        self.ui.btn_ReloadDataset.clicked.connect(self.reload_test_results_dataset)
        self.ui.cb_TyreStrategyTrack.currentIndexChanged.connect(
            self.update_tyre_strategies_plot
        )
        self.ui.sb_NumPlotTyreStrategies.valueChanged.connect(
            self.update_tyre_strategies_plot
        )

    def change_data_source(self):
        mode = self.ui.cb_DataSource.currentIndex()
        if mode == 1:  # On the Race Simulator
            self.ui.btn_StartStop.setDisabled(True)
            self.ui.le_IPAddress.setDisabled(True)
            self.ui.sb_Port.setDisabled(True)
            self.ui.btn_StepModel.setEnabled(True)
            self.ui.btn_StepDecisionTree.setEnabled(True)
            self.ui.btn_NoPit.setEnabled(True)
            self.ui.btn_PitSoft.setEnabled(True)
            self.ui.btn_PitMedium.setEnabled(True)
            self.ui.btn_PitHard.setEnabled(True)
            self.ui.btn_ResetSimulation.setEnabled(True)
            self.ui.cb_RaceSelect.setEnabled(True)
            self.ui.cb_YearSelect.setEnabled(True)
            self.ui.sb_Seed.setEnabled(True)
            if not self.__stopped_listening:
                self.start_stop()
        else:  # Any other mode
            self.__current_sim = None
            self.__current_sim_states = []
            self.__current_sim_actions = []
            self.ui.btn_StartStop.setEnabled(True)
            self.ui.le_IPAddress.setEnabled(True)
            self.ui.sb_Port.setEnabled(True)
            self.ui.btn_StepModel.setDisabled(True)
            self.ui.btn_StepDecisionTree.setDisabled(True)
            self.ui.btn_NoPit.setDisabled(True)
            self.ui.btn_PitSoft.setDisabled(True)
            self.ui.btn_PitMedium.setDisabled(True)
            self.ui.btn_PitHard.setDisabled(True)
            self.ui.btn_ResetSimulation.setDisabled(True)
            self.ui.cb_RaceSelect.setDisabled(True)
            self.ui.cb_YearSelect.setDisabled(True)
            self.ui.sb_Seed.setDisabled(True)

    ############################################################################
    # Model Deployment
    ############################################################################
    def deploy_tab_changed(self, tab_index):
        # Replot feature importance
        if tab_index == 0:
            self.plot_feature_importance(
                self.__last_state,
                SimpleRaceStrategy.NO_PIT,
                self.__fi_exp,
            )
        # Replot decision tree
        elif tab_index == 1:
            self.plot_decision_tree(self.__last_state)
        # Replot counterfactual
        elif tab_index == 2:
            self.plot_counterfactual()
        # Replot race plot
        elif tab_index == 3:
            self.plot_race_plot()

    def reset_simulation(self):
        seed = (
            np.random.randint(0, 1_000_000)
            if self.ui.sb_Seed.value() == 0
            else self.ui.sb_Seed.value()
        )
        self.__current_sim = MercedesRSTranslator(
            selected_driver=self.__loaded_model.selected_driver,
            seed=seed,
            allowed_years=[self.ui.cb_YearSelect.currentText()],
            allowed_tracks=[
                Track[self.ui.cb_RaceSelect.currentText().upper().replace(" ", "_")]
            ],
        )
        self.__current_sim_states = []
        self.__current_sim_actions = []

        # Reset hidden state for the recurrent models
        if isinstance(self.__loaded_model, DRQNModel):
            self.__loaded_model.reset_h()

        self.__current_track_details, state = (
            self.__current_sim.initialise_random_simulation()
        )
        self.__next_model_action = self.__loaded_model.predict(state)
        self.state_updated(state, self.__next_model_action, DEFAULT_FI_EXP)
        self.submit_counterfactual()

    def step_model(self):
        if self.__loaded_model is not None:
            self.__step_simulation(self.__next_model_action)
            self.__next_model_action = self.__loaded_model.predict(self.__last_state)
            self.ui.lbl_ModelPrediction.setText(f"{self.__next_model_action}")
        self.submit_counterfactual()

    def step_decision_tree(self):
        if self.__loaded_model is not None:
            # Let model step forward (for hidden state)
            self.__loaded_model.predict(self.__last_state)
            if self.__loaded_model.has_decision_tree():
                self.__step_simulation(
                    self.__loaded_model.predict_decision_tree(self.__last_state)
                )
        self.submit_counterfactual()

    def step_no_pit(self):
        # Let model step forward (for hidden state)
        if self.__loaded_model is not None:
            self.__loaded_model.predict(self.__last_state)
        self.__step_simulation(SimpleRaceStrategy.NO_PIT)
        self.submit_counterfactual()

    def step_pit_soft(self):
        # Let model step forward (for hidden state)
        if self.__loaded_model is not None:
            self.__loaded_model.predict(self.__last_state)
        self.__step_simulation(SimpleRaceStrategy.PIT_SOFT)
        self.submit_counterfactual()

    def step_pit_medium(self):
        # Let model step forward (for hidden state)
        if self.__loaded_model is not None:
            self.__loaded_model.predict(self.__last_state)
        self.__step_simulation(SimpleRaceStrategy.PIT_MEDIUM)
        self.submit_counterfactual()

    def step_pit_hard(self):
        # Let model step forward (for hidden state)
        if self.__loaded_model is not None:
            self.__loaded_model.predict(self.__last_state)
        self.__step_simulation(SimpleRaceStrategy.PIT_HARD)
        self.submit_counterfactual()

    def __step_simulation(self, action: SimpleRaceStrategy):
        if self.__current_sim is not None:
            state = self.__current_sim.step(strategy=action)
            self.__current_sim_states.append(state)
            self.__current_sim_actions.append(action)
            self.state_updated(state, action, DEFAULT_FI_EXP)

    def start_stop(self):
        # Start Listening
        if self.__stopped_listening:
            self.__stopped_listening = False
            self.ui.btn_StartStop.setText("Stop")
            self.ui.lbl_RunStatus.setText("Running")

            mode = self.ui.cb_DataSource.currentText()
            if mode == "F1 23":
                # Start thread to listen to the data
                self.__listener_thread = F123ListenerThread(
                    udp_ip=self.ui.le_IPAddress.text(),
                    udp_port=int(self.ui.sb_Port.value()),
                    loaded_model=self.__loaded_model,
                    race_plot_ax=self.__rp_ax,
                )
                self.__listener_thread.state_updated.connect(self.state_updated)
                self.__listener_thread.start()

        # Stop Listening
        else:
            self.__stopped_listening = True
            self.ui.btn_StartStop.setText("Start")
            self.ui.lbl_RunStatus.setText("Stopped")
            self.__listener_thread.stop_listening()

    def submit_counterfactual(self):
        if self.ui.tabW_Deploy.currentIndex() != 2:
            return

        self.__cf_index = 0
        self.plot_counterfactual()
        self.ui.btn_CFCandidateLess.setDisabled(True)
        self.ui.btn_CFCandidateMore.setEnabled(self.__cf_total > 1)

    def less_counterfactual(self):
        self.__cf_index -= 1
        self.plot_counterfactual()
        self.ui.btn_CFCandidateLess.setDisabled(self.__cf_index == 0)
        self.ui.btn_CFCandidateMore.setEnabled(True)

    def more_counterfactual(self):
        self.__cf_index += 1
        self.plot_counterfactual()
        self.ui.btn_CFCandidateLess.setEnabled(True)
        self.ui.btn_CFCandidateMore.setDisabled(self.__cf_index == self.__cf_total - 1)

    def plot_counterfactual(self):
        # Clear the axis
        self.__cf_ax.clear()

        # Add desired actions from the user
        desired_actions = []
        if self.ui.box_CFNoPit.isChecked():
            desired_actions.append(SimpleRaceStrategy.NO_PIT)
        if self.ui.box_CFPitSoft.isChecked():
            desired_actions.append(SimpleRaceStrategy.PIT_SOFT)
        if self.ui.box_CFPitMedium.isChecked():
            desired_actions.append(SimpleRaceStrategy.PIT_MEDIUM)
        if self.ui.box_CFPitHard.isChecked():
            desired_actions.append(SimpleRaceStrategy.PIT_HARD)
        if desired_actions == []:
            desired_actions = None

        # If there is no model loaded, or the model does not have a decision tree trained, return
        if self.__loaded_model is None or not self.__loaded_model.has_decision_tree():
            return

        closest_action, score, num_dbs = self.__loaded_model.plot_counterfactual(
            index=self.__cf_index,
            state=self.__last_state,
            desired_actions=desired_actions,
            ax=self.__cf_ax,
            dark_mode=DARK_MODE,
        )

        cf_text, _ = self.__loaded_model.get_counterfactual(
            index=self.__cf_index,
            state=self.__last_state,
            desired_actions=desired_actions,
            track_details=self.__current_track_details,
        )

        # Set the text edit box
        self.ui.te_CFRequiredChanges.setPlainText(cf_text)

        # Set the number of counterfactuals
        self.__cf_total = num_dbs

        # Set the score for the CF
        self.ui.lbl_CFDistance.setText(f"{score:.3f}")

        # Make the CF box text red
        if closest_action is None:
            self.ui.box_CFNoPit.setStyleSheet(f"color: {Colours.LIGHT_TEXT_COLOUR}")
            self.ui.box_CFPitSoft.setStyleSheet(f"color: {Colours.LIGHT_TEXT_COLOUR}")
            self.ui.box_CFPitMedium.setStyleSheet(f"color: {Colours.LIGHT_TEXT_COLOUR}")
            self.ui.box_CFPitHard.setStyleSheet(f"color: {Colours.LIGHT_TEXT_COLOUR}")
        else:
            if closest_action == SimpleRaceStrategy.NO_PIT:
                self.ui.box_CFNoPit.setStyleSheet(f"color: {Colours.TERTIARY_COLOUR}")
                self.ui.box_CFPitSoft.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
                self.ui.box_CFPitMedium.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
                self.ui.box_CFPitHard.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
            elif closest_action == SimpleRaceStrategy.PIT_SOFT:
                self.ui.box_CFNoPit.setStyleSheet(f"color: {Colours.LIGHT_TEXT_COLOUR}")
                self.ui.box_CFPitSoft.setStyleSheet(f"color: {Colours.TERTIARY_COLOUR}")
                self.ui.box_CFPitMedium.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
                self.ui.box_CFPitHard.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
            elif closest_action == SimpleRaceStrategy.PIT_MEDIUM:
                self.ui.box_CFNoPit.setStyleSheet(f"color: {Colours.LIGHT_TEXT_COLOUR}")
                self.ui.box_CFPitSoft.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
                self.ui.box_CFPitMedium.setStyleSheet(
                    f"color: {Colours.TERTIARY_COLOUR}"
                )
                self.ui.box_CFPitHard.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
            elif closest_action == SimpleRaceStrategy.PIT_HARD:
                self.ui.box_CFNoPit.setStyleSheet(f"color: {Colours.LIGHT_TEXT_COLOUR}")
                self.ui.box_CFPitSoft.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
                self.ui.box_CFPitMedium.setStyleSheet(
                    f"color: {Colours.LIGHT_TEXT_COLOUR}"
                )
                self.ui.box_CFPitHard.setStyleSheet(f"color: {Colours.TERTIARY_COLOUR}")

        self.__cf_ax.figure.canvas.draw()

    def plot_feature_importance(self, state, prediction, fi_exp):
        # Create a new matplotlib figure
        if isinstance(self.__loaded_model, DRQNModel):
            vals_for_pred = fi_exp["shap_values"]
        else:
            vals_for_pred = fi_exp["shap_values"][prediction.value][0]

        # Find enum importances
        tyre_importance = vals_for_pred[
            fi_exp["feature_names"].index(state.current_tyre.name.title())
        ]
        sc_importance = vals_for_pred[
            fi_exp["feature_names"].index(
                state.safety_car.name.replace("_", " ").title()
            )
        ]

        vals = {
            "Last Lap": abs(
                vals_for_pred[fi_exp["feature_names"].index("Last Lap To Reference")]
            ),
            "Gap To Leader": abs(
                vals_for_pred[fi_exp["feature_names"].index("Scaled Gap To Leader")]
            ),
            "Gap Behind": abs(
                vals_for_pred[fi_exp["feature_names"].index("Scaled Gap Behind")]
            ),
            "Gap Ahead": abs(
                vals_for_pred[fi_exp["feature_names"].index("Scaled Gap Ahead")]
            ),
            "Tyre Degradation": abs(
                vals_for_pred[fi_exp["feature_names"].index("Scaled Tyre Degradation")]
            ),
            "Current Tyre": abs(tyre_importance),
            "Lap Number": abs(
                vals_for_pred[fi_exp["feature_names"].index("Race Progress")]
            ),
            "Safety Car": abs(sc_importance),
            "Position": abs(
                vals_for_pred[fi_exp["feature_names"].index("Scaled Position")]
            ),
        }

        for i, (_, value) in enumerate(vals.items()):
            self.__fi_exp_barh[i].set_width(value)

        self.__fi_exp_ax.set_xlim(0, max(vals.values()))
        self.__fi_exp_ax.figure.canvas.draw()

    def plot_decision_tree(self, state):
        if self.__loaded_model is not None and self.__loaded_model.has_decision_tree():
            self.ui.te_DecisionPath.clear()
            self.ui.te_DecisionPath.setPlainText(
                self.__loaded_model.get_decision_path(state)
            )

    def plot_race_plot(self):
        if self.__current_sim is not None:
            self.__rp_ax.clear()
            self.__current_sim.plot_live_race(
                ax=self.__rp_ax,
                dark_mode=DARK_MODE,
            )
            self.__rp_ax.figure.canvas.draw()

    def state_updated(self, state: UnifiedRaceState, prediction, fi_exp):
        self.__last_state = state

        if state.terminal:
            self.__current_sim.plot_race()

        # If the current tab is not the deployment tab, return
        if self.ui.tabW_TrainDeploy.currentIndex() == 0:
            return

        ############
        # Update GUI
        ############
        self.ui.lbl_ModelPrediction.setText(f"{prediction}")
        if self.__loaded_model is not None and self.__loaded_model.has_decision_tree():
            self.ui.lbl_DTPrediction.setText(
                f"{self.__loaded_model.predict_decision_tree(state)}"
            )
        self.ui.lbl_StatePosition.setText(f"P{state.position}")
        self.ui.lbl_StateSafetyCarStatus.setText(f"{state.safety_car}")
        self.ui.lbl_StateLapNumber.setText(f"L{int(state.partial_lap_number)}")
        self.ui.lbl_StateCurrentTyre.setText(f"{state.current_tyre}")
        self.ui.lbl_StateTyreDegradation.setText(f"{state.tyre_degradation:.2f}")
        self.ui.lbl_StateGapBehind.setText(f"+{state.gap_behind:.3f}")
        self.ui.lbl_StateGapAhead.setText(f"-{state.gap_ahead:.3f}")
        self.ui.lbl_StateGapToLeader.setText(f">{state.gap_to_leader:.3f}")
        self.ui.lbl_StateLastLap.setText(f"{state.last_lap_time:.3f}")

        ####################
        # Feature Importance
        ####################
        # If the current tab is the feature importance tab
        if self.ui.tabW_Deploy.currentIndex() == 0:
            # Plot feature importance only if we are using the race simulator
            if self.ui.cb_DataSource.currentText() == "Race Simulator":
                if isinstance(self.__loaded_model, DRQNModel):
                    try:
                        self.__fi_exp = self.__loaded_model.explain_feature_importance(
                            self.__current_sim_states,
                            self.__current_sim_actions,
                        )
                    except Exception as e:
                        print(e)
                        self.__fi_exp = DEFAULT_FI_EXP
                else:
                    self.__fi_exp = self.__loaded_model.explain_feature_importance(
                        state
                    )
                self.plot_feature_importance(state, prediction, self.__fi_exp)
            else:
                pass  # TODO: deal with feature importance for other data sources
                # self.plot_feature_importance(state, prediction, fi_exp)

        ################
        # Decision Tree
        ################
        # If the current tab is the decision tree tab
        if self.ui.tabW_Deploy.currentIndex() == 1:
            self.plot_decision_tree(state)

        ################
        # Race Plot
        ################
        # If the current tab is the race plot tab
        if self.ui.tabW_Deploy.currentIndex() == 3:
            self.plot_race_plot()

    def load_model(self):
        model_path, _ = QFileDialog.getOpenFileName(
            self, "Load Model", "~/Saved Models", "Models (*.pth)"
        )
        if model_path == "":
            return

        self.__loaded_model = StrategyRLModel.load_model(model_path)

        self.ui.lbl_LoadedModel.setText(self.__loaded_model.name)

        ####################
        # Enable decision tree prediction if there is a decision tree
        ####################
        if self.__loaded_model.has_decision_tree():
            self.ui.btn_StepDecisionTree.setEnabled(True)
            self.ui.lbl_DTPrediction.setEnabled(True)
            self.ui.lbl_DTPredTitle.setEnabled(True)
        else:
            self.ui.btn_StepDecisionTree.setDisabled(True)
            self.ui.lbl_DTPrediction.setDisabled(True)
            self.ui.lbl_DTPredTitle.setDisabled(True)

        ####################
        # Reset visualisations from previous model
        ####################

        # Decision Tree
        self.__dt_ax.clear()
        self.__loaded_model.plot_decision_tree(
            ax=self.__dt_ax,
            dark_mode=DARK_MODE,
        )
        self.__dt_ax.figure.canvas.draw()
        self.ui.te_DecisionPath.clear()

        # Feature Importance
        for i in range(len(self.__fi_exp_barh)):
            self.__fi_exp_barh[i].set_width(0)
        self.__fi_exp_ax.figure.canvas.draw()

    ############################################################################
    # Model Training
    ############################################################################
    def start_training(self):
        self.ui.btn_StartTraining.setDisabled(True)

        model_parameters = {}

        sd = self.ui.cb_SelectedDriver.currentText()
        if sd == "Lewis Hamilton":
            model_parameters["selected_driver"] = 44
        elif sd == "George Russell":
            model_parameters["selected_driver"] = 63

        if self.ui.le_ModelName.text():
            model_parameters["name"] = self.ui.le_ModelName.text()
        model_parameters["num_episodes"] = int(self.ui.dsb_NumEpisodes.value())
        model_parameters["seed"] = int(self.ui.dsb_Seed.value())
        model_parameters["fixed_seed"] = self.ui.box_FixedSeed.isChecked
        model_parameters["simulation_step_size"] = self.ui.dsb_StepSize.value()
        model_parameters["disable_safety_car"] = self.ui.box_DisableSC.isChecked
        model_parameters["allowed_years"] = ["2023"]
        model_parameters["allowed_tracks"] = [Track.BAHRAIN]
        model_parameters["reward_function"] = thomas_reward_2
        model_parameters["verbose"] = True
        model_parameters["epsilon"] = self.ui.dsb_Epsilon.value()
        model_parameters["epsilon_decay"] = self.ui.dsb_EpsilonDecay.value()
        model_parameters["min_epsilon"] = self.ui.dsb_MinEpsilon.value()
        model_parameters["gamma"] = self.ui.dsb_Gamma.value()
        model_parameters["learning_rate"] = self.ui.dsb_LearningRate.value()
        model_parameters["weight_decay"] = self.ui.dsb_WeightDecay.value()
        model_parameters["replay_buffer_size"] = int(
            self.ui.dsb_ReplayBufferSize.value()
        )
        model_parameters["replay_buffer_sample_size"] = int(
            self.ui.dsb_ReplayBufferSampleSize.value()
        )
        model_parameters["episodes_to_update_target"] = int(
            self.ui.dsb_EpisodesUpdateTargetNetwork.value()
        )
        model_parameters["optimiser_type"] = torch.optim.Adam

        self.__model_trainer_thread = ModelTrainerThread(model_parameters)
        self.__model_trainer_thread.trained_model.connect(self.training_complete)
        self.__model_trainer_thread.console_updated.connect(self.console_updated)
        self.__model_trainer_thread.start()

    def console_updated(self, new_line: str):
        self.__console_history.append(new_line)
        self.ui.te_ConsoleLog.setPlainText("\n".join(self.__console_history))
        self.ui.te_ConsoleLog.scrollToAnchor("end")

    def training_complete(self, model: DQNModel):
        self.__trained_model = model
        self.ui.btn_StartTraining.setEnabled(True)

    def save_model(self):
        model_path, _ = QFileDialog.getSaveFileName(
            self, "Save Model", "", "Models (*.pth)"
        )

        if self.__trained_model is not None:
            self.__trained_model.save_model(model_path)
        else:
            QMessageBox.warning(self, "Error", "No trained model available to save.")

    ############################################################################
    # Test Results
    ############################################################################
    def __filter_tyre_strategy(
        self,
        tr: pd.DataFrame,
        tyre_strategy: str,
    ) -> pd.DataFrame:
        # Parse the tyre strategy
        # =x represents equal to x pitstops
        # >x represents more than x pitstops
        # <x represents less than x pitstops
        # _ represents any pit lap
        # [a, b] represents a to b pit laps
        # S represents soft tyre
        # M represents medium tyre
        # H represents hard tyre
        # X represents any tyre

        def has_pitstop_in_range(tyre_strategy, tyre, min_lap, max_lap):
            if tyre == "X":
                pattern = re.compile(r"\D(\d+)\D")
            else:
                pattern = re.compile(tyre + r"(\d+)")
            matches = pattern.findall(tyre_strategy)

            for match in matches:
                lap_number = int(match)
                if min_lap <= lap_number <= max_lap:
                    return True
            return False

        # Split the tyre strategy into individual pit laps
        tyres_and_laps = tyre_strategy.split(" ")
        for tl in tyres_and_laps:
            tyre = tl[0]
            lap = tl[1:]

            # Filter the number of pitstops
            if tyre == "=":
                tr = tr[tr["Tyre Strategy"].str.len() == 3 * (int(lap) + 1)]
            elif tyre == ">":
                tr = tr[tr["Tyre Strategy"].str.len() > 3 * (int(lap) + 1)]
            elif tyre == "<":
                tr = tr[tr["Tyre Strategy"].str.len() < 3 * (int(lap) + 1)]

            # Filter the tyre type
            elif tyre in ["S", "M", "H", "X"]:
                # Filter wildcard tyre
                if tyre == "X":
                    if lap != "_":
                        tr = tr[tr["Tyre Strategy"].str.contains(f"{lap}")]

                # Filter specific tyre
                else:
                    # Filter wildcard lap
                    if lap == "_":
                        tr = tr[tr["Tyre Strategy"].str.contains(f"{tyre}")]

                    # Filter lap ranges
                    elif len(lap) > 1 and lap[0] == "[":
                        if lap[-1] == "]":
                            lap_range = lap[1:-1].split(",")
                            min_lap = int(lap_range[0])
                            max_lap = int(lap_range[1])
                            tr = tr[
                                tr["Tyre Strategy"].apply(
                                    lambda x: has_pitstop_in_range(
                                        x, tyre, min_lap, max_lap
                                    )
                                )
                            ]

                    # Filter specific lap
                    else:
                        tr = tr[tr["Tyre Strategy"].str.contains(f"{tyre}{lap}")]
        return tr

    def update_test_results_filters(self):
        ####################
        # Filter test results
        ####################
        tr = self.__all_test_results.copy()

        # Filter by test run
        test_run = self.ui.sb_TestRunFilter.value()
        if test_run != 0:
            tr = tr[tr["Test Run"] == test_run]

        # Filter by model name
        model_name = self.ui.cb_NameFilter.currentText()
        if model_name != "All":
            tr = tr[tr["Model Name"] == model_name]

        # Filter by track
        track = self.ui.cb_TrackFilter.currentText()
        if track != "All":
            tr = tr[tr["Track"] == track]

        # Filter by year
        year = self.ui.cb_YearFilter.currentText()
        if year != "All":
            tr = tr[tr["Year"] == int(year)]

        # Filter by finishing position
        finishing_position = self.ui.sb_FinishingPositionFilter.value()
        if finishing_position != 0:
            tr = tr[tr["Finishing Position"] == finishing_position]

        # Filter by tyre strategy
        tyre_strategy = self.ui.le_TyreStrategy.text()
        if tyre_strategy:
            tr = self.__filter_tyre_strategy(tr, tyre_strategy)

        # Reindex the dataframe
        tr.reset_index(drop=True, inplace=True)

        # Update the tyre strategies track combobox
        self.ui.cb_TyreStrategyTrack.clear()
        self.ui.cb_TyreStrategyTrack.addItems(tr["Track"].unique().tolist())
        self.ui.cb_TyreStrategyTrack.setCurrentIndex(0)

        ####################
        # Report statistics
        ####################
        # Remove P21 failure finishes
        stats_tr = tr[tr["Finishing Position"] != 21]

        self.ui.lbl_StatsBestFinish.setText(f"{stats_tr['Finishing Position'].min()}")
        self.ui.lbl_StatsWorstFinish.setText(f"{stats_tr['Finishing Position'].max()}")
        self.ui.lbl_StatsMeanFinish.setText(
            f"{stats_tr['Finishing Position'].mean():.2f}"
        )
        try:
            self.ui.lbl_StatsModeFinish.setText(
                f"{stats_tr['Finishing Position'].mode()[0]}"
            )
        except (
            KeyError
        ):  # If all tests failed (no mode calculated) catch and handle error
            self.ui.lbl_StatsModeFinish.setText("nan")

        self.ui.lbl_StatsStdDev.setText(f"{stats_tr['Finishing Position'].std():.2f}")
        self.ui.lbl_StatsNumValidTests.setText(f"{len(stats_tr)}")
        self.ui.lbl_StatsTestFails.setText(f"{len(tr) - len(stats_tr)}")

        ####################
        # Report test results in table
        ####################
        # Clear table
        self.ui.table_TestResults.setRowCount(0)

        # For each row in tr, make a row in self.ui.table_TestResults
        for i, row in tr.iterrows():
            self.ui.table_TestResults.insertRow(i)
            self.ui.table_TestResults.setItem(
                i, 0, QTableWidgetItem(str(row["Test Run"]))
            )
            self.ui.table_TestResults.setItem(
                i, 1, QTableWidgetItem(str(row["Model Name"]))
            )
            self.ui.table_TestResults.setItem(i, 2, QTableWidgetItem(str(row["Track"])))
            self.ui.table_TestResults.setItem(i, 3, QTableWidgetItem(str(row["Year"])))
            self.ui.table_TestResults.setItem(
                i, 4, QTableWidgetItem(str(row["Finishing Position"]))
            )
            self.ui.table_TestResults.setItem(
                i, 5, QTableWidgetItem((row["Tyre Strategy"]))
            )

        ####################
        # Plot finishing position distribution
        ####################
        self.__fpd_ax.clear()
        plotting.plot_finishing_position_distribution(
            test_results=tr,
            ax=self.__fpd_ax,
            dark_mode=DARK_MODE,
        )
        self.__fpd_ax.figure.canvas.draw()

        self.__current_test_results = tr

        self.update_tyre_strategies_plot()

    def update_tyre_strategies_plot(self):
        tr = self.__current_test_results

        ####################
        # Plot tyre strategies
        ####################
        self.__ts_ax.clear()
        # Take track selected from cb_TyreStrategyTrack
        plot_tr = tr[tr["Track"] == self.ui.cb_TyreStrategyTrack.currentText()]
        plotting.plot_test_results_tyre_strategies(
            test_results=plot_tr,
            ax=self.__ts_ax,
            num_strategies=self.ui.sb_NumPlotTyreStrategies.value(),
            dark_mode=DARK_MODE,
        )
        self.__ts_ax.figure.canvas.draw()

    def reload_test_results_dataset(self):
        self.__all_test_results = pd.read_csv("test_model_results.csv")
        self.__all_test_results.fillna("", inplace=True)
        self.update_test_results_filters()

    ############################################################################
    # Overrides
    ############################################################################
    def closeEvent(self, event):
        if not self.__stopped_listening:
            self.start_stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = RL_Strategy_GUI()
    widget.show()
    sys.exit(app.exec())
