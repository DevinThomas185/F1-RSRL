import argparse
import sys

from Classes.Enums import Track
from ParallelModels.A3CModel import A3CModel
from RewardFunctions.RewardFunctions import simple_reward, thomas_reward_2


def __main(args):

    a3c_model = A3CModel(
        selected_driver=44,
        name=f"A3C HPT{args.experiment_number}",
        disable_safety_car=args.disable_safety_car,
        allowed_years=args.years,
        allowed_tracks=[Track[track] for track in args.tracks],
        reward_function=thomas_reward_2,
    )

    a3c_model.train(
        min_episodes=args.min_episodes,
        simulation_step_size=1,
        checkpointing_details={
            "checkpoint_directory": f"Saved Models/A3C HPT/A3C Experiment {args.experiment_number}",
            "checkpoint_frequency": 1000,
        },
        gamma=args.gamma,
        value_loss_coef=args.value_loss_coef,
        max_grad_norm=args.max_grad_norm,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        generate_plots=False,
    )

    a3c_model.save_model(f"Saved Models/A3C HPT/experiment_{args.experiment_number}")

    return 0


# TODO: Make help more helpful
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--experiment_number",
        type=int,
        help="Experiment Number",
        required=True,
    )

    parser.add_argument(
        "--min_episodes",
        type=int,
        default=100_000,
        help="Minimum Number of Episodes",
    )

    parser.add_argument(
        "--disable_safety_car",
        "-d",
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
        "--gamma",
        type=float,
        default=0.99,
        help="Gamma",
    )

    parser.add_argument(
        "--value_loss_coef",
        type=float,
        default=0.5,
        help="Value Loss Coefficient",
    )

    parser.add_argument(
        "--max_grad_norm",
        type=float,
        default=50,
        help="Maximal Gradient Norm",
    )

    parser.add_argument(
        "--learning_rate",
        type=float,
        default=0.001,
        help="Learning Rate",
    )

    parser.add_argument(
        "--weight_decay",
        type=float,
        default=0.001,
        help="Weight Decay",
    )

    args = parser.parse_args()

    sys.exit(__main(args))
