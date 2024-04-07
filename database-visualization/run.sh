#!/bin/bash

docker build -t database-visualization-container -f Dockerfile .
docker run --name database-visualization-container --rm -d -p 50051:50051 --network microservices database-visualization-container