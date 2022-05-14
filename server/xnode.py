import sys
from w3connection import W3HTTPConnection
import grpc
import _grpc.tpc_pb2_grpc
from concurrent import futures
from systemconfig import SYSCONFIGX
from contract import Contract
from colorama import Style
import threading
import sqlite3
import time
import hashlib

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
        self.timeout = 10

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
        with open(self.config.logfile, 'a+') as f:
            f.write(text + "\n")

    def can_transact(self, work):
        if all([action.pk not in self.working_pk for action in work]):
            for action in work: 
                self.working_pk.add(action.pk)
            return True
        return False

    def voter(self, address, vote):
        contract = self.working_contracts.get(address)["contract"]
        if contract is None:
            return
        # cprint("VOTING " + str(vote) + " on contract " + address)
        tx_hash = contract.functions.voter(vote, self.config.id).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # return contract.functions.getState().call()


    def verdict(self, address, vote):
        contract = self.working_contracts.get(address)["contract"]
        if contract is None:
            return
        contract.functions.verdict.transact()


    def transact(self, tx, cursor):
        data = []
        for item in cursor.execute(tx.sql):
            data.append(str(item))
        return ";;".join(data)

    def transact_multiple(self, work, access):
        db = sqlite3.connect(self.config.dbfile)
        cursor = db.cursor()
        data = []
        for tx in work:
            data.append(self.transact(tx, cursor))
        db.commit()
        db.close()
        return ";;".join(data)


    def checkTxStatus(self, address):
        working_contract = self.working_contracts.get(address)
        if working_contract is None:
            return
        contract = working_contract["contract"]
        tx_hash = contract.functions.verdict().transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        state = contract.functions.getState().call()
        cprint("xnode " + str(self.config.id) + " found a " + state)
        if state == "COMMIT":
            self.timeout = max(self.timeout-5, 5)
            self.clear_contract(working_contract, address)
            self.transact_multiple(working_contract["work"])
        elif state == "ABORT":
            self.clear_contract(working_contract, address)
        elif state in "TIMEOUT":
            self.timeout = min(2*self.timeout, 5000)
            self.clear_contract(working_contract, address)
            # TODO: You mentioned sending a message to other nodes
            # not sure what youre refering to. I think if we let the node
            # acting as the coordinator set the timeout for any incoming
            # request we can let nodes adjust to the needs of thier respective
            # clients. We also should consider adjusting timeout based
            # on request size
            pass
        
        cprint("xnode " + str(self.config.id) + " has a new timeout of " + str(self.timeout))

    # clean up after work is executed or aborted
    def clear_contract(self, contract, address):
        for action in contract["work"]:
            self.working_pk.discard(action.pk)
        self.working_contracts.pop(address)

    def wait_for_result(self, address, clienturl, access):
        working_contract = self.working_contracts.get(address, None)
        if working_contract is None:
            return "ERROR"
        contract = working_contract["contract"]
        while True:
            status = contract.functions.getState().call()
            if status in ["COMMIT", "ABORT", "TIMEOUT"]:
                self.clear_contract(working_contract, address) 
                data = ""
                if status == "COMMIT":
                    self.timeout = max(self.timeout-5, 5)
                    data = self.transact_multiple(working_contract["work"], access) 
                elif status == "TIMEOUT":
                    self.timeout = min(2*self.timeout, 5000)

                if status in ["COMMIT", "ABORT"]:
                    with grpc.insecure_channel(clienturl) as channel:
                        stub = _grpc.tpc_pb2_grpc.ClientStub(channel)
                        outcome_request = _grpc.tpc_pb2.WorkOutcome(address=address, outcome=status) #TODO: data? only for reads
                        print("ACCESS: ", access)
                        if access == "r":
                            tx_hash = contract.functions.set_data(data).transact()
                            self.w3.eth.wait_for_transaction_receipt(tx_hash)
                            outcome_request.data = data
                        stub.ReceiveOutcome(outcome_request)
                return
            time.sleep(0.25)
            

    # COORDINATOR FUNCTIONS

    def request(self, address, num_nodes):
        contract = self.coordinating_contracts.get(address)["contract"]
        tx_hash = contract.functions.request(num_nodes, self.timeout).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def add_node(self, node):
        for n in self.nodes:
            if n.url == node.url:
                return "URL"
            if n.id == node.id:
                return "ID"
        

class XNodeGRPC(_grpc.tpc_pb2_grpc.XNodeServicer):
    def __init__(self, xnode):
        super().__init__()
        self.xnode = xnode

    def ReceiveWork(self, request, context):
        work = request.work
        address = request.address
        timeout = request.timeout
        self.xnode.log(address)
        self.xnode.log(str(work))
        cprint(request.address)
        for tx in request.work:
            cprint(tx)

        contract = self.xnode.w3.eth.contract(address=address, abi=self.xnode.contract.abi)
        working_contract = {
            "contract": contract,
            "work": work
        }
        self.xnode.working_contracts[address] = working_contract
        self.xnode.voter(address, 1 if self.xnode.can_transact(work) else 0)
        thread = threading.Thread(None, self.xnode.wait_for_result, None, [address, request.clienturl, request.access])
        thread.start()

        return _grpc.tpc_pb2.WorkResponse()

    def SendWork(self, request, context):
        work = request.work
        if len(work) == 0:
            return _grpc.tpc_pb2.WorkResponse(error="no work given, operation aborted")

        address = self.xnode.contract.deploy()
        cprint("deployed at address " + address)

        # figuring out where to send the data
        to_send = {} # node.url to WorkRequest
        empty_string_hash = int(hashlib.sha256(b"").hexdigest(), 16)
        for node in self.xnode.nodes:
            node_request = _grpc.tpc_pb2.WorkRequest(address=address, timeout=self.xnode.timeout, clienturl=request.clienturl, access=request.access)

            for tx in work:
                pk = int(tx.pk, 16)
                if pk == empty_string_hash:
                    node_request.work.append(tx)  # forward no-pk requests to all servers
                    continue
                if node.pk_range[0] <= pk <= node.pk_range[1]:
                    node_request.work.append(tx)
                # first = pk[0].lower()
                # if node.pk_range[0] <= first <= node.pk_range[1]:
                #     node_request.work.append(tx)
                

            if len(node_request.work) > 0:
                to_send[node.url] = node_request

        # store contract
        contract = self.xnode.w3.eth.contract(address=address, abi=self.xnode.contract.abi)
        self.xnode.coordinating_contracts[address] = {
            "contract": contract,
            "work": work
        }   

        self.xnode.request(address, len(to_send))

        #TODO: sloppy as hell
        def send_ReceiveWork(url, request):
            with grpc.insecure_channel(url) as channel:
                stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
                stub.ReceiveWork(request)

        for url, request in to_send.items():
            thread = threading.Thread(None, send_ReceiveWork, None, [url, request])
            thread.start()

        response = _grpc.tpc_pb2.WorkResponse(address=address, timeout=self.xnode.timeout, threshold=len(to_send))
        return response

    def JoinSys(self, request, context):
        nodes = request.nodes
        

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
