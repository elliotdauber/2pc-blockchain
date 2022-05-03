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
                print(t["access"])
                transaction = _grpc.tpc_pb2.Transaction(
                    access=t["access"],
                    pk=t["pk"],
                    column=t["column"],
                    action=t["action"]
                )
                request.work.append(transaction)
            retval = stub.SendWork(request)
            print(retval.success)

    def DEPOSIT(self, account, amount):
        op1 = {
            "access": "write",
            "pk": account,
            "column": "balance",
            "action": "+" + str(amount)
        }
        self.makeRequest([op1])

def client():
    c = Client()
    c.DEPOSIT("elliot", 10)

if __name__ == "__main__":
    client()