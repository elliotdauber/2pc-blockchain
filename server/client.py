import grpc
import _grpc.helloworld_pb2_grpc
import _grpc.helloworld_pb2

class Client:
    def __init__(self):
        pass

    def makeRequest(self):
        with grpc.insecure_channel("localhost:8888") as channel:
            stub = _grpc.helloworld_pb2_grpc.CoordinatorStub(channel)
            request = _grpc.helloworld_pb2.WorkRequest(work="the message!", address="the addy!")
            retval = stub.SendWork(request)
            print(retval.success)

def client():
    c = Client()
    c.makeRequest()

if __name__ == "__main__":
    client()