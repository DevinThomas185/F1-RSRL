#!/bin/bash

# Regenerate Unified Race State file
python ./Classes/RaceState/generate_UnifiedRaceState.py

# Regenerate UI file
cd GUI
pyside6-uic form.ui -o ui_form.py
cd ../

# Run GUI
python gui.py