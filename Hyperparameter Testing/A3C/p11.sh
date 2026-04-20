#!/bin/bash
#PBS -lselect=1:ncpus=256:mem=128gb:ngpus=1:gpu_type=RTX6000
#PBS -lwalltime=72:00:00
#PBS -o "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"
#PBS -e "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"

cd $PBS_O_WORKDIR

module load anaconda3/personal
source activate venv

# Simulation Details
EXPERIMENT_NUMBER=11
MIN_EPISODES=100000000
YEARS=2023
TRACKS="BAHRAIN"

# Hyperparameters:
VALUE_LOSS_COEFF=0.001
MAX_GRAD_NORM=1
LEARNING_RATE=0.01

python train_a3c.py \
    --experiment_number $EXPERIMENT_NUMBER \
    --min_episodes $MIN_EPISODES \
    --years $YEARS \
    --tracks $TRACKS \
    --value_loss_coeff $VALUE_LOSS_COEFF \
    --max_grad_norm $MAX_GRAD_NORM \
    --learning_rate $LEARNING_RATE \