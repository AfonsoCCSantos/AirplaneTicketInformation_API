from flask import Flask
import time
import random
import psutil
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import col

from prometheus_client import start_http_server, Summary, Histogram, CONTENT_TYPE_LATEST, generate_latest, Counter, Gauge
from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexerModel, VectorAssembler
from pyspark.ml.regression import LinearRegressionModel
import numpy
from datetime import datetime, timedelta

# create a SparkSession
spark = SparkSession.builder.getOrCreate()

# Load the saved models
model = LinearRegressionModel.load("/forecast/ml_models/ticket_price_pred")
flightDateModel = StringIndexerModel.load("/forecast/ml_models/flightDateModel")
startingAirportModel = StringIndexerModel.load("/forecast/ml_models/startingAirportModel")
destinationAirportModel = StringIndexerModel.load("/forecast/ml_models/destinationAirportModel")


app = Flask(__name__)

# metrics
request_counter = Counter("requests_counter_forecast", "Total number of requests of forecast")
cpu_usage = Gauge('cpu_usage_percent_forecast', 'CPU Usage Percentage of forecast')
memory_usage = Gauge('memory_usage_percent_forecast', 'Memory Usage Percentage of forecast')

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

    predictions = model.transform(data_3)

    return predictions.first()[-1]

@app.route("/api/forecast/chepeast/<departure>/<arrival>/<start_date>/<end_date>", methods=['GET'])
def forecast_cheapest(departure, arrival, start_date, end_date):
    request_counter.inc(1)
    res = pred_ticket_price_in_date_start_end_airport(start_date, departure, arrival)
    curr_date = get_next_day(start_date)

    while curr_date != get_next_day(end_date):
        price = pred_ticket_price_in_date_start_end_airport(curr_date, departure, arrival)
        res = price if price < res else res

        curr_date = get_next_day(curr_date)

    return f"forecast of cheapest ticket: {res}"

@app.route("/api/forecast/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200

@app.route("/metrics", methods=['GET'])
def prometheus_metrics():
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)
    return generate_latest() 