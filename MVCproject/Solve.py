class Solve:

    def __init__(self, Maze, Counter):
        self.maze = Maze
        self.counter = Counter

    def search(self, x, y, verbose=False):
        if self.maze.gridMaze[x][y] == 2:
            print("found at %d,%d" % (x, y))
            return True
        elif self.maze.gridMaze[x][y] == 1:
            if verbose:
                print('wall at %d,%d' % (x, y))
            return (False)
        elif self.maze.gridMaze[x][y] == 3:
            self.counter.AddToCounterList('visited at %d,%d')
            if verbose:
                print('visited at %d,%d' % (x, y))
            return (False)
        if verbose:
            print('visiting %d,%d' % (x, y))
        # mark as visited
        self.maze.gridMaze[x][y] = 3
        # explore neighbors clockwise starting by the one on the right
        if ((x < (len(self.maze.gridMaze)-1) and self.search(x+1, y, verbose))
            or (y > 0 and self.search(x, y-1, verbose))
            or (x > 0 and self.search(x-1, y, verbose))
                or (y < len(self.maze.gridMaze)-1 and self.search(x, y+1, verbose))):
            return True
        return False
