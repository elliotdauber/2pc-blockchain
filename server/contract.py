import solcx

class Contract:
    def __init__(self, source, w3):
        spec = {
            "language": "Solidity",
            "sources": {
                'TPC.sol': {
                    "urls": [
                        source
                    ]
                }
            },
            "settings": {
                "optimizer": {
                    "enabled": True
                },
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode", "abi"
                        ]
                    }
                }
            }
        }
        out = solcx.compile_standard(spec, allow_paths=".")
        bytecode = out['contracts']['TPC.sol']['TPC']['evm']['bytecode']['object']
        self.abi = out['contracts']['TPC.sol']['TPC']['abi']
        print(w3)
        self.contract_bin = w3.eth.contract(abi=self.abi, bytecode=bytecode)
        self.contract = None
        self.w3 = w3
        self.deployments = 0

    def num_deployments(self):
        return self.deployments

    def deploy(self):
        tx_hash = self.contract_bin.constructor().transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        self.deployments += 1
        #self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.abi)
        return tx_receipt.contractAddress
