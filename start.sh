#!/bin/bash

echo "== Changing working directory"
cd "$(dirname "${BASH_SOURCE[0]}")"

echo "== Starting..."

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
pip install -r requirements.txt

echo "== Launching application..."
python ./src/main.py $STATION_CRS
