import sys
from w3connection import W3HTTPConnection
import grpc
import _grpc.tpc_pb2_grpc
from concurrent import futures
from systemconfig import SYSCONFIGX
from contract import Contract

class XNode:
    def __init__(self, w3, config, contract_file):
        self.contract = Contract(contract_file, w3)
        self.nodes = SYSCONFIGX.nodes

        self.config = config
        self.w3 = w3
        self.working_contracts = []
        self.working_pk = set()

    # NODE FUNCTIONS

    def serve(self):
        # Initialize the server
        print("STARTING XNODE SERVER " + str(self.config.id) + " @ " + self.config.url)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.tpc_pb2_grpc.add_XNodeServicer_to_server(
            XNodeGRPC(self), server)
        server.add_insecure_port(self.config.url)
        server.start()
        server.wait_for_termination()

    def can_transact(self, work):
        return all([action.pk not in self.working_pk for action in work])

    #TODO: add address param
    def voter(self, vote):
        state = "COMMIT"  # self.contract.functions.voter(1).transact()
        if state == "COMMIT":
            pass
            #TODO
        elif state == "VOTING":
            pass
            #TODO

    def verdict(self, address, vote):
        state = self.contract.functions.verdict.transact()
        if state == "ABORT":
            pass
            #TODO

    #logic: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
    def transact(self, tx):
        table = self.config.table
        action = tx.action[0] if tx.action != "" else ""
        if tx.access == "read":
            response = table.get_item(
                Key = {
                    "pk": tx.pk
                }
            )
            if tx.column == "":
                return response['Item']
            return response['Item'][tx.column] if tx.column in response['Item'] else None
        elif tx.access == "write":
            if action == "&":
                response = table.put_item(
                    Key={
                        "pk": tx.pk,
                        "balance": 0
                    }
                )
            elif action == "~":
                response = table.delete_item(
                    Key={
                        "pk": tx.pk
                    }
                )
            elif action == '+':
                # TODO: add operation (make sure column is int first)
                pass
            elif action == '-':
                # TODO: subtract operation (make sure column is int first)
                pass



    # COORDINATOR FUNCTIONS

    def request(self, address):
        timeout = 10
        self.contract.functions.request(len(self.nodes), timeout).transact()
        pass

    def deploy(self):
        contract = self.contract.deploy()
        return contract.address




class XNodeGRPC(_grpc.tpc_pb2_grpc.XNodeServicer):
    def __init__(self, xnode):
        super().__init__()
        self.xnode = xnode

    def ReceiveWork(self, request, context):
        work = request.work
        print("printing work for node: ")
        print(request.address)
        for tx in work:
            print(tx)
        print("done printing work for node")
        response = _grpc.tpc_pb2.WorkResponse(success="from node, this was a success!")
        if self.xnode.can_transact(request.work):
            self.xnode.voter(True)
        else:
            self.xnode.voter(False)
        return response

    def SendWork(self, request, context):
        work = request.work
        if len(work) == 0:
            return _grpc.tpc_pb2.WorkResponse(success="no work given, operation aborted")

        address = self.xnode.deploy()
        for node in SYSCONFIGX.nodes:
            with grpc.insecure_channel(node.url) as channel:
                stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
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


def run_xnode(config):
    print("starting up a node...")
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    source = "contracts/TPC.sol"
    X = XNode(w3.w3, config, source)
    X.serve()
    return X


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    assert(0 <= index < len(SYSCONFIGX.nodes))
    run_xnode(SYSCONFIGX.nodes[index])


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
