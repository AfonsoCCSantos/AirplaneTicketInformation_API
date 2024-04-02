#!/bin/bash

# Ensure run scripts have execute permissions
chmod +x database-visualization/run.sh
chmod +x database-ranking/run.sh
chmod +x forecast/run.sh
chmod +x management/run.sh
chmod +x ranking/run.sh
chmod +x recommendations/run.sh
chmod +x visualization/run.sh

# Create Docker network if not exists
docker network inspect microservices &>/dev/null || {
    echo "Creating Docker network..."
    docker network create microservices
}

cd database-visualization
./run.sh
cd ..

cd database-ranking
./run.sh
cd ..

cd forecast
./run.sh
cd ..

cd management
./run.sh
cd ..

cd ranking
./run.sh
cd ..

cd recommendations
./run.sh
cd ..

cd visualization
./run.sh
cd ..