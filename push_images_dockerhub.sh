#!/bin/bash

docker tag database-visualization-container alexandrefigueired0/database-visualization-container
docker tag database-ranking-container alexandrefigueired0/database-ranking-container 
docker tag forecast-container alexandrefigueired0/forecast-container 
docker tag management-container alexandrefigueired0/management-container 
docker tag recommendations-container alexandrefigueired0/recommendations-container
docker tag visualization-container alexandrefigueired0/visualization-container
docker tag ranking-container alexandrefigueired0/ranking-container 

docker push alexandrefigueired0/database-visualization-container
docker push alexandrefigueired0/database-ranking-container
docker push alexandrefigueired0/forecast-container
docker push alexandrefigueired0/management-container
docker push alexandrefigueired0/recommendations-container
docker push alexandrefigueired0/visualization-container
docker push alexandrefigueired0/ranking-container