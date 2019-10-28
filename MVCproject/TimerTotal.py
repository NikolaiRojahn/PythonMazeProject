class TimerTotal:

    # MazeSolutionTimes = []
    MazeSolutionTimes = list()

    def addTimeToMazeSolutionTimesList(self, time):
        self.MazeSolutionTimes.append(time)

    def getMinimumTimeForMazeSolutionTimes(self):
        return self.MazeSolutionTimes.sort()[0]

    def getMaximumTimeForMazeSolutionTimes(self):
        return self.MazeSolutionTimes.sort()[len(self.MazeSolutionTimes - 1)]

    def getAverageTimeForMazeSolutionTimes(self):
        return self.calculateSumTimeForMazeSolutionTimes() / len(self.MazeSolutionTimes)

    def calculateSumTimeForMazeSolutionTimes(self):
        sum = 0
        for i in range(len(self.MazeSolutionTimes)):
            sum += self.MazeSolutionTimes[i]
        return sum

# class TimerTotal:

#    timerTotal = 0.0

#    def setTotalTimer(self, timerRuntime):
#        self.timerTotal += timerRuntime

#    def GetTimer(self):
#        return self.timerTotal
