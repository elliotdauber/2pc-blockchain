from coordinator import coordinator
from node import node
import sys

class System:
    def __init__(self, num_nodes):
        self.startCoordinator()
        for i in range(num_nodes):
            self.startNode(i)

    def startCoordinator(self):
        coordinator()

    def startNode(self, index):
        node(index)


def system(num_nodes):
    S = System(num_nodes)

def main():
    num_nodes = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    system(num_nodes)


if __name__ == "__main__":
    main()