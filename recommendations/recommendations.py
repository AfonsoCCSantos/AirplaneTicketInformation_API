from flask import Flask, redirect, render_template, session, url_for, request
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import Auth0JWTBearerTokenValidator
import os
import jwt
import requests
import json
from urllib.parse import quote_plus, urlencode
import time
import random
import psutil

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from prometheus_client import start_http_server, Summary, Histogram, CONTENT_TYPE_LATEST, generate_latest, Counter, Gauge

from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import col

from prometheus_client import start_http_server, Summary, Histogram, CONTENT_TYPE_LATEST, generate_latest, Counter, Gauge
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexerModel, VectorAssembler
from pyspark.ml.regression import LinearRegressionModel
from datetime import datetime, timedelta

# AUTH0_CLIENT_ID="oyp940zif.eu.auth0.com"
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
request_counter = Counter("requests_counter_recommendations", "Total number of requests of recommendations")
cpu_usage = Gauge('cpu_usage_percent_recommendations', 'CPU Usage Percentage of recommendations')
memory_usage = Gauge('memory_usage_percent_recommendations', 'Memory Usage Percentage of recommendations')

# create a SparkSession
spark = SparkSession.builder.getOrCreate()
# models
airline_pred_model = LinearRegressionModel.load("/recommendations/ml_models/airline_price_pred")
ticket_price_model = LinearRegressionModel.load("/recommendations/ml_models/ticket_price_pred")
flightDateModel = StringIndexerModel.load("/recommendations/ml_models/flightDateModel")
startingAirportModel = StringIndexerModel.load("/recommendations/ml_models/startingAirportModel")
destinationAirportModel = StringIndexerModel.load("/recommendations/ml_models/destinationAirportModel")
assembler = VectorAssembler(inputCols=["flightDate_indexed", "startingAirport_indexed", "destinationAirport_indexed"], outputCol="features")
assembler_airlines = VectorAssembler(inputCols=[ "totalFare","flightDate_indexed", "startingAirport_indexed", "destinationAirport_indexed"], outputCol="features")

airlines_mapper = {
    0:"UA",
    1:"DL",
    2:"AA",
    3:"NK",
    4:"B6",
    5:"AS",
    6:"F9",
    7:"SY",
    8:"9K",
    9:"9X",
    10:"4B",
    11:"LF",
    12:"KG",
    13:"HA"
}

def get_next_day(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    next_day_obj = date_obj + timedelta(days=1)
    next_day_str = next_day_obj.strftime('%Y-%m-%d')
    return next_day_str


def pred_ticket_price_in_date_start_end_airport(date, startingAirport, destinationAirport):
    assembler = VectorAssembler(inputCols=["flightDate_indexed", "startingAirport_indexed", "destinationAirport_indexed"], outputCol="features")
    df = spark.createDataFrame([{"flightDate": date, "startingAirport": startingAirport, "destinationAirport": destinationAirport}])

    # Apply the same StringIndexer models
    fdJob = flightDateModel.transform(df)
    saJob = startingAirportModel.transform(fdJob)
    daJob = destinationAirportModel.transform(saJob)

    data_3 = assembler.transform(daJob)

    predictions = ticket_price_model.transform(data_3)

    return predictions.first()[-1]

def pred_airline_based_in_price_date_start_end_airport(date, startingAirport, destinationAirport,price):
    df = spark.createDataFrame([{"flightDate": date, "startingAirport": startingAirport, "destinationAirport": destinationAirport, "totalFare": price}])

    fdJob = flightDateModel.transform(df)
    saJob = startingAirportModel.transform(fdJob)
    daJob = destinationAirportModel.transform(saJob)

    data_3 = assembler_airlines.transform(daJob)

    predictions = airline_pred_model.transform(data_3)

    airline_nmbr = round(float(predictions.first()[-1]))
    return airlines_mapper[airline_nmbr]

@app.route("/api/recommendations/cheapest_airline/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
def get_chepeast_airline(departure, arrival, start_date, end_date):
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

    hasPermission = response[0]['name'] in ['subscriber', 'admin']

    if not hasPermission:
        return "Not authorized", 401

    res = pred_ticket_price_in_date_start_end_airport(start_date, departure, arrival)
    curr_date = get_next_day(start_date)

    while curr_date != get_next_day(end_date):
        price = pred_ticket_price_in_date_start_end_airport(curr_date, departure, arrival)
        res = price if price < res else res

        curr_date = get_next_day(curr_date)
    
    final_airline = pred_airline_based_in_price_date_start_end_airport(start_date, departure, arrival, res)
    return f"recommendation of the cheapest airline: {final_airline}"

@app.route("/api/recommendations/cheapest_date/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
def get_chepeast_date(departure, arrival, start_date, end_date):
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

    hasPermission = response[0]['name'] in ['subscriber', 'admin']

    if not hasPermission:
        return "Not authorized", 401

    res = pred_ticket_price_in_date_start_end_airport(start_date, departure, arrival)
    date = start_date

    curr_date = get_next_day(start_date)

    while curr_date != get_next_day(end_date):
        price = pred_ticket_price_in_date_start_end_airport(curr_date, departure, arrival)
        if price < res:
            res = price
            date = curr_date

        curr_date = get_next_day(curr_date)
    
    return f"recommendation for the cheapest date to fly: {date}"

@app.route("/api/recommendations/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200


@app.route("/metrics", methods=['GET'])
def prometheus_metrics():
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    return generate_latest() 
