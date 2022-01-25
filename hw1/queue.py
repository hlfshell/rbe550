from abc import ABC, abstractmethod
from queue import PriorityQueue

class Queue(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def push(self, item, cost=None):
        pass

    @abstractmethod
    def pop(self, item):
        pass

    @abstractmethod
    def __len__(self):
        pass


# The queue for the BFS is FIFO
class BFSQueue(Queue):

    def __init__(self):
        self.fifo = []
        super().__init__()

    def push(self, item, cost=None):
        self.fifo.append(item)

    def pop(self):
        return self.fifo.pop(0)

    def __len__(self):
        return len(self.fifo)


# The queue for DFS is LIFO
class DFSQueue(Queue):
    def __init__(self):
        self.lifo = []
        super().__init__()

    def push(self, item, cost=None):
        self.lifo.append(item)

    def pop(self):
        return self.lifo.pop()

    def __len__(self):
        return len(self.lifo)


# The queue for Djikstras is a simple priority queue
class Dijkstras(Queue):
    def __init__(self):
        self.queue = []
        super().__init__()

    def push(self, item, cost=None):
        self.lifo.append(item)

    def pop(self):
        return self.lifo.pop()

    def __len__(self):
        return len(self.lifo)