from dynamo import table1, table2, tables
import sys
from w3connection import W3HTTPConnection
from multiprocessing.connection import Listener

def dynamotest():
    print("tables:")
    print(table1.creation_date_time)
    print(table2.creation_date_time)

class Node:
    def __init__(self, w3, table, nodeid):
        self.table = table
        self.w3 = w3
        self.contract = None #TOOD: get contract from coordinator? how does this work?
        self.id = nodeid

    def run(self):
        # TODO: all of the actual server stuff
        print("node running!")
        print(self.table.creation_date_time)
        self.accept_msgs()
        if self.can_transact():
            self.voter(True)
        else:
            self.voter(False)
        # Upon recieving work, determine if it is doable and
        # pass the nodes vote on to the contract (node.voter(vote))
        # await a verdict

    def can_transact(self):
        # TODO: determine whether or not this work can be done locally
        return True

    # not currently used
    # https://stackoverflow.com/questions/6920858/interprocess-communication-in-python
    def accept_msgs(self):
        address = ('localhost', 6000)  # family is deduced to be 'AF_INET'
        listener = Listener(address, authkey=b'secret password')
        conn = listener.accept()
        print('connection accepted from', listener.last_accepted)
        while True:
            msg = conn.recv()
            # do something with msg
            if msg == 'close':
                conn.close()
                break
        listener.close()

    def voter(self, vote):
        state = self.contract.functions.voter(1).transact()
        if state == "COMMIT":
            pass
            #TODO
        elif state == "VOTING":
            pass
            #TODO

    def verdict(self):
        state = self.contract.functions.verdict.transact()
        if state == "ABORT":
            pass
            #TODO


def node(index):
    print("starting up a node...")
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    N = Node(w3.w3, tables[index], index)
    N.run()
    return N


def main():
    index = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    assert(0 <= index < len(tables))
    node(index)


if __name__ == "__main__":
    main()

# example contract calls:
# # read state:
#     # state = contract_instance.functions.getState().call()
#     # print(state)
#     # # 42
#     #
#     # contract_instance.functions.request([], 42).transact({'from': eth.default_account})
#     # state = contract_instance.functions.getState().call()
#     # print(state)
