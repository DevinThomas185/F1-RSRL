### System imports
import sys
import random
import torch
import numpy as np

### Released Imports
from Classes.Enums import Track
from Classes.RaceState.UnifiedRaceState import UnifiedRaceState
from Classes.RaceStrategy.SimpleRaceStrategy import SimpleRaceStrategy
from Models.CDQNModel import CDQNModel

# Models
from Models.DQNModel import DQNModel
from ParallelModels.A3CModel import A3CModel
from Models.PracticeDQNModel import PracticeDQNModel
from Models.DDPGModel import DDPGModel
from Models.IRLModel import IRLModel
from Models.DRQNModel import DRQNModel
from Models.URSModel import URSModel

# Architectures
from Architectures.QNetwork import QNetwork
from Architectures.RecurrentQN import RecurrentQN
from Architectures.ActorCritic import Actor, Critic
from Architectures.HPT_RecurrentQN import *

# Reward Functions
from RewardFunctions.RewardFunctions import (
    basic_reward,
    simple_reward,
    gap_rewards,
    stint_reward,
    thomas_reward_2,
    thomas_reward,
    picinotti_reward,
    heilmeier_reward,
)


def train_dqn():
    seed = random.randint(0, 1_000_000)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    dqn_model = DQNModel(
        selected_driver=44,
        name="DQN Retest",
        device=device,
        disable_safety_car=False,
        allowed_years=["2023"],
        allowed_tracks=[Track.BAHRAIN],
        reward_function=thomas_reward_2,
    )

    num_episodes = 10000

    dqn_model.train(
        num_episodes=num_episodes,
        seed=seed,
        fixed_seed=False,
        simulation_step_size=1,
        filter_invalid_actions=False,
        checkpointing_details={
            "checkpoint_directory": "Saved Models/DQN Retest",
            "checkpoint_frequency": num_episodes // 20,
        },
        verbose=True,
        epsilon=1.0,
        epsilon_decay=0.96,
        min_epsilon=0.01,
        gamma=0.99,
        learning_rate=0.01,
        weight_decay=0,
        replay_buffer_size=1_000,
        replay_buffer_sample_size=50,
        episodes_to_update_target=20,
        optimiser_type=torch.optim.Adam,
        generate_plots=True,
    )

    dqn_model.save_model("Saved Models/dqn_model")

    return 0


def train_cdqn():
    seed = random.randint(0, 1_000_000)

    policy_network = QNetwork(UnifiedRaceState.size(), len(SimpleRaceStrategy))
    target_network = QNetwork(UnifiedRaceState.size(), len(SimpleRaceStrategy))

    cdqn_model = CDQNModel(
        selected_driver=44,
        name="CDQN BAHRAIN 2023",
        policy_network=policy_network,
        target_network=target_network,
        disable_safety_car=False,
        allowed_years=["2023"],
        allowed_tracks=[Track.BAHRAIN],
        reward_function=thomas_reward,
    )

    num_episodes = 1000

    cdqn_model.train(
        num_episodes=num_episodes,
        seed=seed,
        fixed_seed=False,  # Forces the exact same scenario to run
        simulation_step_size=1,
        # checkpointing={
        #     "checkpoint_directory": "Saved Models/CDQN Multi-Seed",
        #     "checkpoint_frequency": num_episodes // 10,
        # },
        verbose=True,
        epsilon=1.0,
        epsilon_decay=0.99,
        min_epsilon=0.01,
        gamma=0.98,
        tau=0.1,
        learning_rate=0.001,
        weight_decay=0.01,
        replay_buffer_size=100_000,
        replay_buffer_sample_size=25,
        episodes_to_update_target=20,
        optimiser_type=torch.optim.RMSprop,
    )

    cdqn_model.save_model("Saved Models/cdqn_model")

    return 0


def train_practice_dqn():
    policy_network = QNetwork(1, len(SimpleRaceStrategy))
    target_network = QNetwork(1, len(SimpleRaceStrategy))

    practice_dqn_model = PracticeDQNModel(
        selected_driver=0,
        name="PRACTICE DQN",
        policy_network=policy_network,
        target_network=target_network,
    )

    practice_dqn_model.train(
        num_episodes=1000,
        filter_invalid_actions=False,
        verbose=False,
        epsilon=1.0,
        epsilon_decay=0.99,
        min_epsilon=0.1,
        gamma=0.99,
        tau=1,
        learning_rate=0.0001,
        weight_decay=0.01,
        replay_buffer_size=1000,  # 100
        replay_buffer_sample_size=32,  # 50
        episodes_to_update_target=20,
        optimiser_type=torch.optim.Adam,
    )

    return 0


