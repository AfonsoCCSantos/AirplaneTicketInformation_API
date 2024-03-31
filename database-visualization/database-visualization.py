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
        SELECT legId, startingAirport, destinationAirport, CAST(flightDate AS STRING) AS date,
                     totalFare, travelDuration, totalTravelDistance, isRefundable, isNonStop
        FROM visualization.tickets t
        WHERE t.startingAirport='{departure_place}' AND t.destinationAirport='{arrival_place}'
        """

        query_job = client.query(query)
        results = list(query_job.result())

        for row in results:
            ticket = Ticket(
                leg_id = row.legId,
                departure_place = departure_place,
                arrival_place = arrival_place,
                flight_date = row.date,
                total_fare = row.totalFare,
                travel_duration = row.travelDuration,
                total_travel_distance = row.totalTravelDistance,
                is_refundable = row.isRefundable,
                is_non_stop = row.isNonStop
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
        result = list(query_job.result())[0]

        airline = Airline(
            airline_code = result.airlineCode,
            airline_name = result.airlineName
        )
        
        return AirlineResponse(airline = airline)
    
    def AddTicket(self, request, context):
        ticket = request.ticket

        query = f"""
            INSERT INTO 
            visualization.tickets (legId, startingAirport, destinationAirport, flightDate, totalFare, 
                                    travelDuration, totalTravelDistance, isRefundable, isNonStop)
            VALUES 
                ('{ticket.leg_id}', '{ticket.departure_place}', '{ticket.arrival_place}', '
                    {ticket.flight_date}', {ticket.total_fare}, {ticket.travel_duration}, 
                    {ticket.total_travel_distance}, {ticket.is_refundable}, {ticket.is_non_stop})
        """

        query_job = client.query(query)
        results = query_job.result()

        print(results)


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
