class Counter:
    def __init__(self):
        self.countVisited = []

    def AddToCounterList(self, visited):
        self.countVisited.append(visited)

    def GetNumberOfPointsVisited(self):
        return len(self.countVisited)

    def GetNumberOfPointsVisitedWithText(self):
        return str(self.GetNumberOfPointsVisited()) + " " + "points has been visited"
