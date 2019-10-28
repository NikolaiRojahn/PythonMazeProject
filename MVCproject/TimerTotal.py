class TimerTotal:
    # ARGH the following line makes MazeSolutionTimes static,
    # since a value is assigned in class declaration.
    # MazeSolutionTimes = []

    def __init__(self):
        self.MazeSolutionTimes = []

    def addTimeToMazeSolutionTimesList(self, time):
        self.MazeSolutionTimes.append(time)

    def getMinimumTimeForMazeSolutionTimes(self):
        self.MazeSolutionTimes.sort()
        return self.MazeSolutionTimes[0]

    def getMaximumTimeForMazeSolutionTimes(self):
        self.MazeSolutionTimes.sort()
        return self.MazeSolutionTimes[len(self.MazeSolutionTimes) - 1]

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
