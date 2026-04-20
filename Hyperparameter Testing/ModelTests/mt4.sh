#!/bin/bash
#PBS -lselect=1:ncpus=1:mem=3gb:ngpus=1:gpu_type=RTX6000
#PBS -lwalltime=72:00:00
#PBS -o "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"
#PBS -e "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"


################################################################################
# EXPERIMENT: Five Tracks / Single Year
# BAHRAIN, SPAIN, UK, ITALY, BRAZIL / 2023
################################################################################

cd $PBS_O_WORKDIR

module load anaconda3/personal
source activate venv

# Simulation Details
EXPERIMENT_NUMBER=4
NUM_EPISODES=100000
YEARS=2023
TRACKS="BAHRAIN SPAIN UK ITALY BRAZIL"

# Hyperparameters:
EPSILON=1.0
EPSILON_DECAY=0.999
MIN_EPSILON=0.005
GAMMA=0.99
LEARNING_RATE=0.001
WEIGHT_DECAY=0.001
REPLAY_BUFFER_SIZE=1000
EPISODES_TO_UPDATE_TARGET=100
ARCHITECTURE_ID=20

python train_model_test.py \
    --experiment_number $EXPERIMENT_NUMBER \
    --num_episodes $NUM_EPISODES \
    --years $YEARS \
    --tracks $TRACKS \
    --epsilon $EPSILON \
    --epsilon_decay $EPSILON_DECAY \
    --min_epsilon $MIN_EPSILON \
    --gamma $GAMMA \
    --learning_rate $LEARNING_RATE \
    --weight_decay $WEIGHT_DECAY \
    --replay_buffer_size $REPLAY_BUFFER_SIZE \
    --episodes_to_update_target $EPISODES_TO_UPDATE_TARGET \
    --architecture_id $ARCHITECTURE_ID