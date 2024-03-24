from flask import Flask

app = Flask(__name__)

@app.route("api/recommendations/cheapest_airline/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
def get_chepeast_airline(departure, arrival, start_date, end_date):
    return "recommendation of the cheapest airline"

@app.route("api/recommendations/cheapest_date/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
def get_chepeast_date(departure, arrival, start_date, end_date):
    return "recommendation for the cheapest date to fly"