#!/bin/bash

# Stop servers

# fast api server
PID=$(pgrep -f "python server.py")

if [ -z "$PID" ]; then
  # Flask server is not running
  exit 0
else
  # Kill the Flask server process
  kill $PID
fi



# flask server
PID=$(pgrep -f "python app.py")

if [ -z "$PID" ]; then
  # Flask server is not running
  exit 0
else
  # Kill the Flask server process
  kill $PID
fi

# Stop Docker containers
docker compose down
