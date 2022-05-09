import sys
from w3connection import W3HTTPConnection
import grpc
import _grpc.tpc_pb2_grpc
from concurrent import futures
from systemconfig import SYSCONFIGX
from contract import Contract
from colorama import Style

color = ""

def cprint(msg):
    print(color + str(msg) + Style.RESET_ALL)


class XNode:
    def __init__(self, w3, config, contract_file):
        self.contract = Contract(contract_file, w3)
        self.nodes = SYSCONFIGX.nodes

        self.config = config
        self.w3 = w3
        self.working_contracts = {}
        self.coordinating_contracts = {}
        self.working_pk = set()

    # NODE FUNCTIONS

    def serve(self):
        # Initialize the server
        cprint("STARTING XNODE SERVER " + str(self.config.id) + " @ " + self.config.url)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.tpc_pb2_grpc.add_XNodeServicer_to_server(
            XNodeGRPC(self), server)
        server.add_insecure_port(self.config.url)
        server.start()
        server.wait_for_termination()

    def log(self, text):
        with open(self.config.logfile, "a+") as f:
            f.write(text + "\n")

    def can_transact(self, work):
        return all([action.pk not in self.working_pk for action in work])

    def voter(self, address, vote):
        contract = self.working_contracts.get(address)["contract"]
        if contract is None:
            return
        cprint("VOTING " + str(vote) + " on contract " + address)
        tx_hash = contract.functions.voter(vote, self.config.id).transact()
        # self.w3.eth.wait_for_transaction_receipt(tx_hash) #TODO: maybe don't wait?


    def verdict(self, address, vote):
        contract = self.working_contracts.get(address)["contract"]
        if contract is None:
            return
        tx_hash = contract.functions.verdict.transact()
        # self.w3.eth.wait_for_transaction_receipt(tx_hash) #TODO: maybe dont wait?

    #logic: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
    def transact(self, tx):
        table = self.config.table
        action = tx.action[0] if tx.action != "" else ""
        if tx.access == "read":
            response = table.get_item(
                Key={
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

    def request(self, address, num_nodes, timeout):
        contract = self.coordinating_contracts.get(address)["contract"]
        tx_hash = contract.functions.request(num_nodes, timeout).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        pass




class XNodeGRPC(_grpc.tpc_pb2_grpc.XNodeServicer):
    def __init__(self, xnode):
        super().__init__()
        self.xnode = xnode

    def ReceiveWork(self, request, context):
        work = request.work
        address = request.address
        self.xnode.log(address) #TODO: log work too
        cprint(request.address)
        for tx in request.work:
            cprint(tx)

        contract = self.xnode.w3.eth.contract(address=address, abi=self.xnode.contract.abi)
        self.xnode.working_contracts[address] = {
            "contract": contract,
            "work": work
        }
        if self.xnode.can_transact(work):
            self.xnode.voter(address, 1)
        else:
            self.xnode.voter(address, 0)

        response = _grpc.tpc_pb2.WorkResponse()
        return response



    def SendWork(self, request, context):
        work = request.work
        if len(work) == 0:
            return _grpc.tpc_pb2.WorkResponse(error="no work given, operation aborted")

        address = self.xnode.contract.deploy()
        cprint("deployed at address " + address)

        # figuring out where to send the data
        to_send = {} # node.url to WorkRequest
        for node in SYSCONFIGX.nodes:
            node_request = _grpc.tpc_pb2.WorkRequest(address=address)

            for tx in work:
                pk = tx.pk
                if pk == "":
                    continue
                first = pk[0].lower()
                if node.pk_range[0] <= first <= node.pk_range[1]:
                    node_request.work.append(tx)

            if len(node_request.work) > 0:
                to_send[node.url] = node_request

        for url, request in to_send.items():
            with grpc.insecure_channel(url) as channel:
                stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
                retval = stub.ReceiveWork(request)
                cprint(retval)

        # store contract
        contract = self.xnode.w3.eth.contract(address=address, abi=self.xnode.contract.abi)
        self.xnode.coordinating_contracts[address] = {
            "contract": contract,
            "work": work
        }

        timeout = 5
        self.xnode.request(address, len(to_send), timeout)

        response = _grpc.tpc_pb2.WorkResponse(address=address, timeout=timeout)
        return response


def run_xnode(config):
    cprint("starting up a node...")
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    source = "contracts/TPC.sol"
    X = XNode(w3.w3, config, source)
    X.serve()
    return X


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    assert(0 <= index < len(SYSCONFIGX.nodes))
    global color
    color = SYSCONFIGX.nodes[index].color
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
