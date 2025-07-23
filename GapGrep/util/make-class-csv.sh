#!/bin/bash


# Store the directory and CSV file paths
directory=project_data
csv_file=resources/class_projects.csv

# Check if the directory exists and is a directory
if [ ! -d "$directory" ]; then
  echo "Error: '$directory' is not a valid directory."
  exit 1
fi

# Create or overwrite the CSV file with the header
echo "name,active" > "$csv_file"

# Iterate through the directory and append directory names to the CSV
for item in "$directory"/*; do
  if [ -d "$item" ]; then
    dirname=$(basename "$item")
    echo "$dirname,true" >> "$csv_file" # Quote the name for CSV safety
  fi
done

echo "Directory names written to $csv_file"
exit 0