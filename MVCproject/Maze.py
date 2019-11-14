from random import shuffle


import sys
# needed for DFS...
sys.setrecursionlimit(10000)


class Maze:
    maze = None
    convertedMaze = None
    gridMaze = None

    # Q&D pseudo overload of constructor.
    def __init__(self, size=None, convertedMaze=None):
        if size is not None:
            self.size = size
            self.create()
        elif convertedMaze is not None:
            self.convertedMaze = convertedMaze
        else:
            raise Exception()

    def create(self):
        self.maze = self.DFG(self.make_empty_maze())
        self.convertedMaze = self.convert(self.maze)
        #self.gridMaze = self.ConvertedStrMazeToGridOfInt(self.convertedMaze)

    def DFG(self, maze, coords=(0, 0)):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle(directions)
        for direction in directions:
            new_coords = (coords[0] + direction[0], coords[1] + direction[1])
            if (0 <= new_coords[0] < len(maze)) and \
                (0 <= new_coords[1] < len(maze[0])) and \
                    not maze[new_coords[0]][new_coords[1]]:
                maze[coords[0]][coords[1]].append(direction)
                maze[new_coords[0]][new_coords[1]].append(
                    (-direction[0], -direction[1]))
                self.DFG(maze, new_coords)
        return maze

    def make_empty_maze(self):
        maze = [[[] for b in range(self.size)] for a in range(self.size)]
        return maze

    def convert(self, maze, verbose=False):
        # pretty_maze = [["1"]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
        pretty_maze = [[1]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
        if verbose:
            print(str(pretty_maze))
        for y, row in enumerate(maze):
            for x, col in enumerate(row):
                # Check for endpoint position
                if y == len(maze)-1 and x == len(row)-1:
                    # pretty_maze[2*y+1][2*x+1] = "2"
                    pretty_maze[2*y+1][2*x+1] = 2
                else:
                    # pretty_maze[2*y+1][2*x+1] = "0"
                    pretty_maze[2*y+1][2*x+1] = 0
                    for direction in col:
                        # pretty_maze[2*y+1+direction[0]
                        #             ][2*x+1+direction[1]] = "0"
                        pretty_maze[2*y+1+direction[0]
                                    ][2*x+1+direction[1]] = 0
        if verbose:
            print(str(pretty_maze))
        return pretty_maze

    def ConvertedStrMazeToGridOfInt(self, cMaze):
        for a in cMaze:
            for i in range(0, len(a)):
                a[i] = int(a[i])
        return cMaze

    def pretty_print(self):
        string = ""
        for a in self.convertedMaze:
            for b in a:
                string += str(b)
            string += "\n"
        return string
