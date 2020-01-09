class Counter:
    #Opsætter en tom liste uden indhold i konstruktøren
    def __init__(self):
        self.countVisited = []

    #Tilføjer et punkt (string) i listen - denne bruges til optælling af punkter besøgt ved løsningen af labyrinten
    def AddToCounterList(self, visited):
        self.countVisited.append(visited)

    #Returnere længden af listen - altså hvor mange steder som er besøgt ved løsningen af labyrinten
    def GetNumberOfPointsVisited(self):
        return len(self.countVisited)