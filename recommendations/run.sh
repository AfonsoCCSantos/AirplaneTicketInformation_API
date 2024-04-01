#!/bin/bash

docker build -t recommendations_container -f Dockerfile .
docker run --name recommendations_container --rm -d -p 8083:8083 recommendations_container