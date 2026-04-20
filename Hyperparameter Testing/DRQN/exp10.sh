#!/bin/bash
#PBS -lselect=1:ncpus=1:mem=8gb:ngpus=1:gpu_type=RTX6000
#PBS -lwalltime=72:00:00
#PBS -o "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"
#PBS -e "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"

cd $PBS_O_WORKDIR

module load anaconda3/personal
source activate venv

# Simulation Details
EXPERIMENT_NUMBER=10
NUM_EPISODES=100000
YEARS=2023
TRACKS="BAHRAIN"

# Hyperparameters:
EPISODES_TO_UPDATE_TARGET=1000

python train_drqn.py \
    --experiment_number $EXPERIMENT_NUMBER \
    --num_episodes $NUM_EPISODES \
    --years $YEARS \
    --tracks $TRACKS \
    --episodes_to_update_target $EPISODES_TO_UPDATE_TARGET \