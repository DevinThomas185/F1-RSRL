#!/bin/bash

# Run the command and store the output
output=$(qstat)

# Extract the Job IDs from the output
job_ids=$(echo "$output" | awk 'NR>2 {print $1}')

# Loop through each Job ID and echo the qdel command
for job_id in $job_ids; do
    qdel $job_id
done
