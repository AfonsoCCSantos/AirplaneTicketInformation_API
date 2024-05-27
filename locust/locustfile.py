from locust import HttpUser, task

# locust in /home/alexandrerafaof/.local/lib/python3.10/site-packages (1a linha que aparece no pip3 install)

class HelloWorldUser(HttpUser):
    @task
    def view_airline(self):
        self.client.get("/api/visualization/airlines/DL")

    @task
    def view_ranking(self):
        self.client.get("/api/ranking/airlines_by_ticket_price")