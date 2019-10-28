class TimerTotal:

    MazeSolutionTimes = []

    def addTimeToMazeSolutionTimesList(self, time):
        self.MazeSolutionTimes.append(time)

    def getMinimumTimeForMazeSolutionTimes(self):
        return self.MazeSolutionTimes.sort()[0]

    def getMaximumTimeForMazeSolutionTimes(self):
        return self.MazeSolutionTimes.sort()[len(self.MazeSolutionTimes - 1)]

    def getAverageTimeForMazeSolutionTimes(self):
        return self.calculateSumTimeForMazeSolutionTimes / len(self.MazeSolutionTimes)

    def calculateSumTimeForMazeSolutionTimes(self):
        for i in range(len(self.MazeSolutionTimes)):
            sum += i
        return i
        
#class TimerTotal:

#    timerTotal = 0.0
    
#    def setTotalTimer(self, timerRuntime):
#        self.timerTotal += timerRuntime      

#    def GetTimer(self):
#        return self.timerTotal