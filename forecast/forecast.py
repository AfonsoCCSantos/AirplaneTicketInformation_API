from flask import Flask

app = Flask(__name__)

@app.route("/api/forecast/chepeast/<departure>/<arrival>/<start_date>/<end_date>", methods=['GET'])
def forecast_cheapest(departure, arrival, start_date, end_date):
    return "forecast of cheapest ticket"