#!/bin/bash

docker build -t recommendations-container -f Dockerfile .
docker run --name recommendations-container --rm -d -p 8083:8083 recommendations-container