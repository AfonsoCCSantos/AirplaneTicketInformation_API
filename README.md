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

The ranking microservice is a REST API which the only responsabilities are to answer client side requests and delegate their work to the database-ranking microservice via gRPC.

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

For the building and deployment of the microservices there is a run.sh file at the base folder of the project. This run.sh script calls a run.sh present in each of the microservices folders, which builds and runs their respective Docker containers <br>
<br>
So, to build the project, the user should use the following command in the base folder of the project: <br>
`./run.sh`<br>
which will start all the containers. To test a specific endpoint, a browser or a tool like Postman should be used.

## Limitations
When adding a ticket, multiple entries representing airlines and the relation of tickets and arilines are created. This is done via BigQuery streaming buffers. The problem with this imlpementation is that the data is  persisted in the tables 90 minutes after the insertion operation, making it only possible to read them and impossible to perform other operations (like deleting) until the data is persisted. <br>
<br>
For this phase, the services that require machine learning algorithms have still not been implemented. We plan to implement these services on a later phase using Spark.



