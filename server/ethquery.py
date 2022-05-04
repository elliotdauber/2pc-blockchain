from contract import Contract
from w3connection import W3HTTPConnection
import sys


def query(address):
    source = "contracts/TPC.sol"
    w3 = W3HTTPConnection().w3
    assert(w3.isConnected())
    c = Contract(source, w3)
    abi = c.abi
    contract = w3.eth.contract(address=address, abi=abi)
    state = contract.functions.getState().call()
    print("state", state)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("must have address")
    else:
        address = sys.argv[1]
        query(address)
