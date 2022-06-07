import grpc
import _grpc.tpc_pb2_grpc
import _grpc.tpc_pb2
import asyncio
from contract import Contract
from w3connection import W3HTTPConnection
from systemconfig import SYSCONFIGX
from txstatusmap import TransactionStatusMap
import time
import random
import hashlib

from concurrent import futures

def cback_default(state, args):
    print("state: ", state)

class Client:
    def __init__(self, url):
        self.w3 = W3HTTPConnection().w3
        self.contract = Contract("contracts/TPC.sol", self.w3)
        self.abi = self.contract.abi
        self.url = url
        self.outstanding_txs = TransactionStatusMap()
        self.node_urls = [node.url for node in SYSCONFIGX.nodes] #TODO: if we have time, make this info come from the nodes
        self.grpc_server = self.run_grpc()

    def run_grpc(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        _grpc.tpc_pb2_grpc.add_ClientServicer_to_server(
            ClientGRPC(self), server)
        server.add_insecure_port(self.url)
        server.start()
        # server.wait_for_termination()
        return server

    def stop_grpc(self):
        self.grpc_server.stop(0)

    def transform_data(self, data):
        item_strs = data.split(';;')
        items = []
        for item in item_strs:
            columns = item.strip("()").split(",")
            if len(columns) == 1:
                continue
            result = columns[:-1] if columns[-1] == "" else columns
            items.append(result)
        return items
   
    def checkTxStatus(self, address):
        print("checking the status of the contract at: ", address)
        contract = self.w3.eth.contract(address=address, abi=self.abi)
        tx_hash = contract.functions.verdict().transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        state = contract.functions.getState().call()
        data = contract.functions.getData().call()
        return {
            "state": state,
            "data": data
        }

    async def waitForResponse(self, address, timeout):
        total_time = 0
        while not self.outstanding_txs.responded(address):
            await asyncio.sleep(1) 
            total_time += 1
            if total_time >= timeout:
                return None
        return self.outstanding_txs.outcome(address)

    async def getResult(self, timeout, address, threshold):
        self.outstanding_txs.add_request(address, threshold)
        outcome = await self.waitForResponse(address, timeout)
        data = self.outstanding_txs.data(address)
        if outcome is None:  # timeout
            result = self.checkTxStatus(address)
            print("RESULT: ", result)
            outcome = result["state"]
            data = result["data"]
        return self.transform_data(data) if outcome == "COMMIT" else outcome

    async def makeRequest(self, transactions, access="w", blk=True):
        print("Client at " + self.url + " called makeRequest API with: ")
        print(transactions)
        url = random.choice(self.node_urls)
        with grpc.insecure_channel(url) as channel:
            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
            address = self.contract.deploy()
            request = _grpc.tpc_pb2.WorkRequest(clienturl=self.url, access=access, address=address)
            for t in transactions:
                pk = t["pk"].encode()
                pk_hash = hashlib.sha256(pk).hexdigest()
                transaction = _grpc.tpc_pb2.SQLTransaction(
                    sql=t["sql"],
                    pk=pk_hash
                )
                request.work.append(transaction)
            try:
                retval = stub.SendWork(request, timeout=5)
            except grpc.RpcError as e:
                print("SendWork RPC timed out")
                if blk:
                    result = self.checkTxStatus(address)
                    if result["state"] == "VOTING":
                        contract = self.w3.eth.contract(address=address, abi=self.abi)
                        timeout = contract.functions.getTimeout().call()
                        ret = await self.getResult(timeout, address, retval.threshold)
                        return ret

            if blk:
                ret = await self.getResult(retval.timeout, address, retval.threshold)
                return ret


class ClientGRPC(_grpc.tpc_pb2_grpc.ClientServicer):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def ReceiveOutcome(self, request, context):
        self.client.outstanding_txs.add_response(request.address, request.outcome, request.data)
        return _grpc.tpc_pb2.Empty()