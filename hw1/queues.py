from abc import ABC, abstractmethod
from queue import PriorityQueue

class Queue(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def push(self, item):
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

    def push(self, item):
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

    def push(self, item):
        self.lifo.append(item)

    def pop(self):
        return self.lifo.pop()

    def __len__(self):
        return len(self.lifo)


# The queue for Djikstras is a simple priority queue
class Dijkstras(Queue):
    def __init__(self):
        self.queue = PriorityQueue()
        super().__init__()

    def push(self, item, cost=0):
        self.queue.put((cost, item))

    def pop(self):
        return self.queue.get()[1]

    def __len__(self):
        return len(self.queue.queue)