from colorama import Fore
from string import ascii_letters
import random
import bisect

class CoordinatorConfig:
    def __init__(self, url):
        self.url = url


class NodeConfig:
    def __init__(self, id, url, color):
        self.id = id
        self.url = url
        self.color = color
        self.logfile = "log" + str(id) + ".txt"
        self.dbfile = "db" + str(id) + ".db"


class SystemConfig:
    def __init__(self, nodes, coord):
        self.nodes = nodes
        self.coord = coord


_NODES = [
    NodeConfig(id=0, url="localhost:8889", color=Fore.RED),
    NodeConfig(id=1, url="localhost:8887", color=Fore.GREEN)
]

_COORD = CoordinatorConfig("localhost:8888")

SYSCONFIG = SystemConfig(_NODES, _COORD)


class Directory:
    def __init__(self, nodes=[], pre_dir={}):
        self.dir = {}
        self.urls = set()
        if len(pre_dir.keys()) > 0:
            for key, value in pre_dir.items():
                self.dir[key] = value
                for val in value:
                    self.urls.add(val)
        for node in nodes:
            self.addNode(node, 3)
            

    def addNode(self, node, num_vnodes, new_keys=[]):
        if len(new_keys) == 0:
            new_keys, _ = self.findKeys(num_vnodes)
        self.updateDir(new_keys, node.url)
        return new_keys

    def findKeys(self, num_vnodes):
        new_keys = []
        old_nodes = []
        for _ in range(num_vnodes):
            curr_keys = list(self.dir.keys())
            available = [c for c in range(256) if c not in curr_keys and c not in new_keys]
            if not available:
                key = random.choice(range(256))
            else:
                key = random.choice(available)
            old_nodes.append(self.search(key))
            new_keys.append(key)
        return new_keys, old_nodes

    def updateDir(self, new_keys, url):
        for key in new_keys:
            if url in self.urls:
                continue
            elif key in list(self.dir.keys()):
                self.dir[key].append(url)
            else:
                self.dir[key] = [url]
        self.urls.add(url)
        return

    def search(self, key):
        keys = sorted(list(self.dir.keys()))
        if len(keys) == 0:
            return ""
        i = bisect.bisect_left(keys, key)
        if i >= len(keys) or i < 0:
            i = len(keys)-1
        return self.dir[keys[i]]



class SystemConfigX:
    def __init__(self, nodes, directory):
        self.nodes = nodes
        self.directory = directory

m = 2**256
_NODESX = [
    NodeConfig(id=0, url="localhost:8887", color=Fore.RED),
    NodeConfig(id=1, url="localhost:8888", color=Fore.GREEN),
    NodeConfig(id=2, url="localhost:8889", color=Fore.BLUE)
]

SYSCONFIGX = SystemConfigX(_NODESX, Directory(nodes=_NODESX))
