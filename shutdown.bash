#!/bin/bash

# Stop servers

# fast api server
kill $(ps aux | grep '[u]vicorn localCustomersApp:app' | awk '{print $2}')


# flask server
PID=$(pgrep -f "python stripeApp.py")

if [ -z "$PID" ]; then
  # Flask server is not running
  exit 0
else
  # Kill the Flask server process
  kill $PID
fi

# Stop Docker containers
docker compose down
