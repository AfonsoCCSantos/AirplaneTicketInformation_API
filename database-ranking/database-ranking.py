import grpc
from concurrent import futures
from google.cloud import bigquery
from google.oauth2 import service_account
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from ranking_pb2 import (
    AirlineAveragePrice,
    AirlinesRankingByTicketPriceResponse,
    RankingInsertionResponse,
    RankingDeleteResponse
)
import ranking_pb2_grpc as ranking_pb2_grpc

class DatabaseRankingService(ranking_pb2_grpc.RankingServicer):
    global client 
    

    def GetAirlinesRankingByTicketPrice(self, request, context):
        airlines = []

        query = f"""
            SELECT airlineCode, AVG(totalFare) as averagePrice
            FROM ranking.ranking r
            GROUP BY airlineCode
            ORDER BY averagePrice
        """

        query_job = client.query(query)
        results = query_job.result()

        for row in results:
            airline = AirlineAveragePrice(
                airline_code=row.airlineCode,
                average_price=row.averagePrice
            )

            airlines.append(airline)
        
        return AirlinesRankingByTicketPriceResponse(airlines=airlines)

    def AddAirlinePrice(self, request, context):
        airlines = request.airlines
        airlines_price_row_to_insert = []

        for airline in airlines:
            airlines_price_row_to_insert.append({"airlineCode": airline.airline_code, "leg_id": request.leg_id, "totalFare": request.price})

        errors = client.insert_rows_json("ranking.ranking", airlines_price_row_to_insert)
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting row: {}".format(errors))   
        
        return RankingInsertionResponse(query_status = "done")

    def DeleteTicket(self, request, context) : # Need to add leg_id collumn to the table
        leg_id = request.leg_id

        delete_ticket_query = f"""
        DELETE FROM ranking.ranking t WHERE t.leg_id = '{leg_id}'
        """

        query_job = client.query(delete_ticket_query)
        results = query_job.result()

        return RankingDeleteResponse(query_status = "done")



def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    ranking_pb2_grpc.add_RankingServicer_to_server(
        DatabaseRankingService(), server
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
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

client = None
if __name__ == "__main__":
    credentials = service_account.Credentials.from_service_account_file(filename="ranking_key.json")
    client = bigquery.Client(credentials=credentials)
    serve()
