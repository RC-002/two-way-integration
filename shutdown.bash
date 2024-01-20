#!/bin/bash

# Stop server
kill $(ps aux | grep '[u]vicorn localCustomersApp:app' | awk '{print $2}')

# Stop Docker containers
docker compose down
