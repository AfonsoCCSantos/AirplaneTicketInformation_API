import grpc
from concurrent import futures
from google.cloud import bigquery
from google.oauth2 import service_account
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from visualization_pb2 import (
    Ticket,
    Airline,
    TicketsResponse,
    AirlineResponse,
)
import visualization_pb2_grpc as visualization_pb2_grpc

class DatabaseVisualizationService(visualization_pb2_grpc.VisualizationServicer):
    global client 
    
    def GetTickets(self, request, context):
        departure_place = request.departure_place
        arrival_place = request.arrival_place
        tickets = []

        query= f"""
        SELECT *
        FROM visualization.tickets t
        WHERE t.departurePlace='{departure_place}' AND t.arrivalPlace='{arrival_place}'
        """

        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            ticket = Ticket(
                leg_id = row.legId,
                departure_place = departure_place,
                arrival_place = arrival_place,
                flight_date = row.flightDate,
                total_fare = row.totalFare,
                airline_code = row.airlineCode             
            )
            tickets.append(ticket)

        return TicketsResponse(tickets=tickets)
        
    def GetAirline(self, request, context):
        airline_code = request.airline_code

        query= f"""
            SELECT *
            FROM visualization.airlines a
            WHERE a.airlineCode='{airline_code}'
        """
        
        query_job = client.query(query)
        result = query_job.result()

        airline = Airline(
            airline_code = result.airlineCode,
            airline_name = result.airlineName
        )
        
        return AirlineResponse(airline = airline)

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    visualization_pb2_grpc.add_VisualizationServicer_to_server(
        DatabaseVisualizationService(), server
    )

    # with open("server.key", "rb") as fp:
    #     server_key = fp.read()
    # with open("server.pem", "rb") as fp:
    #     server_cert = fp.read()
    # with open("ca.pem", "rb") as fp:
    #     ca_cert = fp.read()

    # creds = grpc.ssl_server_credentials(
    #     [(server_key, server_cert)],
    #     root_certificates=ca_cert,
    #     require_client_auth=True,
    # )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

client = None
if __name__ == "__main__":
    credentials = service_account.Credentials.from_service_account_file(filename="visualization_key.json")
    client = bigquery.Client(credentials=credentials)
    serve()
