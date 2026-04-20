#!/bin/bash

# Run caffeinate in the background to prevent sleeping
if [[ $OSTYPE == 'darwin'* ]]; then
    caffeinate -w $$ &
fi

# Regenerate Unified Race State file
python ./Classes/RaceState/generate_UnifiedRaceState.py

# Run test_models.py
    # --seed 0 \
python test_models.py \
    --num_tests 500 \
    --years 2023 \
    --tracks \
        BAHRAIN AZERBAIJAN UK HUNGARY ITALY SINGAPORE JAPAN QATAR ABU_DHABI SPAIN SAUDI_ARABIA AUSTRIA MEXICO USA \
    --with_random_fixed 
    
    # --models \
    #     "Saved Models/Model Tests/Model Test 16/Model Test 16_CP7000.pth" \
    # --with_fixed \
    # --plot_histograms \
    # --with_mercedes \

    
        # "Saved Models/Model Tests/Model Test 17/Model Test 17_CP9000.pth" \
        # "Saved Models/Model Tests/Model Test 15/Model Test 15_CP11000.pth" \
        # "Saved Models/DRQN HPT/DRQN Experiment 25/DRQN HPT25_CP22000.pth" \

