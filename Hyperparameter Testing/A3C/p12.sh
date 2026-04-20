#!/bin/bash
#PBS -lselect=1:ncpus=256:mem=128gb:ngpus=1:gpu_type=RTX6000
#PBS -lwalltime=72:00:00
#PBS -o "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"
#PBS -e "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"

cd $PBS_O_WORKDIR

module load anaconda3/personal
source activate venv

# Simulation Details
EXPERIMENT_NUMBER=12
MIN_EPISODES=100000000
YEARS=2023
TRACKS="BAHRAIN"

# Hyperparameters:
GAMMA=0.98

python train_a3c.py \
    --experiment_number $EXPERIMENT_NUMBER \
    --min_episodes $MIN_EPISODES \
    --years $YEARS \
    --tracks $TRACKS \
    --gamma $GAMMA \