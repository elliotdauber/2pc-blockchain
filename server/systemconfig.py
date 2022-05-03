from dynamo import tables


class NodeConfig:
    def __init__(self, id, url, table, pk_range):
        self.id = id
        self.url = url
        self.table = table
        self.pk_range = pk_range


class SystemConfig:
    def __init__(self, nodes):
        self.nodes = nodes


_NODES = [
    NodeConfig(id=0, url="localhost:8889", table=tables[0], pk_range=["a", "n"]),
    NodeConfig(id=1, url="localhost:8887", table=tables[1], pk_range=["o", "z"])
]

SYSCONFIG = SystemConfig(_NODES)
