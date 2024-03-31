from flask import Flask
import grpc
import os

from ranking_pb2 import AirlinesRankingByTicketPriceRequest, AirlineAveragePrice
from ranking_pb2_grpc import RankingStub

app = Flask(__name__)

# Connect to the database ranking service
database_ranking_host = os.getenv("DATABASE_RANKING_HOST", "localhost")
database_ranking_channel = grpc.insecure_channel("localhost:50052")
database_ranking_client = RankingStub(database_ranking_channel)

@app.route("/api/ranking/airlines_by_ticket_price", methods=['GET'])
def get_ranking_airlines_ticket_pricing():
    airline_ranking_request = AirlinesRankingByTicketPriceRequest()

    airline_ranking_response = database_ranking_client.GetAirlinesRankingByTicketPrice(airline_ranking_request)
    
    return f"ranking of airlines: {airline_ranking_response.airlines}"