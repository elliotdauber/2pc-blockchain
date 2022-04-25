# 2pc-blockchain

Final Project for Stanford University CS244B (Distributed Systems)

2 phase commit protocol using a blockchain coordinator

Steps for running:
Run ganache-cli
In another terminal:
cd server
bin source/activate
python3 system.py
deactivate

TODO:
Coordinator:
- Deploy contract
- Send work and contract address to nodes
- Wait for more requests

Nodes:
- Wait for work and contract address from coordinator
- When work is received:
    - Determine if we can do the work
    - If we can, vote yes
    - If not, TODO

Nodes:


Resources:
Paper: https://dl.acm.org/doi/pdf/10.1145/3211933.3211940
Aleth: https://github.com/ethereum/aleth
web3.py: https://web3py.readthedocs.io/en/stable/quickstart.html