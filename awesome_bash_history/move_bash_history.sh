#!/bin/bash

# Define the source and destination paths
source_path="$HOME/.my_bash_hist"
destination_dir="$HOME/.history"

# Create the destination directory if it doesn't exist
mkdir -p "$destination_dir"

# Generate the destination filename with the current date
destination_filename="$destination_dir/bh_$(date +%Y%m%d)"

# Move the Bash history file to the destination
mv "$source_path" "$destination_filename"

