from Interfaces import ISolveAlgorithm
from Counter import Counter
from Timer import Timer
from Maze import Maze


class DepthFirst(ISolveAlgorithm):

    def __init__(self):
        pass
    # def __init__(self, Maze, Counter):
    #     self.maze = Maze
    #     self.counter = Counter

    # implement ISolveAlgorithm.
    # def solve(self, maze, counter) -> Timer:
    def solve(self, maze: Maze) -> (Timer, Counter):
        """Solves a maze and counts iterations and time consumption."""
        counter = Counter()
        print("PRE counter: " + str(counter) +
              str(counter.GetNumberOfPointsVisited()))

        timer = Timer()

        self.maze = maze
        # print("PRETTY maze: " + maze.pretty_print())
        timer.StartTimer()
        self.__search(1, 1, counter)
        timer.EndTimer()
        print("POST counter: " + str(counter) +
              str(counter.GetNumberOfPointsVisited()))
        return (timer, counter)

    # private method that implements depth first solving algorithm.
    def __search(self, x, y, counter: Counter, verbose=False):
        if self.maze.convertedMaze[x][y] == 2:
            if verbose:
                print("found at %d,%d" % (x, y))
            return True
        elif self.maze.convertedMaze[x][y] == 1:
            if verbose:
                print('wall at %d,%d' % (x, y))
            return (False)
        elif self.maze.convertedMaze[x][y] == 3:
            counter.AddToCounterList('visited at %d,%d')
            if verbose:
                print('visited at %d,%d' % (x, y))
            return (False)
        if verbose:
            print('visiting %d,%d' % (x, y))
        # mark as visited
        self.maze.convertedMaze[x][y] = 3
        # explore neighbors clockwise starting by the one on the right
        if ((x < (len(self.maze.convertedMaze)-1) and self.__search(x+1, y, counter, verbose))
            or (y > 0 and self.__search(x, y-1, counter, verbose))
            or (x > 0 and self.__search(x-1, y, counter, verbose))
                or (y < len(self.maze.convertedMaze)-1 and self.__search(x, y+1, counter, verbose))):
            return True
        return False
