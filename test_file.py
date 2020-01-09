import unittest, copy, functools
from Model import Model
from Maze import Maze
from Interfaces import ISolveAlgorithm
from DepthFirst import DepthFirst
from Counter import Counter
from Timer import Timer
from functools import reduce

class TestMaze(unittest.TestCase):
    # test data
    #Færdiggenereret maze til brug for test
    generatedMaze = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1],
        [1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,1],
        [1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1],
        [1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,1],
        [1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1],
        [1,0,1,0,0,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
        [1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,1],
        [1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1],
        [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1],
        [1,0,1,0,0,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,2,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

    #Metode som bruges til at teste maze uden slutpunkt - hvor den fjerner tallet "2" fra mazen og i stedet tilføjer tallet "1"
    def removeEndPoint(self, sublist: list) -> list:
        """Helper method to remove endpoint from list. """           
        sublist.remove(2)        
        sublist.append(1)        
        return sublist

    #Initialiserer __init__ fra "unittest.TestCase" - derudover opretter objekterne "Maze" og "DepthFirst" - for at bruge metoder i disse objekter til test
    def __init__(self, methodName):
        super().__init__(methodName)
        self.testMaze = Maze(5)
        self.df = DepthFirst()

    #Tester om en maze har slutpunkt - baseret på metoden "hasEndPoint" i "Maze"-objektet
    def test_MazeHasEndpoint(self):        
        expected = True
        actual = self.testMaze.hasEndPoint(self.generatedMaze)                           
        self.assertEqual(expected, actual)   

    #Tester om en maze kan løses baseret på metoden "search" i objektet "DepthFirst"
    def test_searchMaze(self):
        expected = True
        counterObject = Counter()
        actual = self.df.search(self.generatedMaze, 1, 1, counterObject, False)                       
        self.assertEqual(expected, actual)

    #Tester en maze uden slutpunkt baseret på metoden "hasEndPoint" i objektet "Maze"
    def test_MazeHasNoEndPoint(self):
        expected = False  
        #Nedenstående gør at man kopiere en liste som indeholder andre lister, således at alle lister kopieres med      
        mazeNoEnd = copy.deepcopy(self.generatedMaze)
        #Nedenstående tjekker ovenstående kopierede maze og hvis den finder et "2", så køre den metoden "self.removeEndPoint"
        mazeNoEnd = [sublist if 2 not in sublist else self.removeEndPoint(sublist) for sublist in mazeNoEnd]        
        actual = self.testMaze.hasEndPoint(mazeNoEnd)
        self.assertEqual(expected, actual)

    #Tester "solve"-metoden på "DepthFirst"-objektet
    def test_solveMaze(self):
        expected = True
        actual = self.df.solve(self.generatedMaze) is not None        
        self.assertEqual(expected, actual)
    
    #Tester hvorvidt en maze har væg helle vejen rundt
    def test_wallAllAround(self):
        expected = 1
        listWall = list()
        # top and bottom are all walls.
        listWall.extend(self.generatedMaze[0])
        listWall.extend(self.generatedMaze[-1])
        
        # for each sublist in maze, make a list of first and last int (lambda), 
        # add to a list (sublist) and add each value from it to listWall.
        listWall.extend([value for sublist in list(map(lambda z: [z[0], z[-1]],self.generatedMaze)) for value in sublist])        
        # use reduce to multiply all one's.
        actual = reduce((lambda x, y: x*y), listWall)
        self.assertEqual(expected, actual)