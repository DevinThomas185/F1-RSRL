import argparse
import sys
import numpy as np
import torch
import importlib

from Architectures.HPT_RecurrentQN import *
from Classes.Enums import Track
from Models.DDPGModel import DDPGModel
from RewardFunctions.RewardFunctions import thomas_reward_2


def __main(args):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    module = importlib.import_module("Architectures.HPT_ActorCritic")
    actor_architecture = getattr(module, f"HPT_{args.actor_architecture_id}_Actor")
    critic_architecture = getattr(module, f"HPT_{args.critic_architecture_id}_Critic")

    actor_network = actor_architecture()
    critic_network = critic_architecture()

    print(actor_network)
    print(critic_network)

    ddpg_model = DDPGModel(
        selected_driver=44,
        name=f"DDPG HPT{args.experiment_number}",
        device=device,
        actor_network=actor_network,
        critic_network=critic_network,
        disable_safety_car=args.disable_safety_car,
        allowed_years=args.years,
        allowed_tracks=[Track[track] for track in args.tracks],
        reward_function=thomas_reward_2,
    )

    ddpg_model.train(
        num_episodes=args.num_episodes,
        seed=args.seed,
        fixed_seed=args.fixed_seed,
        simulation_step_size=1,
        filter_invalid_actions=args.filter_invalid_actions,
        checkpointing_details={
            "checkpoint_directory": f"Saved Models/DDPG HPT/DDPG Experiment {args.experiment_number}",
            "checkpoint_frequency": 1000,
        },
        verbose=True,
        epsilon=args.epsilon,
        epsilon_decay=args.epsilon_decay,
        min_epsilon=args.min_epsilon,
        gamma=args.gamma,
        tau=args.tau,
        actor_learning_rate=args.actor_learning_rate,
        critic_learning_rate=args.critic_learning_rate,
        actor_weight_decay=args.actor_weight_decay,
        critic_weight_decay=args.critic_weight_decay,
        replay_buffer_size=args.replay_buffer_size,
        replay_buffer_sample_size=args.replay_buffer_sample_size,
        actor_optimiser_type=torch.optim.Adam,
        critic_optimiser_type=torch.optim.Adam,
        add_loss_noise=args.add_loss_noise,
        generate_plots=False,
    )

    ddpg_model.save_model(f"Saved Models/DDPG HPT/experiment_{args.experiment_number}")

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
        "--num_episodes",
        type=int,
        default=100_000,
        help="Number of Episodes",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=np.random.randint(0, 1_000_000),
        help="Seed for random number generation",
    )

    parser.add_argument(
        "--fixed_seed",
        action="store_true",
        default=False,
        help="Fixed Seed",
    )

    parser.add_argument(
        "--filter_invalid_actions",
        action="store_true",
        default=False,
        help="Whether to filter invalid actions in simulations",
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
        "--epsilon",
        type=float,
        default=1.0,
        help="Epsilon",
    )

    parser.add_argument(
        "--epsilon_decay",
        type=float,
        default=0.995,
        help="Epsilon Decay",
    )

    parser.add_argument(
        "--min_epsilon",
        type=float,
        default=0.01,
        help="Minimum Epsilon",
    )

    parser.add_argument(
        "--gamma",
        type=float,
        default=0.99,
        help="Gamma",
    )

    parser.add_argument(
        "--tau",
        type=float,
        default=0.01,
        help="Tau",
    )

    parser.add_argument(
        "--actor_learning_rate",
        type=float,
        default=0.001,
        help="Actor Learning Rate",
    )

    parser.add_argument(
        "--critic_learning_rate",
        type=float,
        default=0.001,
        help="Critic Learning Rate",
    )

    parser.add_argument(
        "--actor_weight_decay",
        type=float,
        default=0.001,
        help="Actor Weight Decay",
    )

    parser.add_argument(
        "--critic_weight_decay",
        type=float,
        default=0.001,
        help="Critic Weight Decay",
    )

    parser.add_argument(
        "--replay_buffer_size",
        type=int,
        default=1000,
        help="Replay Buffer Size",
    )

    parser.add_argument(
        "--replay_buffer_sample_size",
        type=int,
        default=50,
        help="Replay Buffer Sample Size",
    )

    parser.add_argument(
        "--add_loss_noise",
        action="store_true",
        default=False,
        help="Add Loss Noise",
    )

    parser.add_argument(
        "--actor_architecture_id",
        type=int,
        default=1,
        help="Actor Architecture ID",
    )

    parser.add_argument(
        "--critic_architecture_id",
        type=int,
        default=1,
        help="Critic Architecture ID",
    )

    args = parser.parse_args()

    sys.exit(__main(args))
