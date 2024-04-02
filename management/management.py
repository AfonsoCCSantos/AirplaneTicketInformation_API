from flask import Flask, request
import grpc
import os

from visualization_pb2 import Ticket, TicketsRequest, Airline, AirlineRequest, VisualizationInsertionRequest, VisualizationDeleteRequest, RankingInsertionRequest, RankingDeleteRequest
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

    ticket_body = request_body["ticket"]
    airlines_body = request_body["airlines"]

    ticket = Ticket(
        leg_id=ticket_body['leg_id'],
        departure_place=ticket_body['departure_place'],
        arrival_place=ticket_body['arrival_place'],
        flight_date=ticket_body['flight_date'],
        total_fare=float(ticket_body['total_fare']),
        travel_duration=ticket_body['travel_duration'],
        total_travel_distance=float(ticket_body['total_travel_distance']),
        is_refundable= ticket_body['is_refundable'],
        is_non_stop=ticket_body['is_non_stop']
    )

    airlines = []
    for airline_body in airlines_body:
        airline = Airline(
            airline_code=airline_body["airline_code"],
            airline_name = airline_body["airline_name"]
        )

        airlines.append(airline)

        ranking_insertion_airline_price = RankingInsertionRequest(ticket.leg_id, airline.airline_code, ticket.total_fare) 

        # Add the airline price to the ranking database
        airline_price_response = database_ranking_client.AddAirlinePrice(ranking_insertion_airline_price)

        if airline_price_response == "error":
            return "Error adding airline price to the ranking database"

    visualization_insertion_request = VisualizationInsertionRequest(ticket=ticket, airlines=airlines)

    # Add the ticket to the tickets database
    tickets_response = database_visualization_client.AddTicket(visualization_insertion_request)

    if tickets_response == "error":
        return "Error adding ticket to the visualization database"

    return "Ticket added successfully"

@app.route("/api/management/tickets/<leg_id>", methods=['DELETE'])
def delete_ticket(leg_id):
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