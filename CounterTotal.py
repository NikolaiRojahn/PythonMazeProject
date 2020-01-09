class CounterTotal:
    #Initialisere en tom liste i konstruktøren
    def __init__(self):
        self.MazeSolutionCounters = []

    #Tilføjer en værdi (Int) i listen over steder besøgt ved løsningen tallet kommer som return fra "Counter"-objektet
    def addCounterToMazeSolutionCountersList(self, counter):
        self.MazeSolutionCounters.append(counter)

    #Returnerer den mindste værdi i listen - bruges til plotting for "Minimum Iterations"
    def getMinimumCounterForMazeSolutionCounters(self):
        return min(self.MazeSolutionCounters)

    #Returnerer den højeste værdi i listen - bruges til plotting for "Maximum Iterations"
    def getMaximumCounterForMazeSolutionCounters(self):
        return max(self.MazeSolutionCounters)

    #Returnerer den gennemsnitlige (sum/antal elementer i listen) værdi i listen - bruges til plotting for "Average Iterations"
    def getAverageCounterForMazeSolutionCounters(self):
        return sum(self.MazeSolutionCounters) / len(self.MazeSolutionCounters)