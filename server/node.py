from dynamo import table1, table2, tables
import sys
from w3connection import W3HTTPConnection
import grpc
import _grpc.tpc_pb2_grpc
from concurrent import futures
from systemconfig import SYSCONFIG

def dynamotest():
    print("tables:")
    print(table1.creation_date_time)
    print(table2.creation_date_time)

class Node:
    def __init__(self, w3, nodeid):
        self.table = SYSCONFIG.nodes[nodeid]["table"]
        self.w3 = w3
        self.contract = None #TOOD: get contract from coordinator? how does this work?
        self.id = nodeid
        self.working_pk = set()

    def serve(self):
        # Initialize the server
        print("STARTING NODE SERVER")
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.tpc_pb2_grpc.add_NodeServicer_to_server(
            NodeGRPC(), server)
        server.add_insecure_port(SYSCONFIG.nodes[self.id]["url"])
        server.start()
        server.wait_for_termination()

    def can_transact(self, work):
        return all([action.pk not in self.working_pk for action in work])

    def voter(self, vote):
        state = "COMMIT"  # self.contract.functions.voter(1).transact()
        if state == "COMMIT":
            pass
            #TODO
        elif state == "VOTING":
            pass
            #TODO

    def verdict(self):
        state = self.contract.functions.verdict.transact()
        if state == "ABORT":
            pass
            #TODO

class NodeGRPC(_grpc.tpc_pb2_grpc.NodeServicer):
    def ReceiveWork(self, request, context):
        work = request.work
        print("printing work for node: ")
        print(request.address)
        for tx in work:
            print(tx)
        print("done printing work for node")
        response = _grpc.tpc_pb2.WorkResponse(success="from node, this was a success!")
        if N.can_transact(request.work):
            N.voter(True)
        else:
            N.voter(False)
        return response


N = None

def node(index):
    global N
    print("starting up a node...")
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    N = Node(w3.w3, index)
    N.serve()
    return N


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    assert(0 <= index < len(SYSCONFIG.nodes))
    node(index)


if __name__ == "__main__":
    main()

# example contract calls:
# # read state:
#     # state = contract_instance.functions.getState().call()
#     # print(state)
#     # # 42
#     #
#     # contract_instance.functions.request([], 42).transact({'from': eth.default_account})
#     # state = contract_instance.functions.getState().call()
#     # print(state)
