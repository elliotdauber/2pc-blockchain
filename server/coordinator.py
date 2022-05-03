from w3connection import W3HTTPConnection
from contract import Contract
import grpc
import _grpc.tpc_pb2_grpc
from concurrent import futures
from systemconfig import SYSCONFIG

class Coordinator():
    def __init__(self, contract_file, w3):
        self.contract = Contract(contract_file, w3)
        self.w3 = w3 #TODO: rethink this abstraction
        self.nodes = SYSCONFIG.nodes
        
    def serve(self):
        # Initialize the server
        print("STARTING SERVER")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.tpc_pb2_grpc.add_CoordinatorServicer_to_server(
            CoordinatorGRPC(), server)
        server.add_insecure_port("localhost:8888\0")
        server.start()
        server.wait_for_termination()

    def request(self):
        timeout = 10
        self.contract.functions.request(len(self.nodes), timeout).transact()
        pass

    def send_msg(self, msg, node):
        pass

    def print_num_deployments(self):
        print(self.contract.num_deployments())

    def deploy(self):
        print("deploying contract index " + str(self.contract.num_deployments))
        contract = self.contract.deploy()
        return contract.address


#TODO: pk empty string should be an error
#TODO: abstract out the logic that determines if a node should accept certain data (for tx in work section)
class CoordinatorGRPC(_grpc.tpc_pb2_grpc.CoordinatorServicer):
    def SendWork(self, request, context):
        work = request.work
        if len(work) == 0:
            return _grpc.tpc_pb2.WorkResponse(success="no work given, operation aborted")

        address = C.deploy()
        for node in SYSCONFIG.nodes:
            with grpc.insecure_channel(node.url) as channel:
                stub = _grpc.tpc_pb2_grpc.NodeStub(channel)
                node_request = _grpc.tpc_pb2.WorkRequest(address=address)

                for tx in work:
                    pk = tx.pk
                    if pk == "":
                        continue
                    first = pk[0].lower()
                    if node.pk_range[0] <= first <= node.pk_range[1]:
                        node_request.work.append(tx)

                if len(node_request.work) > 0:
                    retval = stub.ReceiveWork(node_request)
                    print(retval)

        response = _grpc.tpc_pb2.WorkResponse(success="this was a success!")
        return response


C = None

def coordinator():
    global C
    print("starting up the coordinator...")
    source = "contracts/TPC.sol"
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    C = Coordinator(source, w3.w3)
    C.serve()
    return C


coordinator()