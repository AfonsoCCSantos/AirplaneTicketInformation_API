#!/bin/bash

docker build -t database-visualization_container -f Dockerfile .
docker run --name database-visualization_container --rm -d -p 50051:50051 database-visualization_container