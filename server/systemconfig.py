from colorama import Fore


class CoordinatorConfig:
    def __init__(self, url):
        self.url = url


class NodeConfig:
    def __init__(self, id, url, pk_range, color):
        self.id = id
        self.url = url
        self.pk_range = pk_range
        self.color = color
        self.logfile = "log" + str(id) + ".txt"
        self.dbfile = "db" + str(id) + ".db"


class SystemConfig:
    def __init__(self, nodes, coord):
        self.nodes = nodes
        self.coord = coord


_NODES = [
    NodeConfig(id=0, url="localhost:8889", pk_range=["a", "n"], color=Fore.RED),
    NodeConfig(id=1, url="localhost:8887", pk_range=["o", "z"], color=Fore.GREEN)
]

_COORD = CoordinatorConfig("localhost:8888")

SYSCONFIG = SystemConfig(_NODES, _COORD)




class SystemConfigX:
    def __init__(self, nodes):
        self.nodes = nodes

m = 2**256
_NODESX = [
    NodeConfig(id=0, url="localhost:8887", pk_range=[0, m/3], color=Fore.RED),
    NodeConfig(id=1, url="localhost:8888", pk_range=[m/3 + 1, 2*m/3], color=Fore.GREEN),
    NodeConfig(id=2, url="localhost:8889", pk_range=[2*m/3 + 1, m], color=Fore.BLUE)
]


SYSCONFIGX = SystemConfigX(_NODESX)
