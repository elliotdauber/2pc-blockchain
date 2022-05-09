from dynamo import tables
from colorama import Fore


class CoordinatorConfig:
    def __init__(self, url):
        self.url = url


class NodeConfig:
    def __init__(self, id, url, table, pk_range, color, logfile):
        self.id = id
        self.url = url
        self.table = table
        self.pk_range = pk_range
        self.color = color
        self.logfile = logfile


class SystemConfig:
    def __init__(self, nodes, coord):
        self.nodes = nodes
        self.coord = coord


_NODES = [
    NodeConfig(id=0, url="localhost:8889", table=tables[0], pk_range=["a", "n"], color=Fore.RED, logfile="log0.txt"),
    NodeConfig(id=1, url="localhost:8887", table=tables[1], pk_range=["o", "z"], color=Fore.GREEN, logfile="log1.txt")
]

_COORD = CoordinatorConfig("localhost:8888")

SYSCONFIG = SystemConfig(_NODES, _COORD)




class SystemConfigX:
    def __init__(self, nodes):
        self.nodes = nodes


_NODESX = [
    NodeConfig(id=0, url="localhost:8887", table=tables[0], pk_range=["a", "h"], color=Fore.RED, logfile="log0.txt"),
    NodeConfig(id=1, url="localhost:8888", table=tables[1], pk_range=["i", "o"], color=Fore.GREEN, logfile="log1.txt"),
    NodeConfig(id=2, url="localhost:8889", table=tables[2], pk_range=["p", "z"], color=Fore.BLUE, logfile="log2.txt")
]


SYSCONFIGX = SystemConfigX(_NODESX)
