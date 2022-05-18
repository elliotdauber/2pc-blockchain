import sys
from w3connection import W3HTTPConnection
import grpc
import _grpc.tpc_pb2_grpc
from concurrent import futures
from systemconfig import SYSCONFIGX, NodeConfig, Directory
from contract import Contract
from colorama import Style, Fore
import threading
import sqlite3
import random
from recovery import recover
import time
import hashlib


color = ""

def cprint(msg):
    print(color + str(msg) + Style.RESET_ALL)


class XNode:
    def __init__(self, w3, config, directory, contract_file):
        self.contract = Contract(contract_file, w3)
        self.nodes = SYSCONFIGX.nodes
        self.directory = directory

        self.config = config
        self.w3 = w3
        self.working_contracts = {}
        self.coordinating_contracts = {}
        self.working_pk = set()
        self.timeout = 10
        cprint(self.config.url)

    # NODE FUNCTIONS

    def serve(self, url=None):
        # Initialize the server
        cprint("STARTING XNODE SERVER " + str(self.config.id) + " @ " + self.config.url)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.tpc_pb2_grpc.add_XNodeServicer_to_server(
            XNodeGRPC(self), server)
        server.add_insecure_port(self.config.url)
        server.start()
        if url is not None:
            self.join_system(url)
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
                        cprint("ACCESS: " + access)
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

    def valid_new_node(self, id, url):
        for n in self.nodes:
            if n.url == url:
                return False
            if n.id == id:
                return False
        return True

    def join_system(self, url):
        cprint("Requesting to join through node:" + str(url))
        id = self.config.id
        myurl = self.config.url
        with grpc.insecure_channel(url) as channel:
            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
            node_message = _grpc.tpc_pb2.Node(id=id, url=myurl)
            request = _grpc.tpc_pb2.JoinRequest(node=node_message, keys=[])
            retval = stub.AddNode(request)
            if retval.success:
                cprint("Added!")
                info = retval.config
                self.config = NodeConfig(info.id, info.url, info.color)
                new_dir = {int(key): value.url for key, value in retval.directory.items()}
                self.directory = Directory(pre_dir=new_dir)
                cprint(str(self.directory.dir))
                return True
            else:
                print("FAILED TO JOIN")
                return False

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
        # cprint("GOT WORK")
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
                # cprint("DIR LOOKUP: " + str(node.url) + " " + str(self.xnode.directory.search(pk)))
                if node.url in self.xnode.directory.search(pk):
                    node_request.work.append(tx)
                    # cprint("URL: " + str(node.url) + "\nWORK: " + str(tx))


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

    def AddNode(self, request, context): #TODO: Add Logging for recovery
        id = request.node.id
        new_url = request.node.url
        cprint("\nNew Node requesting to join system\nid: " + str(id) + "\nurl: " + str(new_url))
        failed_response = _grpc.tpc_pb2.JoinResponse(work=[], success=False)
        work = []
        start_node = len(request.keys) == 0
        if start_node:

            # select random color
            node_color = random.choice(['YELLOW', 'MAGENTA', 'CYAN'])

            # create/initalize log and db file names
            logfile = "log" + str(id) + ".txt"
            dbfile = "db" + str(id) + ".db"

            new_node = NodeConfig(id, new_url, node_color) # Need to remove the relevance of pk ranges
            node_message = _grpc.tpc_pb2.Node(id=id, url=new_url, color=node_color, log=logfile, db=dbfile)
            curr_key = 0

            if self.xnode.valid_new_node(id, new_url):
                # Update my local directory 
                new_node_keys, old_node_urls =  self.xnode.directory.findKeys(3)# MAKE THIS A SYSTEM CONFIG VALUE
                new_node_keys = [str(key) for key in new_node_keys]
                # Send to every other node 
                cprint("Sharing the request with other nodes")
                for node_url in self.xnode.directory.urls:
                    if node_url in old_node_urls:
                        i = old_node_urls.index(node_url)
                    else:
                        i = 0

                    if node_url == self.xnode.config.url:
                        curr_key = new_node_keys[i]
                        work = recover(self.xnode.config.logfile, curr_key)
                    else:
                        with grpc.insecure_channel(node_url) as channel:
                            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
                            request = _grpc.tpc_pb2.JoinRequest(node=node_message, keys=new_node_keys, idx=i) #Potentially use async grpc
                            retval = stub.AddNode(request)
                            if retval == failed_response:
                                return failed_response
                cprint("\nAll other nodes have confirmed admission")
            else:
                return failed_response

        else:
            # add work to populate any pks we share
            cprint("Collecting work for node")
            c = request.node.color
            new_node = NodeConfig(id, new_url, c) # Need to remove the relevance of pk ranges
            new_node_keys = request.keys
            pk_range = request.keys[request.idx]
            work = recover(self.xnode.config.logfile, pk_range)
        
        if len(work) > 0:
            cprint("Sending work to node")
            with grpc.insecure_channel(new_url) as channel:
                stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
                transactions = []
                for action in work: 
                    transactions.append(_grpc.tpc_pb2.SQLTransaction(pk=curr_key, sql=action))
                request = _grpc.tpc_pb2.MoveRequest(work=transactions)
                retval = stub.MoveData(request)
                if not retval.completed:
                    return failed_response

        # add node to self.xnode.nodes: 
        cprint("Adding Node to Directory")
        self.xnode.nodes.append(new_node)
        self.xnode.directory.updateDir(new_node_keys, new_url)    
        cprint(str(self.xnode.directory.dir))

        if not start_node:
            response = _grpc.tpc_pb2.JoinResponse(work=work, success=True) # We say success is true for original node
        else:
            grpc_dict = {}
            for key, value in self.xnode.directory.dir.items():
                grpc_dict[str(key)] = _grpc.tpc_pb2.url_list(url=value)
            response = _grpc.tpc_pb2.JoinResponse(config=node_message, directory=grpc_dict, work=work, success=True) # sucess when original node is complete
        # TODO: Delete data associated with new keys

        return response

    def MoveData(self, request, context):
        try:
            self.xnode.transact_multiple(self, request.work)
            response = _grpc.tpc_pb2.MoveResponse(complete=True)
        except:
            response = _grpc.tpc_pb2.MoveResponse(complete=False)
        return response



def run_xnode(config, directory, url):
    cprint("starting up a node...")
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    source = "contracts/TPC.sol"
    X = XNode(w3.w3, config, directory, source)
    if url is not None:
        X.serve(url)
    else:
        X.serve()
    return X


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    assert(index >= 0)
    global color
    if index >= len(SYSCONFIGX.nodes):
        color = Fore.CYAN
        print("Adding a New Node to the system")
        if sys.argv[2]:
            url = sys.argv[2]
        else:
            exit("Need system nodes url to add new node to system")
        node = NodeConfig(index, "localhost:888"+str(index), None)
        run_xnode(node, None, url)
    else:
        color = SYSCONFIGX.nodes[index].color
        run_xnode(SYSCONFIGX.nodes[index], SYSCONFIGX.directory, None)


if __name__ == "__main__":
    main()
