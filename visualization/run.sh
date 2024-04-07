#!/bin/bash

docker build -t visualization-container -f Dockerfile .
docker run --name visualization-container --rm -d -p 8084:8084 --network microservices -e DATABASE_VISUALIZATION_HOST=database-visualization-container visualization-container