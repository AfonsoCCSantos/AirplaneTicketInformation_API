from flask import Flask
import grpc
import os
import time
import random
import psutil

from ranking_pb2 import AirlinesRankingByTicketPriceRequest, AirlineAveragePrice
from ranking_pb2_grpc import RankingStub
from prometheus_client import start_http_server, Summary, Histogram, CONTENT_TYPE_LATEST, generate_latest, Counter, Gauge

app = Flask(__name__)

# Connect to the database ranking service
database_ranking_host = os.getenv("DATABASE_RANKING_HOST", "localhost")
database_ranking_channel = grpc.insecure_channel(f"{database_ranking_host}:50052")
database_ranking_client = RankingStub(database_ranking_channel)

# metrics
request_counter = Counter("requests_counter_ranking", "Total number of requests of ranking")
cpu_usage = Gauge('cpu_usage_percent_ranking', 'CPU Usage Percentage of ranking')

@app.route("/api/ranking/airlines_by_ticket_price", methods=['GET'])
def get_ranking_airlines_ticket_pricing():
    request_counter.inc(1)
    airline_ranking_request = AirlinesRankingByTicketPriceRequest()

    airline_ranking_response = database_ranking_client.GetAirlinesRankingByTicketPrice(airline_ranking_request)
    
    return f"ranking of airlines: {airline_ranking_response.airlines}"

@app.route("/api/ranking/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200

@app.route("/metrics", methods=['GET'])
def prometheus_metrics():
    cpu_usage.set(psutil.cpu_percent())
    return generate_latest()