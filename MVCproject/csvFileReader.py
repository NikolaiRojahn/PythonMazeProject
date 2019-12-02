import csv
from Maze import Maze


class csvFileReader:

    sizes: list = list()

    @staticmethod
    def getSizes():
        return csvFileReader.sizes

    def read(self, fileName):
        seperator = ['#']
        seperatorNewSize = ['EndOfMazeSize']
        mazesAllSizes = []
        mazesSingleSize = []
    
        with open(fileName) as f:
            a = 0
            reader = csv.reader(f, delimiter=',')
            maze = []
            for row in reader:
                if len(csvFileReader.sizes) != 0:
                    if row == seperator:
                        objMaze = Maze(csvFileReader.sizes[a], maze.copy())
                        mazesSingleSize.append(objMaze)
                        maze.clear()
                    elif row == seperatorNewSize:
                        mazesAllSizes.append(mazesSingleSize.copy())
                        mazesSingleSize.clear()
                        a += 1
                    else:
                        for i in range(0, len(row)):
                            row[i] = int(row[i])
                        maze.append(row)
                else:
                    for b in range(0, len(row)):
                        csvFileReader.sizes.append(int(row[b]))
        return mazesAllSizes
