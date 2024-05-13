from flask import Flask
import grpc
import os
import time
import random

from visualization_pb2 import Ticket, TicketsRequest, Airline, AirlineRequest
from visualization_pb2_grpc import VisualizationStub
from prometheus_client import start_http_server, Summary, Histogram, CONTENT_TYPE_LATEST, generate_latest

app = Flask(__name__)

# Connect to the database visualization service
database_visualization_host = os.getenv("DATABASE_VISUALIZATION_HOST", "localhost")
database_visualization_channel = grpc.insecure_channel(f"{database_visualization_host}:50051")
database_visualization_client = VisualizationStub(database_visualization_channel)
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
histogram = Histogram('python_my_histogram', 'This is my histogram')
##start_http_server(9050)

@REQUEST_TIME.time()
@app.route("/api/visualization/tickets/<departure>/<arrival>", methods=["GET"])
def get_tickets_from_to(departure, arrival):
    tickets_request = TicketsRequest(
        departure_place=departure,
        arrival_place=arrival
    )

    tickets_response = database_visualization_client.GetTickets(tickets_request)

    return f"list of tickets: {tickets_response.tickets}"

@REQUEST_TIME.time()
@app.route("/api/visualization/airlines/<airline_code>", methods=["GET"])
def get_airline_details(airline_code):
    airline_request = AirlineRequest(airline_code=airline_code)
    
    airline_response = database_visualization_client.GetAirline(airline_request)

    return f"airlineCode: {airline_response.airline.airline_code} | airlineName: {airline_response.airline.airline_name}"

@REQUEST_TIME.time()
@app.route("/api/visualization/liveness-check", methods=['GET'])
def liveness_check():
    rValue = random.random()
    histogram.observe(rValue * 10)
    time.sleep(rValue)
    return "ok",200

# @app.route("/api/visualization/metrics", methods=['GET'])
# def metrics():
#     return "ok",200    

@app.route("/metrics", methods=['GET'])
def prometheus_metrics():
    return generate_latest() 