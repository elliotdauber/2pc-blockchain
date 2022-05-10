import grpc
import _grpc.tpc_pb2_grpc
import _grpc.tpc_pb2
import asyncio
from contract import Contract
from w3connection import W3HTTPConnection
from systemconfig import SYSCONFIGX
import time
import random

def cback_default(state, args):
    print("state: ", state)

class Client:
    def __init__(self, abi, w3):
        self.abi = abi
        self.w3 = w3
        self.timeout = 100
        self.node_urls = [node.url for node in SYSCONFIGX.nodes] #TODO: if we have time, make this info come from the nodes

    def checkTxStatus(self, address, callback, args):
        print("checking the status of the contract at: ", address)
        contract = self.w3.eth.contract(address=address, abi=self.abi)
        tx_hash = contract.functions.verdict().transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        state = contract.functions.getState().call()
        callback(state, args)
        return state


    async def makeRequest(self, transactions, callback=cback_default, args=None):
        if args is None:
            args = []
        url = random.choice(self.node_urls)
        with grpc.insecure_channel(url) as channel:
            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
            request = _grpc.tpc_pb2.WorkRequest()
            for t in transactions:
                transaction = _grpc.tpc_pb2.SQLTransaction(
                    sql=t["sql"],
                    pk=t["pk"]
                )
                request.work.append(transaction)
            retval = stub.SendWork(request)
            await asyncio.sleep(retval.timeout)
            self.checkTxStatus(retval.address, callback, args)


class BankClient(Client):
    async def CREATE_CUSTOMERS_TABLE(self):
        op1 = {
            "pk": "",
            "sql": "CREATE TABLE customers (pk text, balance real);"
        }
        await self.makeRequest([op1])

    async def DEPOSIT(self, account, amount):
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1])

    # for withdraw and transfer -- make a conditional to make sure user has necessary balance
    async def WITHDRAW(self, account, amount):
        op1 = {
            "pk": account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1])

    async def TRANSFER(self, from_account, to_account, amount):
        op1 = {
            "pk": from_account,
            "sql": "UPDATE customers SET balance = balance - " + str(amount) + " WHERE pk='" + from_account + "';"
        }
        op2 = {
            "pk": to_account,
            "sql": "UPDATE customers SET balance = balance + " + str(amount) + " WHERE pk='" + to_account + "';"
        }
        await self.makeRequest([op1, op2])

    async def CHECK_BALANCE(self, account):
        op1 = {
            "pk": account,
            "sql": "SELECT balance FROM customers WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1])

    async def CREATE_ACCOUNT(self, account):
        op1 = {
            "pk": account,
            "sql": "INSERT INTO customers (pk, balance) VALUES ('" + account + "', 0);"
        }
        await self.makeRequest([op1])

    async def DELETE_ACCOUNT(self, account):
        op1 = {
            "pk": account,
            "sql": "DELETE FROM customers WHERE pk='" + account + "';"
        }
        await self.makeRequest([op1])

def simple_test(c):
    asyncio.run(
        asyncio.wait(
            [c.CREATE_CUSTOMERS_TABLE(),
            time.sleep(5),
            c.CREATE_ACCOUNT("elliot"),
            c.CREATE_ACCOUNT("nick"),
            c.CREATE_ACCOUNT("zach"),
            c.DEPOSIT("elliot", 15),
            c.TRANSFER("elliot", "zach", 10),
            c.CHECK_BALANCE("elliot"),
            c.CHECK_BALANCE("nick"),
            c.CHECK_BALANCE("zach"),
            c.DELETE_ACCOUNT("nick")]
        )
    )

def client():
    w3 = W3HTTPConnection()
    contract = Contract("contracts/TPC.sol", w3.w3)
    w3 = W3HTTPConnection()
    c = BankClient(contract.abi, w3.w3)
    simple_test(c)

if __name__ == "__main__":
    client()