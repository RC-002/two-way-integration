# !/bin/bash

# Set python path
export PYTHONPATH=$(pwd):$PYTHONPATH

# Start postgres and kafka containers
docker compose up -d

# Wait till the docker containers are up
sleep 10

# Start servers

# fast api server
cd source
python server.py

# flask server
cd ../stripe
python app.py
sleep 5
PID=$(pgrep -f "python stripeApp.py")
