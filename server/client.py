import grpc
import _grpc.tpc_pb2_grpc
import _grpc.tpc_pb2
import asyncio
from contract import Contract
from w3connection import W3HTTPConnection


def cback_default(state, args):
    print("state: ", state)

class Client:
    def __init__(self, abi, w3):
        self.abi = abi
        self.w3 = w3

    async def checkTxStatus(self, address, callback, timeout, args):
        print("checking the status of the contract at: ", address)
        contract = self.w3.eth.contract(address=address, abi=self.abi)
        tx_hash = contract.functions.verdict().transact()
        await self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout)
        state = contract.functions.getState().call()
        callback(state, args)


    async def makeRequest(self, transactions, callback=cback_default, args=None):
        if args is None:
            args = []
        with grpc.insecure_channel("localhost:8888") as channel:
            stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
            request = _grpc.tpc_pb2.WorkRequest()
            for t in transactions:
                transaction = _grpc.tpc_pb2.Transaction(
                    access=t["access"],
                    pk=t["pk"],
                    column=t["column"] if "column" in t else None,
                    action=t["action"] if "action" in t else None
                )
                request.work.append(transaction)
            retval = stub.SendWork(request)
            await self.checkTxStatus(retval.address, callback, retval.timeout, args)

#TODO: Maybe we should discuss how this opperates 
# if we want these to run in parallel I think we
# have to increase the number of async functions

class BankClient(Client):
    async def DEPOSIT(self, account, amount):
        op1 = {
            "access": "write",
            "pk": account,
            "column": "balance",
            "action": "+" + str(amount)
        }
        await self.makeRequest([op1])

    # for withdraw and transfer -- make a conditional to make sure user has necessary balance
    async def WITHDRAW(self, account, amount):
        op1 = {
            "access": "write",
            "pk": account,
            "column": "balance",
            "action": "-" + str(amount)
        }
        await self.makeRequest([op1])

    async def TRANSFER(self, from_account, to_account, amount):
        op1 = {
            "access": "write",
            "pk": from_account,
            "column": "balance",
            "action": "-" + str(amount)
        }
        op2 = {
            "access": "write",
            "pk": to_account,
            "column": "balance",
            "action": "+" + str(amount)
        }
        await self.makeRequest([op1, op2])

    async def CHECK_BALANCE(self, account):
        op1 = {
            "access": "read",
            "pk": account,
            "column": "balance"
        }
        await self.makeRequest([op1])

    async def CREATE_ACCOUNT(self, account):
        op1 = {
            "access": "write",
            "pk": account,
            "action": "&"
        }
        await self.makeRequest([op1])

    async def DELETE_ACCOUNT(self, account):
        op1 = {
            "access": "write",
            "pk": account,
            "action": "~"
        }
        await self.makeRequest([op1])

def simple_test(c):
    asyncio.run(asyncio.wait(
        [c.CREATE_ACCOUNT("elliot"),
        c.CREATE_ACCOUNT("nick"),
        c.CREATE_ACCOUNT("zach"),
        c.DEPOSIT("elliot", 15),
        c.TRANSFER("elliot", "zach", 10),
        c.CHECK_BALANCE("elliot"),
        c.CHECK_BALANCE("nick"),
        c.CHECK_BALANCE("zach"),
        c.DELETE_ACCOUNT("nick")]
    ))

def client():
    w3 = W3HTTPConnection()
    contract = Contract("contracts/TPC.sol", w3.w3)
    w3 = W3HTTPConnection()
    c = BankClient(contract.abi, w3.w3)
    simple_test(c)

if __name__ == "__main__":
    client()