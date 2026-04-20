#!/bin/bash

experiment_dir="./Hyperparameter Testing/$1"
output_file="$experiment_dir/hyperparameter_testing_$1.json"

# Remove existing output file if it exists
rm -f "$output_file"

# Start writing the JSON object
echo "{" >> "$output_file"

# Regenerate Unified Race State file
python ./Classes/RaceState/generate_UnifiedRaceState.py

# Loop through each file in the experiment directory
for entry in "$experiment_dir"/*.sh
do
    # Execute the qsub command and capture its output
    output=$(qsub "$entry")
    output="${output%.pbs}"

    # Extract the entry name from the file path
    entry_name=$(basename "$entry")
    entry_name="${entry_name%.sh}"

    # Write the entry and its output to the output file as JSON key-value pairs
    echo "  \"$entry_name\": \"$output\"," >> "$output_file"
done

# Remove the trailing comma from the last line
sed -i '$s/,$//' "$output_file"

# Close the JSON object
echo "}" >> "$output_file"