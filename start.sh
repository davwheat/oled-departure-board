#!/bin/bash

echo "== Changing working directory"
cd "$(dirname "${BASH_SOURCE[0]}")" || exit 1

echo "== Starting..."

use_emulator=0
if [[ -n "${USE_EMULATOR}" && "${USE_EMULATOR}" == "1" ]]; then
  use_emulator=1
fi

# If already in a virtual environment, exit it
if [ -z "${VIRTUAL_ENV}" ]; then
  echo "== Leaving existing venv..."
  deactivate
fi

if [ ! -d ./venv ]; then
  echo "== Creating venv..."
  python -m venv venv
else
  echo "=== Using existing venv!"
fi

echo "== Activating venv..."
source ./venv/bin/activate

echo "== Installing dependencies..."
req_file="requirements.txt"

if [[ $use_emulator == "1" ]]; then
  req_file="requirements.dev"
fi

pip install -r "$req_file"

echo "== Launching application..."

# Handle environment var args
if [ -z "${STATION_CRS}" ]; then
  echo "===! STATION_CRS is not set." >&2
  exit 1
fi

num_services="${NUM_SERVICES}"
if [ -z "${NUM_SERVICES}" ]; then
  num_services=3
fi

if [[ ! "$num_services" =~ ^[2-9]$ ]]; then
  echo "===! NUM_SERVICES does not contain a valid value. Must be a whole number between 2 and 9 inclusive." >&2
  exit 1
fi

use_emulator_opt=""
if [[ $use_emulator == "1" ]]; then
  use_emulator_opt="--emulate"
fi

python ./src/main.py $use_emulator_opt --services="$num_services" "$STATION_CRS"
