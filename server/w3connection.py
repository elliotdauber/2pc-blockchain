from web3 import Web3

class W3HTTPConnection:
    def __init__(self, address='http://127.0.0.1:8545'):
        self.w3 = Web3(Web3.HTTPProvider(address))
        self.w3.eth.default_account = self.w3.eth.accounts[0]

    def isConnected(self):
        return self.w3.isConnected()