from web3 import Web3, EthereumTesterProvider, eth
from serverconfig import *

def server():
    w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
    print('connected', w3.isConnected())
    eth.default_account = default_account

    contract_instance = w3.eth.contract(address=address, abi=abi)

    # read state:
    state = contract_instance.functions.getState().call()
    print(state)
    # 42

    contract_instance.functions.request([], 42).transact({'from': eth.default_account})
    state = contract_instance.functions.getState().call()
    print(state)

server()
