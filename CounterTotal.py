class CounterTotal:
    def __init__(self):
        self.MazeSolutionCounters = []

    def addCounterToMazeSolutionCountersList(self, counter):
        self.MazeSolutionCounters.append(counter)

    def getMinimumCounterForMazeSolutionCounters(self):
        return min(self.MazeSolutionCounters)

    def getMaximumCounterForMazeSolutionCounters(self):
        return max(self.MazeSolutionCounters)

    def getAverageCounterForMazeSolutionCounters(self):
        return sum(self.MazeSolutionCounters) / len(self.MazeSolutionCounters)