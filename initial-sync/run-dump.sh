#!/bin/bash

# Check if the argument is provided
if [ "$#" -ne 3 ]; then
  echo "Usage: $0 <connection_string> <snapshot_name> <output_file>"
  exit 1
fi

CONNECTION_STRING="$1"
SNAPSHOT_NAME="$2"
OUTPUT_FILE="$3"

# TODO: only dump the public schema
pg_dump --dbname="$CONNECTION_STRING" --snapshot="$SNAPSHOT_NAME" > "$OUTPUT_FILE"

# Check if the command was successful
if [ $? -eq 0 ]; then
  echo "Backup successful: $OUTPUT_FILE"
else
  echo "Backup failed"
fi
