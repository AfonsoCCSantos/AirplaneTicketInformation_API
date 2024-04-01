#!/bin/bash

docker build -t ranking_container -f Dockerfile .
docker run --name ranking_container --rm -d -p 8082:8082 --network microservices -e DATABASE_RANKING_HOST=database-ranking ranking_container