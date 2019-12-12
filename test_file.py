import unittest
from model import Model
from Maze import Maze
from Interfaces import ISolveAlgorithm
from DepthFirst import DepthFirst
from Counter import Counter
from Timer import Timer

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

    def test_MazeHasNoEndPoint(self):
        expected = False        
        mazeNoEnd = [sublist if 2 not in sublist else self.removeEndPoint(sublist) for sublist in self.generatedMaze]        
        actual = self.testMaze.hasEndPoint(mazeNoEnd)
        self.assertEqual(expected, actual)
<<<<<<< HEAD

    def test_searchMaze(self):
        expected = True
        counterObject = Counter()
        actual = self.df.search(self.generatedMaze, 1, 1, counterObject, False)                       
        self.assertEqual(expected, actual)

    def test_solveMaze(self):
        expected = True
        actual = self.df.solve(self.generatedMaze) is not None
        # print(actual)
        # if(actual is not None):
        #     expected == True
        self.assertEqual(expected, actual)

    if __name__ == '__main__':
        unittest.main()
=======
    
    def test_wallAllAround(self):
        expected = 1
        listWall = list()
        listWall.extend(self.generatedMaze[0])
        listWall.extend(self.generatedMaze[len(self.generatedMaze) - 1])
        listWall.extend([item for elem in list(map(lambda z: [z[0], z[-1]],self.generatedMaze)) for item in elem])
        actual = sum(listWall)/len(listWall)
        self.assertEqual(expected, actual)

    def test_make_empty_maze5(self):
        testBool = True
        empty_maze = self.testMaze.make_empty_maze()
        if len(empty_maze) is not self.testMaze.size:
            testBool = False
        for a in empty_maze:
            if len(a) is not self.testMaze.size:
                testBool = False
        self.assertTrue(testBool)

#if __name__ == '__main__':
#    unittest.main()
>>>>>>> cf575cef453ef4bc37ffad02e6059f3ffa316aa0
