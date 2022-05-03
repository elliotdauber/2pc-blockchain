class SystemConfig:
    def __init__(self, nodes):
        self.nodes = nodes

_NODES = [
    {
        "url": "localhost:8889",
        "pk_range": ["a", "n"]
    },
    {
        "url": "localhost:8887",
        "pk_range": ["o", "z"]
    }
]

SYSCONFIG = SystemConfig(_NODES)
