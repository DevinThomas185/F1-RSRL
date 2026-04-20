#!/bin/bash
#PBS -lselect=1:ncpus=1:mem=8gb:ngpus=1:gpu_type=RTX6000
#PBS -lwalltime=72:00:00
#PBS -o "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"
#PBS -e "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"

cd $PBS_O_WORKDIR

module load anaconda3/personal
source activate venv

# Simulation Details
EXPERIMENT_NUMBER=21
NUM_EPISODES=100000
YEARS=2023
TRACKS="BAHRAIN"

# Hyperparameters:
EPSILON_DECAY=0.999
MIN_EPSILON=0.005
GAMMA=0.98
LEARNING_RATE=0.002
REPLAY_BUFFER_SIZE=100

python train_drqn.py \
    --experiment_number $EXPERIMENT_NUMBER \
    --num_episodes $NUM_EPISODES \
    --years $YEARS \
    --tracks $TRACKS \
    --epsilon_decay $EPSILON_DECAY \
    --min_epsilon $MIN_EPSILON \
    --gamma $GAMMA \
    --learning_rate $LEARNING_RATE \
    --replay_buffer_size $REPLAY_BUFFER_SIZE \