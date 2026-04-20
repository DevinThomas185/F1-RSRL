import random
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from Classes.Enums import Track, TyreCompound
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.Pitstop import Pitstop
from Classes.RaceStrategy.UnifiedRaceStrategy import UnifiedRaceStrategy
from Classes.ConsoleLogger import ConsoleLogger

from Models.StrategyRLModel import StrategyRLModel

pre_defined_strategies = {
    Track.BAHRAIN: [ 
        ["S", 14, 20, "H", 35, 42, "S"],
        ["S", 12, 17, "H", 31, 48, "H"],
        ["S", 20, 28, "H"],
        ["S", 15, 21, "M", 35, 42, "S"],
    ],
    Track.SAUDI_ARABIA: [
        ["M", 18, 25, "H"],
        ["S", 13, 20, "H"],
        ["H", 21, 35, "M"],
        ["M", 28, 36, "S"],
    ],
    Track.AUSTRALIA: [
        ["M", 14, 22, "H"],
        ["S", 9, 16, "H"],
        ["M", 11, 17, "H", 40, 48, "S"],
    ],
    Track.JAPAN: [
        ["S", 13, 19, "H", 31, 37, "H"],
        ["M", 14, 20, "H", 37, 43, "S"],
        ["S", 13, 19, "H", 36, 41, "S"],
        ["S", 18, 25, "H"],
    ],
    Track.MIAMI: [
        ["M", 13, 20, "H"],
        ["M", 11, 17, "H", 37, 43, "M"],
        ["M", 11, 17, "H", 41, 46, "S"],
    ],
    Track.EMILIA_ROMAGNA: [
        ["M", 21, 27, "H"],
        ["H", 34, 40, "M"],
        ["H", 41, 47, "S"],
    ],
    Track.MONACO: [
        ["M", 30, 38, "H"],
        ["S", 22, 30, "H"],
    ],
    Track.CANADA: [
        ["M", 16, 24, "H", 40, 48, "H"],
        ["H", 43, 50, "M"],
        ["M", 20, 30, "H"],
        ["M", 16, 24, "H", 43, 50, "M"],
    ],
    Track.SPAIN: [
        ["S", 13, 18, "H", 37, 43, "H"],
        ["S", 15, 20, "H", 46, 51, "S"],
        ["S", 10, 15, "H", 31, 36, "S", 48, 54, "S"],
        ["S", 15, 20, "H", 40, 46, "M"],
    ],
    Track.AUSTRIA: [
        ["M", 18, 26, "H", 45, 51, "M"],
        ["M", 15, 23, "H", 40, 48, "H"],
        ["M", 27, 37, "H"],
    ],
    Track.UK: [
        ["S", 11, 17, "M", 33, 40, "S"],
        ["M", 21, 27, "H"],
        ["M", 14, 20, "H", 35, 42, "S"],
        ["H", 33, 41, "S"],
    ],
    Track.HUNGARY: [
        ["M", 17, 24, "H", 42, 48, "H"],
        ["M", 18, 25, "H", 45, 52, "M"],
        ["M", 18, 25, "M", 39, 47, "H"],
        ["M", 13, 19, "H", 32, 39, "H", 52, 58, "S"],
    ],
    Track.BELGIUM: [
        ["S", 10, 15, "M", 25, 30, "M"],
        ["S", 10, 15, "M", 28, 33, "S"],
        ["M", 14, 20, "H"],
        ["S", 12, 18, "H"],
    ],
    Track.NETHERLANDS: [
        ["S", 20, 25, "M", 48, 54, "S"],
        ["M", 30, 36, "H"],
        ["S", 18, 23, "H", 50, 56, "S"],
        ["M", 22, 29, "S", 45, 52, "S"],
    ],
    Track.ITALY: [
        ["M", 20, 26, "H"],
        ["S", 14, 20, "H"],
        ["S", 10, 15, "M", 30, 36, "M"],
    ],
    Track.AZERBAIJAN: [
        ["M", 13, 20, "H"],
        ["H", 33, 40, "M"],
        ["M", 8, 16, "H", 27, 35, "H"],
    ],
    Track.SINGAPORE: [
        ["M", 20, 30, "H"],
        ["S", 15, 25, "H"],
        ["S", 13, 18, "H", 40, 46, "S"],
    ],
    Track.USA: [
        ["M", 14, 19, "H", 35, 42, "M"],
        ["M", 12, 17, "H", 30, 38, "H"],
        ["M", 14, 19, "H", 40, 46, "S"],
        ["M", 20, 26, "H"],
    ],
    Track.MEXICO: [
        ["M", 27, 34, "H"],
        ["M", 17, 23, "H", 45, 51, "M"],
        ["H", 50, 56, "S"],
    ],
    Track.BRAZIL: [
        ["S", 17, 23, "M", 46, 52, "S"],
        ["M", 20, 26, "M", 48, 54, "S"],
        ["S", 13, 18, "M", 33, 40, "S", 50, 56, "S"],
        ["M", 25, 32, "H"],
    ],
    Track.LAS_VEGAS: [
        ["M", 10, 15, "H", 29, 34, "H"],
        ["M", 18, 24, "H"],
        ["M", 12, 17, "H", 32, 37, "M"],
        ["M", 12, 17, "H", 35, 40, "S"],
    ],
    Track.QATAR: [
        ["M", 16, 23, "H", 37, 42, "M"],
        ["S", 13, 18, "M", 34, 39, "M"],
        ["S", 13, 18, "H", 36, 41, "M"],
    ],
    Track.ABU_DHABI: [
        ["M", 20, 26, "H"],
        ["M", 12, 18, "H", 33, 39, "H"],
        ["S", 12, 18, "H"],
    ],
}


class FixedStrategyModel(StrategyRLModel):
    __slots__ = [
        "__fixed_strategies",
        "__current_strategy",
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
    def generate_random_strategy(
        self,
        track: Track,
    ) -> None:
        if track not in self.__fixed_strategies:
            raise ValueError(f"Track {track} does not have a fixed strategy")
        
        chosen_strategy = random.choice(self.__fixed_strategies[track])

        strategy = UnifiedRaceStrategy()
        strategy.set_starting_tyre(TyreCompound.convert(chosen_strategy[0]))
        for i in range(1, len(chosen_strategy), 3):
            pit_lap = np.random.randint(chosen_strategy[i], chosen_strategy[i + 1] + 1)
            strategy.add_pitstop(
                Pitstop(
                    tyre_compound=TyreCompound.convert(chosen_strategy[i + 2]),
                    lap_number=pit_lap,
                )
            )

        self.__current_strategy = strategy

    def predict(
        self,
        state: UnifiedRaceState,
    ) -> UnifiedRaceStrategy:
        return self.__current_strategy
     
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
