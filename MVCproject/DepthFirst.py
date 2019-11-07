from Interfaces import ISolveAlgorithm
from Counter import Counter


class DepthFirst(ISolveAlgorithm):

    def __init__(self):
        pass
    # def __init__(self, Maze, Counter):
    #     self.maze = Maze
    #     self.counter = Counter

    # implement ISolveAlgorithm.
    def solve(self, maze, counter) -> Counter:
        self.maze = maze
        self.counter = counter
        self.__search(1, 1)
        return self.counter

    # private method that implements depth first solving algorithm.
    def __search(self, x, y, verbose=False):
        if self.maze.convertedMaze[x][y] == 2:
            print("found at %d,%d" % (x, y))
            return True
        elif self.maze.convertedMaze[x][y] == 1:
            if verbose:
                print('wall at %d,%d' % (x, y))
            return (False)
        elif self.maze.convertedMaze[x][y] == 3:
            self.counter.AddToCounterList('visited at %d,%d')
            if verbose:
                print('visited at %d,%d' % (x, y))
            return (False)
        if verbose:
            print('visiting %d,%d' % (x, y))
        # mark as visited
        self.maze.convertedMaze[x][y] = 3
        # explore neighbors clockwise starting by the one on the right
        if ((x < (len(self.maze.convertedMaze)-1) and self.__search(x+1, y, verbose))
            or (y > 0 and self.__search(x, y-1, verbose))
            or (x > 0 and self.__search(x-1, y, verbose))
                or (y < len(self.maze.convertedMaze)-1 and self.__search(x, y+1, verbose))):
            return True
        return False
