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
nohup python server.py > output.log 2>&1 &

# flask server
cd ../stripe
nohup python app.py > output.log 2>&1 &
sleep 5
PID=$(pgrep -f "python app.py")
