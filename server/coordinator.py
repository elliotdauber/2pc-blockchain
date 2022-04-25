from w3connection import W3HTTPConnection
from contract import Contract
import grpc
import _grpc.helloworld_pb2_grpc
from concurrent import futures

class Coordinator():
    def __init__(self, contract_file, w3, num_nodes):
        self.contract = Contract(contract_file, w3)
        self.w3 = w3 #TODO: rethink this abstraction
        self.num_nodes = num_nodes
        self.serve()
        
    def serve(self):
        # Initialize the server
        print("STARTING SERVER")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.helloworld_pb2_grpc.add_CoordinatorServicer_to_server(
            CoordinatorGRPC(), server)
        server.add_insecure_port("localhost:8888\0")
        server.start()
        server.wait_for_termination()

    def run(self):
        print("deploying contract index " + str(self.contract.num_deployments))
        self.contract.deploy()

    def request(self):
        timeout = 10
        self.contract.functions.request(self.num_nodes, timeout).transact()
        pass

    def send_msg(self, msg, node):
        pass

    def print_num_deployments(self):
        print(self.contract.num_deployments())

class CoordinatorGRPC(_grpc.helloworld_pb2_grpc.CoordinatorServicer):

    def SendWork(self, request, context):
        # TODO: Send Work to Noodes
        print(request.work, request.address)
        response = _grpc.helloworld_pb2.WorkResponse(success="this was a success!")
        return response

def coordinator(numNodes):
    print("starting up the coordinator...")
    source = "contracts/TPC.sol"
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    C = Coordinator(source, w3.w3, numNodes)
    C.run()
    return C


coordinator(2)