#!/bin/bash

docker build -t management-container -f Dockerfile .
docker run --name management-container --rm -d -p 8081:8081 --network microservices -e DATABASE_VISUALIZATION_HOST=database-visualization-container -e DATABASE_RANKING_HOST=database-ranking-container management-container