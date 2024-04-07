#!/bin/bash

docker build -t ranking-container -f Dockerfile .
docker run --name ranking-container --rm -d -p 8082:8082 --network microservices -e DATABASE_RANKING_HOST=database-ranking-container ranking-container