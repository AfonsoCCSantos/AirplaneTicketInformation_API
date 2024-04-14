from flask import Flask
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "tomasbarreto.eu.auth0.com",
    "https://localhost:8084"
)
require_auth.register_token_validator(validator)

app = Flask(__name__)

@app.route("/api/recommendations/cheapest_airline/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
@require_auth("subscriber")
def get_chepeast_airline(departure, arrival, start_date, end_date):
    return "recommendation of the cheapest airline"

@app.route("/api/recommendations/cheapest_date/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
@require_auth("subscriber")
def get_chepeast_date(departure, arrival, start_date, end_date):
    return "recommendation for the cheapest date to fly"