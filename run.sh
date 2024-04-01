#!/bin/bash
chmod u+r+x database-visualization/run.sh
chmod u+r+x database-ranking/run.sh
chmod u+r+x forecast/run.sh
chmod u+r+x management/run.sh
chmod u+r+x ranking/run.sh
chmod u+r+x recommendations/run.sh
chmod u+r+x visualization/run.sh

# docker network create microservices

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