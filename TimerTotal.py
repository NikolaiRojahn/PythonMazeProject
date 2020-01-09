class TimerTotal:
    #Initialisere en tom liste i konstruktøren
    def __init__(self):
        self.MazeSolutionTimes = []

    #Tilføjer en værdi (Double) i listen over tid beregnet ved løsningen tallet kommer som return fra "Timer"-objektet
    def addTimeToMazeSolutionTimesList(self, time):
        self.MazeSolutionTimes.append(time)

    #Returnere den mindste værdi i listen - altså den hurtigste tid ved løsningen af labyrinten - bruges til plotting for "Minimum Time"
    def getMinimumTimeForMazeSolutionTimes(self):
        return min(self.MazeSolutionTimes)

    #Returnere den højeste værdi i listen - altså den langsommeste tid ved løsningen af labyrinten - bruges til plotting for "Maximum Time"
    def getMaximumTimeForMazeSolutionTimes(self):
        return max(self.MazeSolutionTimes)

    #Returnerer den gennemsnitlige (sum/antal elementer i listen) værdi i listen - bruges til plotting for "Average Time"
    def getAverageTimeForMazeSolutionTimes(self):
        return sum(self.MazeSolutionTimes) / len(self.MazeSolutionTimes)