from flask import Flask, redirect, render_template, session, url_for, request
import grpc
import os
import jwt
import requests
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import Auth0JWTBearerTokenValidator
import time
import random
import psutil

from visualization_pb2 import Ticket, TicketsRequest, Airline, AirlineRequest, VisualizationInsertionRequest, \
                                 VisualizationDeleteRequest
from visualization_pb2_grpc import VisualizationStub
from ranking_pb2 import AirlinesRankingByTicketPriceRequest, AirlinesRankingByTicketPriceResponse, \
                         RankingInsertionRequest, RankingDeleteRequest, AirlineRanking
from ranking_pb2_grpc import RankingStub
from authlib.integrations.flask_client import OAuth
from prometheus_client import start_http_server, Summary, Histogram, CONTENT_TYPE_LATEST, generate_latest, Counter, Gauge

# app = Flask(__name__)

# Connect to the database visualization service
database_visualization_host = os.getenv("DATABASE_VISUALIZATION_HOST", "localhost")
database_visualization_channel = grpc.insecure_channel(f"{database_visualization_host}:50051")
database_visualization_client = VisualizationStub(database_visualization_channel)

# Connect to the database ranking service
database_ranking_host = os.getenv("DATABASE_RANKING_HOST", "localhost")
database_ranking_channel = grpc.insecure_channel(f"{database_ranking_host}:50052")
database_ranking_client = RankingStub(database_ranking_channel)

APP_SECRET_KEY=os.getenv("APP_SECRET_KEY")

AUTH0_DOMAIN=os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID=os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET=os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_MANAGEMENT_TOKEN=os.getenv("AUTH0_MANAGEMENT_TOKEN")

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
)

# metrics
request_counter = Counter("requests_counter_management", "Total number of requests of management")
cpu_usage = Gauge('cpu_usage_percent_management', 'CPU Usage Percentage of management')
memory_usage = Gauge('memory_usage_percent_management', 'Memory Usage Percentage of management')

@app.route("/api/management/tickets/<access_token>", methods=['POST'])
def add_tickets(access_token):
    request_counter.inc(1)

    headers = {
        "authorization": f"""Bearer {AUTH0_MANAGEMENT_TOKEN}"""
    }

    user_id = request.cookies.get("user_id")
    if not user_id:
        return "Not authorized", 401
    
    try:
        response = requests.get(f"https://{AUTH0_DOMAIN}/api/v2/users/{user_id}/roles", headers=headers)
        response = response.json()
    except Exception as e:
        return "Not authorized", 401

    if not response:
        return "Not authorized", 401

    hasPermission = response[0]['name'] in ['admin']

    if not hasPermission:
        return "Not authorized", 401

    request_body = request.json

    ticket_body = request_body["ticket"]
    airlines_body = request_body["airlines"]

    ticket = Ticket(
        leg_id=ticket_body['leg_id'],
        departure_place=ticket_body['departure_place'],
        arrival_place=ticket_body['arrival_place'],
        flight_date=ticket_body['flight_date'],
        total_fare=ticket_body['total_fare'],
        travel_duration=ticket_body['travel_duration'],
        total_travel_distance=ticket_body['total_travel_distance'],
        is_refundable= ticket_body['is_refundable'],
        is_non_stop=ticket_body['is_non_stop']
    )

    airlines = []
    airlinesRanking = []
    for airline_body in airlines_body:
        airline = Airline(
            airline_code=airline_body["airline_code"],
            airline_name = airline_body["airline_name"]
        )
        airlineRanking = AirlineRanking(
            airline_code=airline_body["airline_code"],
            airline_name = airline_body["airline_name"]
        )

        airlines.append(airline)
        airlinesRanking.append(airlineRanking)

    visualization_insertion_request = VisualizationInsertionRequest(ticket=ticket, airlines=airlines)
    ranking_insertion_request = RankingInsertionRequest(leg_id = ticket.leg_id, price=ticket.total_fare, airlines=airlinesRanking)

    # Add the ticket to the tickets database
    tickets_response = database_visualization_client.AddTicket(visualization_insertion_request)
    # Add to the ranking database
    ranking_response = database_ranking_client.AddAirlinePrice(ranking_insertion_request)

    if tickets_response == "error":
        return "Error adding ticket to the visualization database"
    if ranking_response == "error":
        return "Error adding airline price to the ranking database"    

    return "Ticket added successfully"

@app.route("/api/management/tickets/<leg_id>/<access_token>", methods=['DELETE'])
def delete_ticket(leg_id, access_token):
    request_counter.inc(1)

    headers = {
        "authorization": f"""Bearer {AUTH0_MANAGEMENT_TOKEN}"""
    }
    
    user_id = request.cookies.get("user_id")
    if not user_id:
        return "Not authorized", 401
    
    try:
        response = requests.get(f"https://{AUTH0_DOMAIN}/api/v2/users/{user_id}/roles", headers=headers)
        response = response.json()
    except Exception as e:
        return "Not authorized", 401

    if not response:
        return "Not authorized", 401

    hasPermission = response[0]['name'] in ['admin']

    if not hasPermission:
        return "Not authorized", 401

    # Delete the ticket from the tickets database
    # tickets_response = database_visualization_client.DeleteTicket(TicketsRequest(ticket_id=ticketId))

    #Remove ticket from ranking database
    ranking_delete_request = RankingDeleteRequest(leg_id=leg_id)
    ranking_delete_response = database_ranking_client.DeleteTicket(ranking_delete_request)

    if ranking_delete_response == "error":
        return "Error deleting ticket from the ranking database"

    visualization_delete_request = VisualizationDeleteRequest(leg_id=leg_id)
    visualization_delete_response = database_visualization_client.DeleteTicket(visualization_delete_request)

    if visualization_delete_response == "error":
        return "Error deleting ticket from the visualization database"

    return "Ticket deleted successfully"

@app.route("/api/management/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200

@app.route("/metrics", methods=['GET'])
def prometheus_metrics():
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    return generate_latest() 
