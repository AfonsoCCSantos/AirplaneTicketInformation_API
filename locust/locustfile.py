from locust import HttpUser, task

class SystemTestUser(HttpUser):
    @task
    def view_airline(self):
        self.client.get("/api/visualization/airlines/DL")

    @task
    def view_ranking(self):
        self.client.get("/api/ranking/airlines_by_ticket_price")
    
    # @task
    # def view_forecast(self):
    #     self.client.get("/api/forecast/chepeast/BOS/ATL/2024-08-10/2024-08-20")