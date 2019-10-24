import csv

from Maze import Maze

filename = "test2.csv"
seperator = ['#']

mazes = []

with open(filename) as f:
    reader = csv.reader(f, delimiter=',')
    maze = []
    for row in reader:
        if(row == seperator):
            objMaze = Maze(None, maze.copy())
            mazes.append(objMaze)
            maze.clear()
        else:
            for i in range(0, len(row)):
                row[i] = int(row[i])
            maze.append(row)