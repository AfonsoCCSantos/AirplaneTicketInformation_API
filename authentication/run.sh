#!/bin/bash

docker build -t authentication-container -f Dockerfile .
docker run --name authentication-container --rm -d -p 8085:8085 authentication-container