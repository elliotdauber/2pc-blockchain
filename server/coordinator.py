from w3connection import W3HTTPConnection
from contract import Contract

class Coordinator:
    def __init__(self, contract_file, w3, num_nodes):
        self.contract = Contract(contract_file, w3)
        self.w3 = w3 #TODO: rethink this abstraction
        self.num_nodes = num_nodes

    def run(self):
        print("deploying contract index " + str(self.contract.num_deployments))
        self.contract.deploy()

    def request(self):
        timeout = 10
        self.contract.functions.request(self.num_nodes, timeout).transact()
        pass

    def print_num_deployments(self):
        print(self.contract.num_deployments())

def coordinator(numNodes):
    print("starting up the coordinator...")
    source = "contracts/TPC.sol"
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    C = Coordinator(source, w3.w3, numNodes)
    C.run()
    return C


coordinator(2)