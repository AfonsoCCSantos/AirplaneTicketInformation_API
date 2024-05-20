#!/bin/bash

docker build -t forecast-container -f Dockerfile .
docker run --name forecast-container --rm -p 8080:8080 forecast-container