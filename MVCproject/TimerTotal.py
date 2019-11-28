class TimerTotal:
    def __init__(self):
        self.MazeSolutionTimes = []

    def addTimeToMazeSolutionTimesList(self, time):
        self.MazeSolutionTimes.append(time)

    def getMinimumTimeForMazeSolutionTimes(self):
        return min(self.MazeSolutionTimes)

    def getMaximumTimeForMazeSolutionTimes(self):
        return max(self.MazeSolutionTimes)

    def getAverageTimeForMazeSolutionTimes(self):
        return sum(self.MazeSolutionTimes) / len(self.MazeSolutionTimes)