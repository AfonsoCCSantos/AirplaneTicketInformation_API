#!/bin/bash

docker build -t login-container -f Dockerfile .
docker run --name login-container --rm -d -p 8085:8085 login-container