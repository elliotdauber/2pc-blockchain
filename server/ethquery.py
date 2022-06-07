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
    tx_hash = contract.functions.verdict().transact()
    w3.eth.wait_for_transaction_receipt(tx_hash)
    state = contract.functions.getState().call()
    #print("state", state)
    return state

def query_data(address):
    source = "contracts/TPC.sol"
    w3 = W3HTTPConnection().w3
    assert(w3.isConnected())
    c = Contract(source, w3)
    abi = c.abi
    contract = w3.eth.contract(address=address, abi=abi)
    data = contract.functions.getData().call()
    print("data", data)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("must have address and op")
    address = sys.argv[1]
    op = sys.argv[2]
    if op == "state":
        address = sys.argv[1]
        query(address)
    elif op == "data":
        address = sys.argv[1]
        query_data(address)
