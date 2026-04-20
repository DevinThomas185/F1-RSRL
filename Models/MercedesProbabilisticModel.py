import numpy as np
from sklearn.tree import DecisionTreeClassifier
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.BlankRaceStrategy import BlankRaceStrategy
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Classes.Enums import TyreCompound
from Classes.ConsoleLogger import ConsoleLogger

from Models.StrategyRLModel import StrategyRLModel


class MercedesProbabilisticModel(StrategyRLModel):
    def __init__(
        self,
        selected_driver: int,
        name: str = "MercedesProbabilisticModel",
        device: str = "cpu",
        decision_tree: DecisionTreeClassifier | None = None,
        logger: ConsoleLogger = ConsoleLogger(),
        number_of_episodes_trained: int = 0,
    ) -> None:
        super().__init__(
            selected_driver=selected_driver,
            name=name,
            device=device,
            decision_tree=decision_tree,
            logger=logger,
            number_of_episodes_trained=number_of_episodes_trained,
            is_recurrent=False,
            disable_safety_car=False,
            allowed_years=[],
            allowed_tracks=[],
            reward_function=None,
        )

    ############################################################################
    # Training Methods
    ############################################################################
    def train(
        self,
    ) -> None:
        pass

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
        _: UnifiedRaceState,
    ) -> BlankRaceStrategy:
        return BlankRaceStrategy()

    def predict_q_values(
        self,
        state: UnifiedRaceState,
    ) -> np.ndarray:
        pass

    ############################################################################
    # Model Saving and Loading
    ############################################################################
    def save_model(
        self,
        _: str = "Saved Models/model",
    ) -> None:
        pass

    @staticmethod
    def infer_simple_race_strategy(
        state: UnifiedRaceState,
        next_state: UnifiedRaceState,
    ) -> SimpleRaceStrategy:
        if state.current_tyre == next_state.current_tyre:
            return SimpleRaceStrategy.NO_PIT

        if next_state.current_tyre == TyreCompound.SOFT:
            return SimpleRaceStrategy.PIT_SOFT

        if next_state.current_tyre == TyreCompound.MEDIUM:
            return SimpleRaceStrategy.PIT_MEDIUM

        if next_state.current_tyre == TyreCompound.HARD:
            return SimpleRaceStrategy.PIT_HARD

        return SimpleRaceStrategy.NO_PIT
