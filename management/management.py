from flask import Flask

app = Flask(__name__)

@app.route("/api/management/tickets", methods=['POST'])
def add_tickets():
    return "adds a new ticket"

@app.route("/api/management/tickets/<ticketId>", methods=['DELETE'])
def delete_ticket(ticketId):
    return "deletes a ticket"