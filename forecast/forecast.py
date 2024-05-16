from flask import Flask
import time
import random
import psutil

from prometheus_client import start_http_server, Summary, Histogram, CONTENT_TYPE_LATEST, generate_latest, Counter, Gauge

app = Flask(__name__)

request_counter = Counter("requests_counter_forecast", "Total number of requests of forecast")
cpu_usage = Gauge('cpu_usage_percent_forecast', 'CPU Usage Percentage of forecast')

@app.route("/api/forecast/chepeast/<departure>/<arrival>/<start_date>/<end_date>", methods=['GET'])
def forecast_cheapest(departure, arrival, start_date, end_date):
    request_counter.inc(1)
    return "forecast of cheapest ticket"

@app.route("/api/forecast/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200

@app.route("/metrics", methods=['GET'])
def prometheus_metrics():
    cpu_usage.set(psutil.cpu_percent())
    return generate_latest() 