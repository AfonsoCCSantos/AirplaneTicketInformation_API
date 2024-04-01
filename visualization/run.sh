#!/bin/bash

docker build -t visualization_container -f Dockerfile .
docker run --name visualization_container --rm -d -p 8084:8084 --network microservices -e DATABASE_VISUALIZATION_HOST=database-visualization visualization_container