# !/bin/bash

# Set python path
export PYTHONPATH=./:$PYTHONPATH

# Start postgres and kafka containers
docker compose up -d

# Wait till the docker containers are up
sleep 10

# Start servers

# fast api server
uvicorn localCustomersApp:app --port 8000 --reload

# flask server
python stripeApp.py
sleep 5
PID=$(pgrep -f "python stripeApp.py")
