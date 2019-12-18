from Interfaces import ISolveAlgorithm
from Counter import Counter
from Timer import Timer
from Maze import Maze


class DepthFirst(ISolveAlgorithm):

    def __init__(self):
        pass

    # implement ISolveAlgorithm.
    def solve(self, convertedMaze) -> (Timer, Counter):
        """Solves a maze and counts iterations and time consumption."""
        counter = Counter()
        timer = Timer()

        timer.StartTimer()
        self.search(convertedMaze, 1, 1, counter)
        timer.EndTimer()
        return (timer, counter)

    #  method that implements depth first solving algorithm.
    def search(self, convertedMaze: list, x, y, counter: Counter, verbose=False) -> bool:
        if convertedMaze[x][y] == 2:
            if verbose:
                print("found at %d,%d" % (x, y))
            return True
        elif convertedMaze[x][y] == 1:
            if verbose:
                print('wall at %d,%d' % (x, y))
            return False
        elif convertedMaze[x][y] == 3:
            counter.AddToCounterList('visited at %d,%d' % (x, y))
            if verbose:
                print('visited at %d,%d' % (x, y))
            return False
        if verbose:
            print('visiting %d,%d' % (x, y))
        # mark as visited
        convertedMaze[x][y] = 3

        if ((x < (len(convertedMaze)-1) and self.search(convertedMaze, x+1, y, counter, verbose))
            or (y > 0 and self.search(convertedMaze, x, y-1, counter, verbose))
            or (x > 0 and self.search(convertedMaze, x-1, y, counter, verbose))
                or (y < len(convertedMaze)-1 and self.search(convertedMaze, x, y+1, counter, verbose))):
            return True
        return False
