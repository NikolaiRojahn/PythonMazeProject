class CounterTotal:

    def __init__(self):
        self.MazeSolutionCounters = []

    def addCounterToMazeSolutionCountersList(self, counter):
        self.MazeSolutionCounters.append(counter)

    def getMinimumCounterForMazeSolutionCounters(self):
        return self.MazeSolutionCounters.sort()[0]

    def getMaximumCounterForMazeSolutionCounters(self):
        return self.MazeSolutionCounters.sort()[len(self.MazeSolutionCounters - 1)]

    def getAverageCounterForMazeSolutionCounters(self):
        return self.calculateSumCounterForMazeSolutionCounters() / len(self.MazeSolutionCounters)

    def calculateSumCounterForMazeSolutionCounters(self):
        sum = 0
        for i in range(len(self.MazeSolutionCounters)):
            sum += self.MazeSolutionCounters[i]
        return sum