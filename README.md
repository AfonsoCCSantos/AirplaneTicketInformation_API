# ☁️ Cloud Computing Project - Group 19 
- Afonso Santos - FC56368
- Raquel Domingos - FC56378
- Tomás Barreto - FC56282
- Alexandre Figueiredo - FC57099
- Miguel Faísco - FC56954

## 📐 Project Structure

The system is divided in 7 microservices, each one located in its own folder within the project:
- Visualization
- Ranking
- Recommendations
- Forecast
- Management
- Database-Ranking
- Database-Visualization

### Visualization

The visualization microservice is a REST API which the only responsabilities are to answer client side requests and delegate their work to the database-visualization microservice via gRPC.

### Database-Visualization

The database-visualization microservice can only be accessed by the visualization and management microservices via gRPC. Its only responsibilities are to handle requests from both of these microservices by retrieving, adding and deleting information from the database. The database consists of the tables: tickets, airlines and ticket_airlines. The table tickets stores information like: legId, totalFare, flightDate, travelDuration, totalTravelDistance, isRefundable, startingAirport, destinationAirport, isNonStop. The table airlines stores information like: airlineName, airlineCode. The table ticket_airlines is responsible to map tickets and airlines, storing the legId of the ticket and the airlineCode of the airline.


### Ranking

The ranking microservice is a REST API which the only responsabilities are to answer client side requests and delegate their work to the database-ranking microservice via gRPC..

### Database-Ranking

The database-ranking microservice can only be accessed by the ranking and management microservices via gRPC. Its only responsibilities are to handle requests from both of these microservices by retrieving, adding and deleting information from the database. The database related to the ranking service
consists of a single table called "ranking". This table consists of tickets and holds its id, its price and the corresponding airline so that it is possible to get a hold of the average price for every airline, thus creating a ranking.

### Recommendations

The recommendations microservice is a REST API that answers client side requests and makes use of a ML model to get recommendations for the cheapest airline to flight or the cheapest date to flight.

### Forecast

The forecast microservice is a REST API that answers client side requests and makes use of a ML model to get a forecast of the cheapest airplane ticket.

### Management

The management microservice is able the database-visualization and the database-ranking via gRPC. It is responsible for the addition and deletion of tickets in the databases.

## 🛠️ Building & Deployment 

### Running Locally
For the building and deployment of the microservices, the following commands should be run.<br>
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml`<br>
`kubectl apply -f ingress.yaml`<br>
`kubectl apply -f kubernetes.yaml`<br>
`kubectl apply -f autoscaler.yaml`<br>
`kubectl port-forward --namespace=ingress-nginx service/ingress-nginx-controller 8080:80`
<br>

To test a specific endpoint, a browser or a tool like Postman should be used. If the docker containers are started in the Google Cloud Platform, then the Google Cloud Platform web preview should be used.

### Running In the Cloud
To run the project in the Google Cloud, the following commands should be used.

`minikube start`<br>
`gcloud config set project projectId` where projectId is the id of a project in GCP <br>
`gcloud container clusters create-auto clusterName --region=europe-west4` where clusterName is the name of the cluster to create <br>
`gcloud container clusters get-credentials clusterName --region=europe-west4` where clusterName is the name of the previously created cluster <br>
`kubectl config current-context` <br>
`kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml`<br>
Wait for the ingress-nginx-controller to start running, use the next command to verify this condition <br>
`kubectl get pods --namesapce=ingress-nginx` <br>
`kubectl apply -f ingress.yaml`<br>
`kubectl apply -f kubernetes.yaml`<br>
`kubectl apply -f autoscaler.yaml`<br>
`kubectl get ingress` wait until an ip is attributed, to get the ip of where the application is running on <br>

### Logging and Monitoring
The project uses Prometheus to register system logs, and Grafana to display dashboards that are easier to read and customize.


## 📉 Limitations
When adding a ticket, multiple entries representing airlines and the relation of tickets and airlines are created. This is done via BigQuery streaming buffers. The problem with this implementation is that the data is  persisted in the tables 90 minutes after the insertion operation, making it only possible to read them and impossible to perform other operations (like deleting) until the data is persisted. <br>
<br><br>
There are some endpoints that require authentication to work (The endpoints from the recommendation). We aimed to present the user with a login page when he tries to access these endpoints, being redirected (with his token obtained from the login) to the endpoint he initially tried to access. Instead, the user must access the authentication service and perform the login through there, which grants him with a cookie with the required permissions to access the intended endpoints (provided he has the permission to access them).
<br> 
Spark isn't configured as wished. The requests regarding machine learning models aren't being ran parallely in a spark cluster environment.



