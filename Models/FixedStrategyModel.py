import numpy as np
from sklearn.tree import DecisionTreeClassifier
from Classes.Enums import Track
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.UnifiedRaceStrategy import UnifiedRaceStrategy
from Classes.ConsoleLogger import ConsoleLogger

from Models.StrategyRLModel import StrategyRLModel

pre_defined_strategies = {
    Track.BAHRAIN: ["S", 13, "H", 37, "S"],
    Track.SAUDI_ARABIA: ["M", 19, "H"],
    Track.AUSTRALIA: ["M", 17, "H", 36, "H"],
    Track.JAPAN: ["S", 12, "H", 32, "H"],
    Track.MIAMI: ["M", 18, "H"],
    Track.EMILIA_ROMAGNA: ["M", 24, "H"],
    Track.MONACO: ["S", 27, "H"],
    Track.CANADA: ["M", 20, "H", 44, "H"],
    Track.SPAIN: ["M", 22, "M", 48, "S"],
    Track.AUSTRIA: ["M", 21, "H", 47, "M"],
    Track.UK: ["S", 14, "M", 37, "S"],
    Track.HUNGARY: ["M", 21, "H", 45, "H"],
    Track.BELGIUM: ["S", 13, "M", 28, "M"],
    Track.NETHERLANDS: ["S", 22, "M", 51, "S"],
    Track.ITALY: ["S", 25, "M"],
    Track.AZERBAIJAN: ["M", 17, "H"],
    Track.SINGAPORE: ["M", 25, "H"],
    Track.USA: ["M", 16, "H", 39, "M"],
    Track.MEXICO: ["M", 30, "H"],
    Track.BRAZIL: ["S", 20, "M", 49, "S"],
    Track.LAS_VEGAS: ["M", 12, "H", 31, "H"],
    Track.QATAR: ["M", 14, "M", 28, "M", 42, "H"],
    Track.ABU_DHABI: ["M", 23, "H"],
}


class FixedStrategyModel(StrategyRLModel):
    __slots__ = [
        "__fixed_strategies",
    ]

    def __init__(
        self,
        selected_driver: int,
        name: str = "FixedStrategyModel",
        device: str = "cpu",
        decision_tree: DecisionTreeClassifier | None = None,
        logger: ConsoleLogger = ConsoleLogger(),
        number_of_episodes_trained: int = 0,
        fixed_strategies: dict[Track, list] = pre_defined_strategies,
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
        self.__fixed_strategies = fixed_strategies

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
        state: UnifiedRaceState,
    ) -> UnifiedRaceStrategy:
        if state.track not in self.__fixed_strategies:
            raise ValueError(f"Track {state.track} does not have a fixed strategy")

        return UnifiedRaceStrategy.to_strategy(self.__fixed_strategies[state.track])
    
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
