import time

class Timer:
    def __init__(self):
        self.timerStart = None
        self.timerEnd = None
        self.timerRuntime = None

    def StartTimer(self):
        self.timerStart = time.clock()

    def EndTimer(self):
        self.timerEnd = time.clock()
        self.timerRuntime = self.timerEnd - self.timerStart

    def GetTimer(self):
        return self.timerRuntime * 1000