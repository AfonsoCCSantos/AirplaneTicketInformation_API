from flask import Flask, redirect, render_template, session, url_for, make_response
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

# AUTH0_CLIENT_ID="oyp940gN2eaffEZjgdHvFKSCfprngFmY"
# AUTH0_CLIENT_SECRET="_bb5JwYk_enfIaVrWt9kKqLDcwWSKAt--zLDHJAZOULdrnMwmrgtjD3FJhITSRAz"
# AUTH0_DOMAIN="dev-yq8vieybb3gnrzif.eu.auth0.com"
APP_SECRET_KEY = env.get("APP_SECRET_KEY")

AUTH0_DOMAIN = env.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = env.get("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = env.get("AUTH0_CLIENT_SECRET")

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

@app.route("/api/authentication/see_id")
def see_token():
    response = make_response()
    response.set_cookie("user_id", session["user"]["userinfo"]["sub"])
    return response

@app.route("/api/authentication/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("/api/authentication/callback", _external=True)
    )

@app.route("/api/authentication/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/api/authentication/see_id")

@app.route("/api/authentication/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/api/authentication/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@app.route("/api/authentication/liveness-check", methods=['GET'])
def liveness_check():
    return "ok",200