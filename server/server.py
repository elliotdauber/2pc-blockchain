from web3 import Web3, EthereumTesterProvider, eth
from serverconfig import *
from dynamo import table1, table2

# find better way to organize/import tables

def dynamotest():
    print("tables:")
    print(table1.creation_date_time)
    print(table2.creation_date_time)

def server():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    if not w3.isConnected():
        return
    eth.default_account = default_account

    contract_instance = w3.eth.contract(address=address, abi=abi)

    # read state:
    state = contract_instance.functions.getState().call()
    print(state)
    # 42

    contract_instance.functions.request([], 42).transact({'from': eth.default_account})
    state = contract_instance.functions.getState().call()
    print(state)

dynamotest()
server()
