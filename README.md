# 2pc-blockchain

Final Project for Stanford University CS244B (Distributed Systems)

2 phase commit protocol using a blockchain coordinator

Steps for running the Solidity files:

1. Go to remix.ethereum.org (in FireFox)
2. Run remixd -s <folder_location> -u <remix_url> and set workspace to localhost
3. Run ganache-cli and set the environment to Web3 Provider
4. Compile .sol file, and copy the abi to serverconfig.py
5. Deploy the contract, and copy the address to serverconfig.py

Paper: https://dl.acm.org/doi/pdf/10.1145/3211933.3211940

Aleth: https://github.com/ethereum/aleth

web3.py: https://web3py.readthedocs.io/en/stable/quickstart.html