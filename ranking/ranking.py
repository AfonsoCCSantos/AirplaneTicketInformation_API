from flask import Flask

app = Flask(__name__)

@app.route("/api/ranking/airlines_by_ticket_price", methods=['GET'])
def get_ranking_airlines_ticket_pricing():
    return "list of airlines ranked by ticket price"