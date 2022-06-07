import _grpc.tpc_pb2
from ethquery import query

# test of making a "header" file in python -- declare fn prototypes upfront and then assign the functions later
# class Test:
#     def __init__(self):
#         pass
#
#     def m(self,msg):
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
def in_range(pk, pks):
    low = int(pks[0])
    high = int(pks[1])
    if pk == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": #The empty PK
        return True
    pk = int(pk, 16)
    if low > high:
        return pk >= low and pk < high # Normal Case
    return pk > low and pk <= high # If we have a wrap around

def recover(logfile, pk_range=None):
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
                    state = query(line)
                    if state == "COMMIT":
                        commit = True
                        #txs = []
                    else:
                        commit = False
                    continue
                elif not commit:
                    continue
                elif line[0] == "]":
                    # end of list
                    if pk_range:
                        if in_range(tx.pk, pk_range):
                            txs.append(tx)
                        #return(txs)
                    else:
                        txs.append(tx)
                        print(txs)
                        #return(txs)
                    #self.transact_multiple(txs)
                    continue
                elif line[0] == "[":
                    line = line[1:]
                    tx = _grpc.tpc_pb2.SQLTransaction()
                elif line[0] == ",":
                    line = line[2:]
                    if pk_range:
                        if in_range(tx.pk, pk_range):
                            txs.append(tx)
                    else:
                        txs.append(tx)
                    tx = _grpc.tpc_pb2.SQLTransaction()

                #TODO: handle multiple txs for one address (comma separator)
                halves = line.split(":")
                key = halves[0]
                val = halves[1].strip(" \"").replace("\\", "")
                if key == "sql":
                    tx.sql = val
                elif key == "pk":
                    tx.pk = val
            return txs
    except FileNotFoundError:
        print("NO LOG FILE FOUND")
        return []

if __name__ == "__main__":
    recover("log0.txt")



