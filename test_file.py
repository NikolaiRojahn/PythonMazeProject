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

    def removeEndPoint(self, sublist: list) -> list:
        """Helper method to remove endpoint from list. """           
        sublist.remove(2)        
        sublist.append(1)        
        return sublist

    def __init__(self, methodName):
        super().__init__(methodName)
        self.testMaze = Maze(5)
        self.df = DepthFirst()

    def test_MazeHasEndpoint(self):        
        expected = True
        actual = self.testMaze.hasEndPoint(self.generatedMaze)                           
        self.assertEqual(expected, actual)   

    def test_searchMaze(self):
        expected = True
        counterObject = Counter()
        actual = self.df.search(self.generatedMaze, 1, 1, counterObject, False)                       
        self.assertEqual(expected, actual)

    def test_MazeHasNoEndPoint(self):
        expected = False        
        mazeNoEnd = copy.deepcopy(self.generatedMaze)
        mazeNoEnd = [sublist if 2 not in sublist else self.removeEndPoint(sublist) for sublist in mazeNoEnd]        
        actual = self.testMaze.hasEndPoint(mazeNoEnd)
        self.assertEqual(expected, actual)

    def test_solveMaze(self):
        expected = True
        actual = self.df.solve(self.generatedMaze) is not None        
        self.assertEqual(expected, actual)
    
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


# def test_wallAllAround(self):
#         expected = 1
#         listWall = list()
#         # top and bottom are all walls.
#         multiplyer = lambda x,y: x*y
#         listWall.append(reduce(multiplyer, self.generatedMaze[0]))
#         listWall.append(reduce(multiplyer, self.generatedMaze[-1]))
        
#         # for each sublist in maze (map), make a list of first and last int (lambda), 
#         # add the resulting lists to a list (sublist) and add each value from this sublist to listWall.
#         # listWall.extend([value for sublist in list(map(lambda z: [z[0], z[-1]],self.generatedMaze)) for value in sublist])

#         # for each sublist in maze, multiply first and last item (lambda), 
#         # put result in a list (map) and reduce this list with multiplyer(), 
#         # append this result to listWall.
#         listWall.append(reduce(multiplyer, map(lambda z: z[0]* z[-1],self.generatedMaze)))
#         # use reduce to multiply all one's.
#         actual = reduce((lambda x, y: x*y), listWall)
#         self.assertEqual(expected, actual)