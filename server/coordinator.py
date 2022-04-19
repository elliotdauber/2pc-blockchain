from w3connection import W3HTTPConnection
from contract import Contract

class Coordinator:
    def __init__(self, contract_file, w3):
        self.contract = Contract(contract_file, w3)
        self.w3 = w3 #TODO: rethink this abstraction

    def run(self):
        print("deploying contract index " + str(self.contract.num_deployments))
        self.contract.deploy()

    def print_num_deployments(self):
        print(self.contract.num_deployments())

def coordinator():
    print("starting up the coordinator...")
    source = "../contracts/TPC.sol"
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    C = Coordinator(source, w3.w3)
    C.run()


coordinator()