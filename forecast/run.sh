#!/bin/bash

docker build -t forecast_container -f Dockerfile .
docker run --name forecast_container --rm -d -p 8080:8080 forecast_container