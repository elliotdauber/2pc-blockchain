from dynamo import tables

class SystemConfig:
    def __init__(self, nodes):
        self.nodes = nodes

_NODES = [
    {
        "url": "localhost:8889",
        "pk_range": ["a", "n"],
        "table": tables[0]
    },
    {
        "url": "localhost:8887",
        "pk_range": ["o", "z"],
        "table": tables[1]
    }
]

SYSCONFIG = SystemConfig(_NODES)
