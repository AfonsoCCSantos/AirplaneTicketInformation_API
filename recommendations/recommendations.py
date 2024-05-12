from flask import Flask, redirect, render_template, session, url_for, request
from authlib.integrations.flask_oauth2 import ResourceProtector
from validator import Auth0JWTBearerTokenValidator
import os
import jwt
import requests
import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

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

@app.route("/api/recommendations/cheapest_airline/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
def get_chepeast_airline(departure, arrival, start_date, end_date):

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

    return "recommendation of the cheapest airline"

@app.route("/api/recommendations/cheapest_date/<departure>/<arrival>/<start_date>/<end_date>", methods=["GET"])
def get_chepeast_date(departure, arrival, start_date, end_date):
    
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

    return "recommendation for the cheapest date to fly"

@app.route("/api/recommendations/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200