def train_ddpg():
    seed = random.randint(0, 1_000_000)

    actor_network = Actor(UnifiedRaceState.size(), len(SimpleRaceStrategy))
    critic_network = Critic(UnifiedRaceState.size(), len(SimpleRaceStrategy))

    ddpg_model = DDPGModel(
        selected_driver=44,
        name="DDPG BAHRAIN 2023",
        actor_network=actor_network,
        critic_network=critic_network,
        disable_safety_car=False,
        allowed_years=["2023"],
        allowed_tracks=[Track.BAHRAIN],
        reward_function=stint_reward,
    )

    ddpg_model.train(
        num_episodes=10_000,
        seed=seed,
        fixed_seed=True,  # Forces the exact same scenario to run
        simulation_step_size=1,
        filter_invalid_actions=False,
        checkpointing={
            "checkpoint_directory": "Saved Models/DDPG Bahrain Stint",
            "checkpoint_frequency": 500,
        },
        verbose=True,
        epsilon=1.0,
        epsilon_decay=0.995,
        min_epsilon=0.01,
        gamma=0.99,
        tau=0.001,
        actor_learning_rate=0.001,
        critic_learning_rate=0.001,
        actor_weight_decay=0.0,
        critic_weight_decay=0.0,
        replay_buffer_size=100,
        replay_buffer_sample_size=50,
        actor_optimiser_type=torch.optim.Adam,
        critic_optimiser_type=torch.optim.Adam,
        generate_plots=True,
    )

    ddpg_model.save_model("Saved Models/ddpg_model_1")

    return 0


def train_irl():
    seed = random.randint(0, 1_000_000)

    from torch import nn

    policy_network = nn.Sequential(
        nn.Linear(UnifiedRaceState.size(), 128),
        nn.ReLU(),
        nn.Linear(128, 128),
        nn.ReLU(),
        nn.Linear(128, len(SimpleRaceStrategy)),
        nn.Softmax(dim=-1),
    )

    irl_model = IRLModel(
        selected_driver=44,
        policy_network=policy_network,
    )

    irl_model.train(
        num_episodes=1000,
        seed=seed,
        fixed_seed=False,  # Forces the exact same scenario to run
        simulation_step_size=1,
        disable_safety_car=False,
        allowed_years=["2023"],
        allowed_tracks=[Track.BAHRAIN],
        verbose=True,
        learning_rate=0.001,
        weight_decay=0.0,
        optimiser_type=torch.optim.Adam,
    )

    irl_model.save_model("Saved Models/irl_model_1")

    return 0


def train_drqn():
    seed = random.randint(0, 1_000_000)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    policy_network = HPT_6_RecurrentQN()
    target_network = HPT_6_RecurrentQN()

    exp_num = 3
    drqn_model = DRQNModel(
        selected_driver=44,
        name=f"DRQN HPT{exp_num}",
        device=device,
        policy_network=policy_network,
        target_network=target_network,
        disable_safety_car=False,
        allowed_years=["2023"],
        allowed_tracks=[Track.BAHRAIN],
        reward_function=thomas_reward_2,
    )

    # drqn_model = DRQNModel.load_model("Saved Models/drqn_params_test.pth")

    drqn_model.train(
        num_episodes=100,
        seed=seed,
        fixed_seed=False,
        simulation_step_size=1,
        filter_invalid_actions=False,
        # checkpointing_details={
        #     "checkpoint_directory": f"Saved Models/DRQN HPT/DRQN Experiment {exp_num}",
        #     "checkpoint_frequency": 10,
        # },
        verbose=True,
        epsilon=1.0,
        epsilon_decay=0.995,
        min_epsilon=0.01,
        gamma=0.99,
        learning_rate=0.001,
        weight_decay=0.001,
        replay_buffer_size=100,
        episodes_to_update_target=100,
        optimiser_type=torch.optim.Adam,
        generate_plots=False,
    )

    # drqn_model.save_model(f"Saved Models/DRQN HPT/experiment_{exp_num}")

    return 0


def train_urs():
    ursmodel = URSModel(
        selected_driver=44,
        name="URS BAHRAIN 2023",
    )

    ursmodel.train(
        num_episodes=1000,
        allowed_tracks=[Track.BAHRAIN],
        allowed_years=["2023"],
        verbose=False,
    )


def train_parallel():
    parallel_model = A3CModel(
        selected_driver=44,
        name="ParallelModel",
        disable_safety_car=False,
        allowed_years=["2023"],
        allowed_tracks=[Track.BAHRAIN],
        reward_function=simple_reward,
    )

    parallel_model.train(
        min_episodes=1000,
        simulation_step_size=1,
        checkpointing_details={
            "checkpoint_directory": f"Saved Models/ParallelModel",
            "checkpoint_frequency": 100,
        },
        gamma=0.99,
        value_loss_coef=0.5,
        max_grad_norm=50,
        learning_rate=0.001,
        weight_decay=0.001,
        generate_plots=True,
    )

    parallel_model.save_model("Saved Models/parallel_model")


def __main():
    np.set_printoptions(suppress=True)

    train_dqn()
    # train_cdqn()
    # train_practice_dqn()
    # train_ddpg()
    # train_irl()
    # train_drqn()
    # train_urs()
    # train_parallel()


if __name__ == "__main__":
    sys.exit(__main())
