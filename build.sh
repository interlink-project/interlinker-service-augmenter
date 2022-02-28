#!/bin/bash

#docker-compose down
# Start up the containers
docker-compose -f docker-compose.yml --env-file .env build

docker-compose -f docker-compose.yml --env-file .env up -d
# Check that containers are up and running
docker-compose ps