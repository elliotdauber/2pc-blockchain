import _grpc.tpc_pb2

# test of making a "header" file in python -- declare fn prototypes upfront and then assign the functions later
# class Test:
#     def __init__(self):
#         pass
#
#     def m(self, msg):
#         pass
#
# def fn(self, msg):
#     print(msg)
#
#
# Test.m = fn
#
# t = Test()
# t.m("yo!")

#abi = ""

def recover(logfile, pk = None):
    tx = None
    txs = []
    commit = False
    try:
        with open(logfile, "r") as f:
            while True:
                line = f.readline().strip("\n")
                if not line:
                    break

                if line[:2] == "0x":
                    contract = None #TODO: set contract using line
                    state = "COMMIT" #contract.functions.getState().call()
                    if state == "COMMIT":
                        commit = True
                        txs = []
                    continue
                elif not commit:
                    continue
                elif line[0] == "]":
                    # end of list
                    if pk:
                        if tx.pk == pk:
                            txs.append(tx)
                        return(txs)
                    else:
                        txs.append(tx)
                        print(txs)
                        return(txs)
                    #self.transact_multiple(txs)
                    continue
                elif line[0] == "[":
                    line = line[1:]
                    tx = _grpc.tpc_pb2.SQLTransaction()
                elif line[0] == ",":
                    line = line[2:]
                    if pk:
                        if tx.pk == pk:
                            txs.append(tx)
                        return(txs)
                    else:
                        txs.append(tx)
                    tx = _grpc.tpc_pb2.SQLTransaction()

                #TODO: handle multiple txs for one address (comma separator)
                halves = line.split(":")
                key = halves[0]
                val = halves[1].strip(" \"")
                if key == "sql":
                    tx.sql = val
                elif key == "pk":
                    tx.pk = val
    except:
        print("NO LOG TO RECOVER FROM")
        return []

if __name__ == "__main__":
    recover("log0.txt")



