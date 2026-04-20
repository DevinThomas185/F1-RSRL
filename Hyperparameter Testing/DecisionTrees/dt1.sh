#!/bin/bash
#PBS -lselect=1:ncpus=1:mem=8gb:ngpus=1:gpu_type=RTX6000
#PBS -lwalltime=72:00:00
#PBS -o "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"
#PBS -e "/rds/general/user/dt120/home/Work/f1-race-strategy/HPC Logs"


################################################################################
# EXPERIMENT: Single Track / Single Year
# UK / 2023
################################################################################

cd $PBS_O_WORKDIR

module load anaconda3/personal
source activate venv

# Simulation Details
MODEL_PATH="Saved Models/DRQN HPT/DRQN Experiment 25/DRQN HPT25_CP7000.pth"
DISABLE_SAFETY_CAR=False
YEARS=2023
TRACKS="UK"

# Decision Tree Hyperparameters:
MAX_DEPTH=30
MAX_ITERATIONS=1000
MAX_SAMPLES=10000
REWEIGHT_SAMPLES=False
BATCH_ROLLOUTS=1000
TEST_ROLLOUTS=1000

python train_decision_tree.py \
    --model_path $MODEL_PATH \
    --disable_safety_car $DISABLE_SAFETY_CAR \
    --years $YEARS \
    --tracks $TRACKS \
    --max_depth $MAX_DEPTH \
    --max_iterations $MAX_ITERATIONS \
    --max_samples $MAX_SAMPLES \
    --reweight_samples $REWEIGHT_SAMPLES \
    --batch_rollouts $BATCH_ROLLOUTS \
    --test_rollouts $TEST_ROLLOUTS \
    --verbose