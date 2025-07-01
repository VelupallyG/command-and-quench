#!/bin/bash

# Activate your virtual environment
# source venv/bin/activate

# Create logs folder if not exists
mkdir -p logs

echo "=========================="
echo "Starting mic_transcribe.py"
echo "=========================="
# Run mic_transcribe.py in the background, save logs
python mic_transcribe.py > logs/mic_transcribe.log 2>&1 &

# Capture the PID so you can clean up later
MIC_PID=$!

echo "=========================="
echo "Starting watcher.py"
echo "=========================="
# Run watcher.py in the background, save logs
python watcher.py > logs/watcher.log 2>&1 &

WATCHER_PID=$!

echo "=========================="
echo "Both scripts are running."
echo "mic_transcribe.py PID: $MIC_PID"
echo "watcher.py PID: $WATCHER_PID"
echo "=========================="

echo "Press [CTRL+C] to stop both gracefully."

# Trap CTRL+C to clean up background processes
trap "echo ''; echo 'Stopping processes...'; kill $MIC_PID; kill $WATCHER_PID; exit 0" SIGINT

# Keep the script alive to maintain trap handling
while true; do
    sleep 1
done
