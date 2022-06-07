import grpc
import _grpc.tpc_pb2_grpc
import _grpc.tpc_pb2
import sys

def kill(url):
    with grpc.insecure_channel(url) as channel:
        stub = _grpc.tpc_pb2_grpc.XNodeStub(channel)
        request = _grpc.tpc_pb2.Empty()
        retval = stub.Kill(request)
        return retval


if __name__ == "__main__":
    url = sys.argv[1]
    kill(url)