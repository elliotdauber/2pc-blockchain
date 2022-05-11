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

from concurrent import futures

def cback_default(state, args):
    print("state: ", state)

class Client:
    def __init__(self, abi, w3, url):
        self.abi = abi
        self.w3 = w3
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
   
    def checkTxStatus(self, address, callback, args):
        print("checking the status of the contract at: ", address)
        contract = self.w3.eth.contract(address=address, abi=self.abi)
        tx_hash = contract.functions.verdict().transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        state = contract.functions.getState().call()
        callback(state, args)
        return state

    def waitForResponse(self, address, timeout):
        total_time = 0
        while not self.outstanding_txs.responded(address):
            time.sleep(1) 
            total_time += 1
            if total_time >= timeout:
                return None
        return self.outstanding_txs.outcome(address)

    async def makeRequest(self, transactions, callback=cback_default, args=None, blk=True):
        if args is None:
            args = []
        url = random.choice(self.node_urls)
        with grpc.insecure_channel(url) as channel:
            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
            request = _grpc.tpc_pb2.WorkRequest(clienturl=self.url)
            for t in transactions:
                transaction = _grpc.tpc_pb2.SQLTransaction(
                    sql=t["sql"],
                    pk=t["pk"]
                )
                request.work.append(transaction)
            retval = stub.SendWork(request)
            if blk:
                self.outstanding_txs.add_request(retval.address, retval.threshold)
                outcome = self.waitForResponse(retval.address, retval.timeout)
                if outcome is None: # timeout
                    self.checkTxStatus(retval.address, callback, args)
                else:
                    callback(outcome, args)

class ClientGRPC(_grpc.tpc_pb2_grpc.ClientServicer):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def ReceiveOutcome(self, request, context):
        self.client.outstanding_txs.add_response(request.address, request.outcome)
        #TODO: data? what to do for writes?
        return _grpc.tpc_pb2.Empty() #TODO: data? only for reads


class BankClient(Client):
    async def CREATE_CUSTOMERS_TABLE(self, blk=True):
        op1 = {
            "pk": "",
            "sql": "CREATE TABLE customers (pk text, balance real);"
        }
        await self.makeRequest([op1], blk=blk)

    async def DEPOSIT(self, account, amount, blk=True):
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1], blk=blk)

    # for withdraw and transfer -- make a conditional to make sure user has necessary balance
    async def WITHDRAW(self, account, amount, blk=True):
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1], blk=blk)

    async def TRANSFER(self, from_account, to_account, amount, blk=True):
        op1 = {
            "pk": from_account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + from_account + "';"
        }
        op2 = {
            "pk": to_account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + to_account + "';"
        }
        await self.makeRequest([op1, op2], blk=blk)

    async def CHECK_BALANCE(self, account, blk=True):
        op1 = {
            "pk": account,
            "sql": "SELECT balance FROM customers WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1], blk=blk)

    async def CREATE_ACCOUNT(self, account, blk=True):
        op1 = {
            "pk": account,
            "sql": "INSERT INTO customers (pk, balance) VALUES ('" + account + "', 0);"
        }
        await self.makeRequest([op1], blk=blk)

    async def DELETE_ACCOUNT(self, account, blk=True):
        op1 = {
            "pk": account,
            "sql": "DELETE FROM customers WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1], blk=blk)

async def simple_test(c):
    await c.CREATE_CUSTOMERS_TABLE()
    await c.CREATE_ACCOUNT("elliot")
    await c.CREATE_ACCOUNT("nick")
    await c.CREATE_ACCOUNT("zach")
    await c.DEPOSIT("elliot", 15)
    await c.TRANSFER("elliot", "zach", 10)
    await c.CHECK_BALANCE("elliot", False)
    await c.CHECK_BALANCE("nick", False)
    await c.CHECK_BALANCE("zach", False)
    #await c.DELETE_ACCOUNT("nick")

def client():
    w3 = W3HTTPConnection()
    contract = Contract("contracts/TPC.sol", w3.w3)
    url = "localhost:49155"
    c = BankClient(contract.abi, w3.w3, url)

    tests = {
        "simple": simple_test
    }   

    while True:
        test = input("Enter a test name for the client at url " + url + ": ")
        if test == "quit":
            break
        if test in tests:
            asyncio.run(tests[test](c))

    # asyncio.run(simple_test(c))
    c.stop_grpc()

if __name__ == "__main__":
    client()


    #function(address): run loop that queries the outstanding_txs object and sees if the address has a response
    #checks the whole map first, then runs the loop