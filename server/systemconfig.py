from colorama import Fore
import random
import bisect
import hashlib

class NodeConfig:
    def __init__(self, id, url, color):
        self.id = id
        self.url = url
        self.color = color
        self.logfile = "log" + str(id) + ".txt"
        self.dbfile = "db" + str(id) + ".db"


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
            new_keys, _ = self.findKeys(node.id, num_vnodes)
        self.updateDir(new_keys, node.url)
        return new_keys

    def findKeys(self, node_id, num_vnodes):
        new_keys = []
        old_nodes = []
        for i in range(num_vnodes):
            # key = random.randint(0, 2**256)
            pre_hash = str(node_id) + "_" + str(i)
            key = int(hashlib.sha256(bytes(pre_hash, "utf-8")).hexdigest(), 16)
            old_nodes.append(self.search(key))
            new_keys.append(key)
        return new_keys, old_nodes

    def updateDir(self, new_keys, url):
        for key in new_keys:
            key = int(key)
            if url in self.urls:
                continue
            elif key in list(self.dir.keys()):
                self.dir[key].append(url)
            else:
                self.dir[key] = [url]
        self.urls.add(url)
        return

    def search(self, key):
        key = int(key)
        # print("KEY: ", key)
        keys = sorted(list(self.dir.keys()))
        if len(keys) == 0:
            return "" #todo: return empty list for type safety?
        i = bisect.bisect_left(keys, key)
        if i >= len(keys) or i < 0:
            i = len(keys)-1
        return self.dir[keys[i]]

    def key_range(self, key):
        key = int(key)
        keys = sorted(list(self.dir.keys()))
        i = keys.index(key) - 1
        if key < i:
            return (key , i)
        return (i, key)
        



class SystemConfigX:
    def __init__(self, nodes):
        self.nodes = nodes
        self.directory = Directory(nodes)

m = 2**256
_NODESX = [
    NodeConfig(id=0, url="localhost:8887", color=Fore.RED),
    NodeConfig(id=1, url="localhost:8888", color=Fore.GREEN),
    NodeConfig(id=2, url="localhost:8889", color=Fore.BLUE)
]

SYSCONFIGX = SystemConfigX(_NODESX)
