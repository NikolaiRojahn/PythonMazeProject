import time

class Timer:
    timerStart = None
    timerEnd = None
    timerRuntime = None
    
    def StartTimer(self):
        self.timerStart = time.time()

    def EndTimer(self):
        self.timerEnd = time.time()
        self.timerRuntime = self.timerEnd - self.timerStart  

    def GetTimer(self):
        return self.timerRuntime 

    def GetTimerWithText(self):
        return "Running time:" + " " + str(self.timerRuntime) + " " + "seconds!"