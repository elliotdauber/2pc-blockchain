from dbquery import query_pk
import sys

def dbfind_pk(table, pk, num_nodes):
    _pk = None
    for i in range(num_nodes):
        dbfile = "db" + str(i) + ".db"
        _pk = query_pk(dbfile, table, pk)
        if _pk is not None:
            return i
    return -1

if __name__ == "__main__":
    pk = sys.argv[1]
    node = dbfind_pk("customers", sys.argv[1], int(sys.argv[2]))
    print("pk " + pk + " found on node " + str(node))
