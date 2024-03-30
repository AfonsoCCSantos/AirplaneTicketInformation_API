from flask import Flask

app = Flask(__name__)

@app.route("/api/visualization/tickets/<departure>/<arrival>", method=["GET"])
def get_tickets_from_to(departure, arrival):
    return "list of tickets"

@app.route("/api/visualization/airlines/<airline_code>", method=["GET"])
def get_airline_details(airline_code):
    return "list of tickets"