import grpc
import _grpc.tpc_pb2_grpc
import _grpc.tpc_pb2

class Client:
    def __init__(self):
        pass

    def makeRequest(self, transactions):
        with grpc.insecure_channel("localhost:8888") as channel:
            stub = _grpc.tpc_pb2_grpc.CoordinatorStub(channel)
            request = _grpc.tpc_pb2.WorkRequest()
            for t in transactions:
                transaction = _grpc.tpc_pb2.Transaction(
                    access=t["access"],
                    pk=t["pk"],
                    column=t["column"],
                    action=t["action"]
                )
                request.work.append(transaction)
            retval = stub.SendWork(request)
            print(retval)

    def DEPOSIT(self, account, amount):
        op1 = {
            "access": "write",
            "pk": account,
            "column": "balance",
            "action": "+" + str(amount)
        }
        self.makeRequest([op1])

    # for withdraw -- make a conditional to make sure user has necessary balance
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


def client():
    c = Client()
    # c.DEPOSIT("elliot", 10)
    c.TRANSFER("elliot", "zach", 10)

if __name__ == "__main__":
    client()