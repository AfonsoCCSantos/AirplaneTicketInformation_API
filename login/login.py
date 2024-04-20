from flask import Flask, redirect, render_template, session, url_for, make_response
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

# AUTH0_CLIENT_ID="oyp940gN2eaffEZjgdHvFKSCfprngFmY"
# AUTH0_CLIENT_SECRET="_bb5JwYk_enfIaVrWt9kKqLDcwWSKAt--zLDHJAZOULdrnMwmrgtjD3FJhITSRAz"
# AUTH0_DOMAIN="dev-yq8vieybb3gnrzif.eu.auth0.com"
APP_SECRET_KEY="699b3d871c8e5daa1cd5a2bf6e2b9bf436a05b469bc61885a6a9c5026b71047c"

AUTH0_DOMAIN="tomasbarreto.eu.auth0.com"
AUTH0_CLIENT_ID="IEvRaY6CXjAAT4UElgICkfN12DydX71a"
AUTH0_CLIENT_SECRET="CpYur9-495GPTSc-rxT-NPoDm1rZ7uASFrdlWwDiTkcAyFns2utviMIh7Kq1BgAA"

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

@app.route("/see_id")
def see_token():
    response = make_response()
    response.set_cookie("user_id", session["user"]["userinfo"]["sub"])
    return response

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/see_id")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )