import re
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
import os

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
        self.server = None
        cprint(self.config.url)

    # NODE FUNCTIONS

    def serve(self, url=None, txs=[]):
        # Initialize the server
        cprint("STARTING XNODE SERVER " + str(self.config.id) + " @ " + self.config.url)
        if len(txs) > 0:
            self.transact_multiple(txs, "w")
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.tpc_pb2_grpc.add_XNodeServicer_to_server(
            XNodeGRPC(self), self.server)
        self.server.add_insecure_port(self.config.url)
        self.server.start()
        if url is not None:
            self.join_system(url)
        
        self.server.wait_for_termination()

    def log(self, text):
        with open(self.config.logfile, 'a+') as f:
            f.write(text + "\n")

    def can_transact(self, work):
        db = sqlite3.connect(self.config.dbfile)
        cursor = db.cursor()
        if all([tx.pk not in self.working_pk for tx in work]): # Check that no pks are already being manipulated
            for tx in work:

                command = tx.sql.split(" ")

                if command[0] == "CREATE": # Check for duplicate creates
                    check = ("SELECT * FROM sqlite_master WHERE type = 'table' AND name = '" + command[2] + "';")
                    if len([x for x in cursor.execute(check)]) > 0: # Cant Create a table that already exists without deleting it
                        return False

                if command[0] == "INSERT": # Check for Creating an account that already exists
                    check = ("SELECT * FROM sqlite_master WHERE type = 'table' AND name = '" + command[2] + "';") # Check table exists
                    if len([x for x in cursor.execute(check)]) < 0:
                        return False
                    check = "SELECT * FROM customers WHERE pk=" + command[6][1:-1] + ";"
                    if len([x for x in cursor.execute(check)]) > 0:
                        return False

            for tx in work: self.working_pk.add(tx.pk)
            return True
        return False

    def voter(self, address, vote):
        contract = self.working_contracts.get(address)["contract"]
        if contract is None:
            return
        cprint("VOTING " + str(vote) + " on contract " + address[-4:])
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

    def valid_new_node(self, _id, url):
        i = 0
        for n in self.nodes:
            if n.url == url:
                i += 1
            if n.id == _id:
                i += 1
            if i > 0:
                return i
        return 0

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
                return True
            else:
                print("FAILED TO JOIN")
                return False

class XNodeGRPC(_grpc.tpc_pb2_grpc.XNodeServicer):
    def __init__(self, xnode):
        super().__init__()
        self.xnode = xnode

    def Kill(self, request, context):
        cprint("\n\nNODE " + str(self.xnode.config.id) + " KILLED\n\n\n")
        os.remove("db" + str(self.xnode.config.id) + ".db")
        self.xnode.server.stop(0)
        exit()
        return _grpc.tpc_pb2.Empty()

    def ReceiveWork(self, request, context):
        work = request.work
        address = request.address
        timeout = request.timeout
        self.xnode.log(address)
        self.xnode.log(str(work))
        cprint("Node " + str(self.xnode.config.id) + " is in the cohort for tx at ..." + address[-4:])
        for tx in request.work:
            cprint("pk: " + tx.pk[:4] + "...")
            cprint("sql: " + tx.sql)
            cprint("")

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
        address = request.address
        if len(work) == 0:
            return _grpc.tpc_pb2.WorkResponse(error="no work given, operation aborted")

        cprint("Node " + str(self.xnode.config.id) + " acting as the coordinator for tx at ..."+ address[-4:] + "\n")

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
                if node.url in self.xnode.directory.search(pk)[1]:
                    node_request.work.append(tx)


            if len(node_request.work) > 0:
                to_send[node.url] = node_request
                
        # store contract
        contract = self.xnode.w3.eth.contract(address=address, abi=self.xnode.contract.abi)
        self.xnode.coordinating_contracts[address] = {
            "contract": contract,
            "work": work
        }   

        self.xnode.request(address, len(to_send))

        def send_ReceiveWork(url, request):
            try:
                with grpc.insecure_channel(url) as channel:
                    stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
                    stub.ReceiveWork(request)
            except:
                pass

        for url, request in to_send.items():
            thread = threading.Thread(None, send_ReceiveWork, None, [url, request])
            thread.start()

        response = _grpc.tpc_pb2.WorkResponse(timeout=self.xnode.timeout, threshold=len(to_send))
        return response

    def AddNode(self, request, context): #TODO: Add Logging for recovery
        _id = request.node.id
        new_url = request.node.url
        cprint("\nNew Node requesting to join system\nid: " + str(_id) + "\nurl: " + str(new_url))
        failed_response = _grpc.tpc_pb2.JoinResponse(work=[], success=False)
        work = []
        start_node = len(request.keys) == 0
        if start_node == True:
            # select random color
            node_color = random.choice(['YELLOW', 'MAGENTA', 'CYAN'])

            # create/initalize log and db file names
            logfile = "log" + str(_id) + ".txt"
            dbfile = "db" + str(_id) + ".db"

            new_node = NodeConfig(_id, new_url, node_color) # Need to remove the relevance of pk ranges
            node_message = _grpc.tpc_pb2.Node(id=_id, url=new_url, color=node_color, log=logfile, db=dbfile)
            curr_key = 0
            new_node_type = self.xnode.valid_new_node(_id, new_url) # New and valid = 0, Old and failed = 2, Bad = 1
            if  new_node_type == 0:
                # Update my local directory 
                new_node_keys,  old_node_keys, old_node_urls =  self.xnode.directory.findKeys(_id, 3)# MAKE THIS A SYSTEM CONFIG VALUE
                new_node_keys = [str(key) for key in new_node_keys]
                old_node_keys = [str(key) for key in old_node_keys]

                #TODO for old node URLS we need to make sure that if new keys overlap thaat the largest one is used

                # Send to every other node 
                cprint("Sharing the request with other nodes")
                key_replaced = False
                for node_url in self.xnode.directory.urls:
                    i = -1
                    if node_url in old_node_urls:
                        i = old_node_urls.index(node_url)
                    if i != -1:
                        key_replaced = True
                    if node_url == self.xnode.config.url:
                        if i != -1:
                            curr_key = new_node_keys[i]
                            work = recover(self.xnode.config.logfile, (old_node_keys[i], curr_key))
                    else:
                        with grpc.insecure_channel(node_url) as channel:
                            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
                            request = _grpc.tpc_pb2.JoinRequest(node=node_message, keys=new_node_keys, idx=i, old_keys=old_node_keys) #Potentially use async grpc
                            retval = stub.AddNode(request)
                            if retval == failed_response:
                                return failed_response
                if not key_replaced:
                    work = recover(self.xnode.config.logfile, ("0", "0"))
                cprint("\nAll other nodes have confirmed admission")
            elif new_node_type == 2:
                grpc_dict = {}
                for key, value in self.xnode.directory.dir.items():
                    grpc_dict[str(key)] = _grpc.tpc_pb2.url_list(url=value)
                response = _grpc.tpc_pb2.JoinResponse(config=node_message, directory=grpc_dict, work=work, success=True) # sucess when original node is complete
                return response
            else: 
                return failed_response

        else:
            # add work to populate any pks we share
            cprint("Collecting work for node")
            c = request.node.color
            new_node = NodeConfig(id, new_url, c) # Need to remove the relevance of pk ranges
            new_node_keys = request.keys
            if request.idx != -1:
                pk_range = (request.keys[request.idx], request.old_keys[request.idx])
                work = recover(self.xnode.config.logfile, pk_range)
        if work == None:
            work = []
        if len(work) > 0:
            cprint("Sending work to node")
            #for demo purposes
            moved_accounts = set()
            cleaned_work = []
            for tx in work:
                tx_sql = tx.sql.split(' ')
                if tx_sql[0] == "INSERT":
                    moved_accounts.add("Add Account: " + tx_sql[6])
                if tx_sql[0] == "CREATE":
                    moved_accounts.add("Create Table: " + tx_sql[2])
                if tx_sql[0] != 'SELECT':
                    cleaned_work.append(tx)
            cprint("Updating new node with: " + str(moved_accounts))
            work = cleaned_work
            with grpc.insecure_channel(new_url) as channel:
                stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
                request = _grpc.tpc_pb2.MoveRequest(work=work)
                retval = stub.MoveData(request)
                if not retval.complete:
                    return failed_response

        # add node to self.xnode.nodes: 
        cprint("Adding Node to Directory")
        self.xnode.nodes.append(new_node)
        self.xnode.directory.updateDir(new_node_keys, new_url)    

        if not start_node:
            response = _grpc.tpc_pb2.JoinResponse(work=work, success=True)
        else:
            grpc_dict = {}
            for key, value in self.xnode.directory.dir.items():
                grpc_dict[str(key)] = _grpc.tpc_pb2.url_list(url=value)
            response = _grpc.tpc_pb2.JoinResponse(config=node_message, directory=grpc_dict, work=work, success=True) # sucess when original node is complete

        #Delete data associated with new keys
            keys_to_delete = set()
            to_delete = []
            for tx in work:
                _sql = tx.sql
                name_start = _sql.find("(\'")
                name_end = _sql.find("\',")
                if name_start != -1 :
                    name = _sql[name_start + 2: name_end]
                    cprint("GOING TO DELETE:" + str(name))
                    if name not in keys_to_delete:
                        op1 = _grpc.tpc_pb2.SQLTransaction(
                            pk=tx.pk,
                            sql="DELETE FROM customers WHERE pk='" + name + "';"
                        )
                        to_delete.append(op1)
                        keys_to_delete.add(name)
            self.xnode.transact_multiple(to_delete, "w")
            cprint("Old PKs Removed")

        return response

    def MoveData(self, request, context):
        try:
            work = request.work
            transactions = []
            for i in range(len(work)):
                transactions.append(work[i])
            self.xnode.transact_multiple(transactions, "X")
            print("Updates Completed")
            response = _grpc.tpc_pb2.MoveResponse(complete=True)
        except:
            response = _grpc.tpc_pb2.MoveResponse(complete=False)
        return response



def run_xnode(config, directory, url, txs):
    cprint("starting up a node...")
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    source = "contracts/TPC.sol"
    X = XNode(w3.w3, config, directory, source)
    X.serve(url, txs)
    return X


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    assert(index >= 0)
    logfile = "log" + str(index) + ".txt"
    txs = []
    if os.path.exists(logfile):
        txs = recover(logfile)
    global color
    if index >= len(SYSCONFIGX.nodes):
        color = random.choice([Fore.MAGENTA, Fore.CYAN, Fore.YELLOW])
        print("Adding a New Node to the system")
        if sys.argv[2]:
            url = sys.argv[2]
        else:
            exit("Need system nodes url to add new node to system")
        node = NodeConfig(index, "localhost:888"+str(index), None)
        run_xnode(node, None, url, txs)
    else:
        color = SYSCONFIGX.nodes[index].color
        run_xnode(SYSCONFIGX.nodes[index], SYSCONFIGX.directory, None, txs)


if __name__ == "__main__":
    main()
