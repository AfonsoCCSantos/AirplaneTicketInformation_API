#!/bin/bash

docker build -t database-ranking-container -f Dockerfile .
docker run --name database-ranking-container --rm -d -p 50052:50052 --network microservices  database-ranking-container