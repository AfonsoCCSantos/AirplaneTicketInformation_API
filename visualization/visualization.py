from flask import Flask
import grpc
import os

from visualization_pb2 import Ticket, TicketsRequest, Airline, AirlineRequest
from visualization_pb2_grpc import VisualizationStub

app = Flask(__name__)

# Connect to the database visualization service
database_visualization_host = os.getenv("DATABASE_VISUALIZATION_HOST", "localhost")
database_visualization_channel = grpc.insecure_channel(f"{database_visualization_host}:50051")
database_visualization_client = VisualizationStub(database_visualization_channel)

@app.route("/api/visualization/tickets/<departure>/<arrival>", methods=["GET"])
def get_tickets_from_to(departure, arrival):
    tickets_request = TicketsRequest(
        departure_place=departure,
        arrival_place=arrival
    )

    print(tickets_request)

    tickets_response = database_visualization_client.GetTickets(tickets_request)

    return f"list of tickets: {tickets_response.tickets}"

@app.route("/api/visualization/airlines/<airline_code>", methods=["GET"])
def get_airline_details(airline_code):
    airline_request = AirlineRequest(airline_code=airline_code)
    
    airline_response = database_visualization_client.GetAirline(airline_request)

    return f"airlineCode: {airline_response.airline.airline_code} | airlineName: {airline_response.airline.airline_name}"

@app.route("/api/visualization/liveness-check", methods=['GET'])
def liveness_check():
    return 200