# 2pc-blockchain

Final Project for Stanford University CS244B (Distributed Systems)

2 phase commit protocol using a blockchain coordinator

Steps for running:
- Open 5 Terminals
- Terminal 1
    - cd server
    - ./setup
    - ./build
    - cd ..
    - Run ganache-cli
- Terminal 2 - 4:
    - cd server
    - source server_env/bin/activate
    - python3 xnode.py 0, 1, 2 (for terminals 2,3,4 respectively)
- Terminal 5;
    - cd server
    - source server_env/bin/activate
    - python3 client.py


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
    
TODO CLIENT:
- Add timestamps to requests!s

Notes:
- There is currently a bug where a request from a client causes a crash.
The crash goes away when I comment out the code that sends the ReceiveWork 
RPCs in the coordinator (could have to do with processing time?)


GRPC:
If you update tpc.proto:
- cd server
- run python -m grpc_tools.protoc -I./protos --python_out=./_grpc --grpc_python_out=./_grpc ./protos/tpc.proto
- change "import tpc_pb2 as tpc__pb2" to "import _grpc.tpc_pb2 as tpc__pb2" in _grpc/tpc_pb2_grpc.py

Resources:
Paper: https://dl.acm.org/doi/pdf/10.1145/3211933.3211940
Aleth: https://github.com/ethereum/aleth
web3.py: https://web3py.readthedocs.io/en/stable/quickstart.html