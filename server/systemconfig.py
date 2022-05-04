from dynamo import tables


class CoordinatorConfig:
    def __init__(self, url):
        self.url = url


class NodeConfig:
    def __init__(self, id, url, table, pk_range):
        self.id = id
        self.url = url
        self.table = table
        self.pk_range = pk_range


class SystemConfig:
    def __init__(self, nodes, coord):
        self.nodes = nodes
        self.coord = coord


_NODES = [
    NodeConfig(id=0, url="localhost:8889", table=tables[0], pk_range=["a", "n"]),
    NodeConfig(id=1, url="localhost:8887", table=tables[1], pk_range=["o", "z"])
]

_COORD = CoordinatorConfig("localhost:8888")

SYSCONFIG = SystemConfig(_NODES, _COORD)




class SystemConfigX:
    def __init__(self, nodes):
        self.nodes = nodes


_NODESX = [
    NodeConfig(id=0, url="localhost:8887", table=tables[0], pk_range=["a", "h"]),
    NodeConfig(id=1, url="localhost:8888", table=tables[1], pk_range=["i", "o"]),
    NodeConfig(id=2, url="localhost:8889", table=tables[2], pk_range=["p", "z"])
]


SYSCONFIGX = SystemConfigX(_NODESX)
