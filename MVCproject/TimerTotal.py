class TimerTotal:

    timerTotal = 0.0
    
    def setTotalTimer(self, timerRuntime):
        self.timerTotal += timerRuntime      

    def GetTimer(self):
        return self.timerTotal