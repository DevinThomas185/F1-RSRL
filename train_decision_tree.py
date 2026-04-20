
import argparse
import sys
import numpy as np
import torch
import importlib

from Architectures.HPT_RecurrentQN import *
from Classes.Enums import Track
from Models.DQNModel import DQNModel
from Models.StrategyRLModel import StrategyRLModel
from RewardFunctions.RewardFunctions import thomas_reward_2


def __main(args):
    model = StrategyRLModel.load_model(args.model_path)
    model.set_model_simulation_parameters(
        disable_safety_car=args.disable_safety_car,
        allowed_years=args.years,
        allowed_tracks=[Track[track] for track in args.tracks],
        reward_function=thomas_reward_2,
    )

    model.train_viper(
        max_depth=args.max_depth,
        max_iters=args.max_iterations,
        max_samples=args.max_samples,
        is_reweight=args.reweight_samples,
        n_batch_rollouts=args.batch_rollouts,
        n_test_rollouts=args.test_rollouts,
        verbose=args.verbose,
    )

    model.name = model.name + "_DecisionTreeModel"
    model.save_model(f"Saved Models/DecisionTreeModels/{model.name}")

    return 0


# TODO: Make help more helpful
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--model_path",
        type=str,
        help="Model path",
        required=True,
    )

    parser.add_argument(
        "--disable_safety_car",
        action="store_true",
        default=False,
        help="Whether to disable the safety car in simulations",
    )

    parser.add_argument(
        "--years",
        nargs="*",
        default=[],
        help="List of years to allow",
    )

    parser.add_argument(
        "--tracks",
        nargs="*",
        default=[],
        help="List of tracks to allow",
    )

    parser.add_argument(
        "--max_depth",
        type=int,
        default=10,
        help="Maximum Tree Depth",
    )

    parser.add_argument(
        "--max_iterations",
        type=int,
        default=20,
        help="Maximum number of student iterations",
    )

    parser.add_argument(
        "--max_samples",
        type=int,
        default=1000,
        help="Maximum number of samples",
    )

    parser.add_argument(
        "--reweight_samples",
        action="store_true",
        default=False,
        help="Whether to reweight samples",
    )

    parser.add_argument(
        "--batch_rollouts",
        type=int,
        default=10,
        help="Number of batch rollouts",
    )

    parser.add_argument(
        "--test_rollouts",
        type=int,
        default=2,
        help="Number of test rollouts",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Verbose mode",
    )

    args = parser.parse_args()

    sys.exit(__main(args))
