from dynamo import table1, table2, tables
import sys
from w3connection import W3HTTPConnection

def dynamotest():
    print("tables:")
    print(table1.creation_date_time)
    print(table2.creation_date_time)

class Node:
    def __init__(self, w3, table):
        self.table = table
        self.w3 = w3
        print(self.table.creation_date_time)

    def run(self):
        # TODO: all of the actual server stuff
        print("node running!")


def node(index):
    print("starting up a node...")
    w3 = W3HTTPConnection()
    assert(w3.isConnected())
    N = Node(w3.w3, tables[index])
    N.run()


def main():
    print(sys.argv)
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
