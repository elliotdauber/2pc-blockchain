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

    async def makeRequest(self, transactions, access="w", blk=True):
        url = random.choice(self.node_urls)
        with grpc.insecure_channel(url) as channel:
            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
            request = _grpc.tpc_pb2.WorkRequest(clienturl=self.url, access=access)
            for t in transactions:
                pk = t["pk"].encode()
                pk_hash = hashlib.sha256(pk).hexdigest()
                transaction = _grpc.tpc_pb2.SQLTransaction(
                    sql=t["sql"],
                    pk=pk_hash
                )
                request.work.append(transaction)
            retval = stub.SendWork(request)
            print("THRESHOLD IS " + str(retval.threshold) + " FOR " + retval.address)
            if blk:
                self.outstanding_txs.add_request(retval.address, retval.threshold)
                outcome = await self.waitForResponse(retval.address, retval.timeout)
                data = self.outstanding_txs.data(retval.address)
                if outcome is None: # timeout
                    result = self.checkTxStatus(retval.address) #TODO
                    print("RESULT: ", result)
                    outcome = result["state"]
                    data = result["data"]
                return self.transform_data(data) if outcome == "COMMIT" else outcome

class ClientGRPC(_grpc.tpc_pb2_grpc.ClientServicer):
    def __init__(self, client):
        super().__init__()
        self.client = client

    def ReceiveOutcome(self, request, context):
        self.client.outstanding_txs.add_response(request.address, request.outcome, request.data)
        return _grpc.tpc_pb2.Empty()


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
            "sql": "SELECT pk, balance FROM customers WHERE pk='" + account + "';"
        }
        return await self.makeRequest([op1], blk=blk, access="r")

    async def CHECK_BALANCES(self, accounts, blk=True):
        ops = []
        for account in accounts:
            op = {
                "pk": account,
                "sql": "SELECT pk, balance FROM customers WHERE pk='" + account + "';"
            }
            ops.append(op)
        return await self.makeRequest(ops, blk=blk, access="r")

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
    print(await c.CHECK_BALANCE("elliot"))
    print(await c.CHECK_BALANCE("nick"))
    print(await c.CHECK_BALANCE("zach"))
    print(await c.CHECK_BALANCES(["elliot", "nick", "zach"]))
    #await c.DELETE_ACCOUNT("nick")

async def init_tables(c):
    await c.CREATE_CUSTOMERS_TABLE()

async def small_test(c):
    await c.CREATE_ACCOUNT("isaac")
    await c.CREATE_ACCOUNT("sahit")
    await c.DEPOSIT("isaac", 15)
    await print(await c.CHECK_BALANCE("isaac"))
    await c.DEPOSIT("sahit", 5)
    print(await c.CHECK_BALANCE("sahit"))
    await c.TRANSFER("isaac", "sahit", 5)
    print(await c.CHECK_BALANCES(["isaac", "sahit"]))

async def balance(c):
    await c.CREATE_CUSTOMERS_TABLE()
    await c.CREATE_ACCOUNT("elliot")
    await c.DEPOSIT("elliot", 24)
    print(await c.CHECK_BALANCE("elliot"))

def client():
    w3 = W3HTTPConnection()
    contract = Contract("contracts/TPC.sol", w3.w3)
    url = "localhost:49155"
    c = BankClient(contract.abi, w3.w3, url)

    tests = {
        "simple": simple_test,
        "small": small_test,
        "balance": balance
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