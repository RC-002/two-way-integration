# !/bin/bash

# Start postgres and kafka containers
docker compose up -d

# Wait till the docker containers are up
sleep 10

# Start servers
uvicorn localCustomersApp:app --port 8000 --reload