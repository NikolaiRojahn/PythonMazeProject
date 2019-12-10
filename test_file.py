import unittest
from Model import Model
from Maze import Maze
from Interfaces import ISolveAlgorithm
from DepthFirst import DepthFirst


class TestMaze(unittest.TestCase):
    # test data

    def __init__(self, methodName):
        super().__init__(methodName)
        self.testMaze = Maze(10)

    def test_MazeHasEndpoint(self):
        print("test_MazeHasEndpoint running")
        # loop through Maze.convertedMaze, which is a list of (sub)lists,
        # for each sublist run a lambda that checks if 2 is in sublist.
        lwep = list(filter(lambda sublist: 2 in sublist,
                           self.testMaze.convertedMaze))
        self.assertTrue(len(lwep) > 0)
