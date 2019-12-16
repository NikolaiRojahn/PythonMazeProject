from abc import ABCMeta, abstractmethod
from Maze import Maze
from Counter import Counter
from Timer import Timer

# ICreateAlgorithm interface (abstract class)
# class ICreateAlgorithm(object):
#     __metaclass__ = ABCMeta

#     @abstractmethod
#     def Create(self, width, height): raise NotImplementedError


# ISolveAlgorithm interface (abstract class)
class ISolveAlgorithm(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def solve(self, maze: Maze) -> (Timer, Counter): raise NotImplementedError
    # def solve(self, maze: Maze,
    #   counter: Counter) -> Timer: raise NotImplementedError

#


class IView(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def start(self): raise NotImplementedError  # starts the view.
    @abstractmethod
    # attaches an observer to the view
    def attach(self, observer): raise NotImplementedError
    @abstractmethod
    def getState(self) -> str: raise NotImplementedError  # returns the state.
    @abstractmethod
    # returns data from view to observer(controller)
    def getData(self): raise NotImplementedError

    # @abstractmethod
    # def getAlgorithm(self) -> str: raise NotImplementedError
    # @abstractmethod
    # def getFilename(self) -> str: raise NotImplementedError
    # @abstractmethod
    # def getSizes(self): raise NotImplementedError

    # String "constants" for view's state, can be reassigned, just don't do it!
    SELECT_ALGORITHM = "selectAlgorithm"
    READ_FROM_FILE = "readFromFile"
    WRITE_TO_FILE = "writeToFile"
    ADD_MAZE_SIZE = "addMazeSize"
    SHOW_MAZE_SIZES = "showMazeSizes"
    CLEAR_MAZE_SIZES = "clearMazeSizes"
    GENERATE_MAZES = "generateMazes"
    SOLVE_MAZES = "solveMazes"
    SHOW_GRAPHS = "showGraphs"
