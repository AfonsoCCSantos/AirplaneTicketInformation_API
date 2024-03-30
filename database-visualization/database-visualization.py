import grpc
from concurrent import futures
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from protobufs.compiled.visualization_pb2 import (
    Ticket,
    Airline,
    TicketsResponse,
    AirlineResponse,
)
import protobufs.compiled.visualization_pb2_grpc as visualization_pb2_grpc

class DatabaseVisualizationService(visualization_pb2_grpc.VisualizationServicer):
    def GetTickets(self, request, context):
        
        return TicketsResponse(tickets=None)
        
    def GetAirline(self, request, context):

        return AirlineResponse(airline = None)
        
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    visualization_pb2_grpc.add_RecommendationsServicer_to_server(
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


if __name__ == "__main__":
    serve()
