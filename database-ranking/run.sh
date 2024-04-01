#!/bin/bash

docker build -t database-ranking_container -f Dockerfile .
docker run --name database-ranking_container --rm -d -p 50052:50052 --network microservices --name database-ranking database-ranking_container