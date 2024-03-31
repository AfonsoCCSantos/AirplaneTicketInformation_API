from flask import Flask, request
import grpc
import os

from visualization_pb2 import Ticket, TicketsRequest, Airline, AirlineRequest
from visualization_pb2_grpc import VisualizationStub
from ranking_pb2 import AirlinesRankingByTicketPriceRequest, AirlinesRankingByTicketPriceResponse, AirlinePrice
from ranking_pb2_grpc import RankingStub

app = Flask(__name__)

# Connect to the database visualization service
database_visualization_host = os.getenv("DATABASE_VISUALIZATION_HOST", "localhost")
database_visualization_channel = grpc.insecure_channel("localhost:50051")
database_visualization_client = VisualizationStub(database_visualization_channel)

# Connect to the database ranking service
database_ranking_host = os.getenv("DATABASE_MANAGEMENT_HOST", "localhost")
database_ranking_channel = grpc.insecure_channel("localhost:50052")
database_ranking_client = RankingStub(database_ranking_channel)

@app.route("/api/management/tickets", methods=['POST'])
def add_tickets():
    request_body = request.json

    ticket = Ticket(
        leg_id=request_body['leg_id'],
        departure_place=request_body['departure_place'],
        arrival_place=request_body['arrival_place'],
        flight_date=request_body['flight_date'],
        total_fare=request_body['total_fare'],
        travel_duration=request_body['travel_duration'],
        total_travel_distance=request_body['total_travel_distance'],
        is_refundable=request_body['is_refundable'],
        is_non_stop=request_body['is_non_stop']
    )

    #airline_price = AirlinePrice(
    #    airline_code=request_body['airline'],
    #    price=request_body['price']
    #)

    # Add the ticket to the tickets database
    tickets_response = database_visualization_client.AddTicket(ticket)

    # Add the ticket to the ranking database
    #ranking_response = database_ranking_client.AddAirlinePrice(airline_price)

    return "adds a new ticket"

@app.route("/api/management/tickets/<ticketId>", methods=['DELETE'])
def delete_ticket(ticketId):
    return "deletes a ticket"