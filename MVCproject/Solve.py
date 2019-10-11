class Solve:

    def __init__(self, Maze, Counter):
        self.maze = Maze
        self.counter = Counter

    def search(self, x, y):
        if self.maze.gridMaze[x][y] == 2:
            print("found at %d,%d" % (x, y))
            return True
        elif self.maze.gridMaze[x][y] == 1:
            print ('wall at %d,%d' % (x, y))
            return (False)
        elif self.maze.gridMaze[x][y] == 3:
            self.counter.AddToCounterList('visited at %d,%d')
            print ('visited at %d,%d' % (x, y))
            return (False)
        print ('visiting %d,%d' % (x, y))
        # mark as visited
        self.maze.gridMaze[x][y] = 3
        # explore neighbors clockwise starting by the one on the right
        if ((x < (len(self.maze.gridMaze)-1) and self.search(x+1, y))
            or (y > 0 and self.search(x, y-1))
            or (x > 0 and self.search(x-1, y))
            or (y < len(self.maze.gridMaze)-1 and self.search(x, y+1))):
            return True
        return False