import threading
from Maze import Maze

class ThreadPool(object):
    def __init__(self):
        super(ThreadPool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
    def makeActive(self, Maze):
        with self.lock:
            self.active.append(Maze)
    def makeInactive(self, Maze):
        with self.lock:
            self.active.remove(Maze)