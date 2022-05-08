import grpc
import _grpc.tpc_pb2_grpc
import _grpc.tpc_pb2
import threading
from contract import Contract
from w3connection import W3HTTPConnection

class Client:
    def __init__(self, abi, w3):
        self.abi = abi
        self.w3 = w3

    def checkTxStatus(self, address):
        print("checking the status of the contract at: ", address)
        contract = self.w3.eth.contract(address=address, abi=self.abi)
        state = contract.functions.getState().call()
        print("state: ", state)


    def makeRequest(self, transactions):
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
            thread = threading.Timer(retval.timeout, self.checkTxStatus, [retval.address])
            thread.start()

class BankClient(Client):
    def DEPOSIT(self, account, amount):
        op1 = {
            "access": "write",
            "pk": account,
            "column": "balance",
            "action": "+" + str(amount)
        }
        self.makeRequest([op1])

    # for withdraw and transfer -- make a conditional to make sure user has necessary balance
    def WITHDRAW(self, account, amount):
        op1 = {
            "access": "write",
            "pk": account,
            "column": "balance",
            "action": "-" + str(amount)
        }
        self.makeRequest([op1])

    def TRANSFER(self, from_account, to_account, amount):
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
        self.makeRequest([op1, op2])

    def CHECK_BALANCE(self, account):
        op1 = {
            "access": "read",
            "pk": account,
            "column": "balance"
        }
        self.makeRequest([op1])

    def CREATE_ACCOUNT(self, account):
        op1 = {
            "access": "write",
            "pk": account,
            "action": "&"
        }
        self.makeRequest([op1])

    def DELETE_ACCOUNT(self, account):
        op1 = {
            "access": "write",
            "pk": account,
            "action": "~"
        }
        self.makeRequest([op1])

def simple_test(c):
    c.CREATE_ACCOUNT("elliot")
    c.CREATE_ACCOUNT("nick")
    c.CREATE_ACCOUNT("zach")
    c.DEPOSIT("elliot", 15)
    c.TRANSFER("elliot", "zach", 10)
    c.CHECK_BALANCE("elliot")
    c.CHECK_BALANCE("nick")
    c.CHECK_BALANCE("zach")
    c.DELETE_ACCOUNT("nick")

def client():
    w3 = W3HTTPConnection()
    contract = Contract("contracts/TPC.sol", w3.w3)
    w3 = W3HTTPConnection()
    c = BankClient(contract.abi, w3.w3)
    simple_test(c)

if __name__ == "__main__":
    client()