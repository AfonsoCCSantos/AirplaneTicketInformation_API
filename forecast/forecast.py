from flask import Flask

app = Flask(__name__)

@app.route("/api/forecast/chepeast/<departure>/<arrival>/<start_date>/<end_date>", methods=['GET'])
def forecast_cheapest(departure, arrival, start_date, end_date):
    return "forecast of cheapest ticket"

@app.route("/api/forecast/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200