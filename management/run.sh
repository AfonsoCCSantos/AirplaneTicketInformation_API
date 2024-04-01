#!/bin/bash

docker build -t management_container -f Dockerfile .
docker run --name management_container --rm -d -p 8081:8081 --network microservices -e DATABASE_VISUALIZATION_HOST=database-visualization management_container