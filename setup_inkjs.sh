#!/bin/bash

# Check if there's only one json file in output/
count=0
for file in output/*.json; do
    ((count++))
done
if [ $count -ne 1 ]; then
    echo "Error: Not exactly one .json file found."
    exit 1
fi

# Copy the json file to assets/ with name game.json
cp output/*json inkjs/story.json