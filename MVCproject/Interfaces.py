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
