#!/bin/bash

# Run caffeinate in the background to prevent sleeping
if [[ $OSTYPE == 'darwin'* ]]; then
    caffeinate -w $$ &
fi

# Regenerate Unified Race State file
python ./Classes/RaceState/generate_UnifiedRaceState.py

# Run main.py
python main.py