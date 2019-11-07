import csv
from Maze import Maze


class csvFileReader:

    sizes: list = None  

    @staticmethod
    def getSizes():
        return csvFileReader.sizes

    def read(self, fileName):
        seperator = ['#']
        seperatorNewSize = ['EndOfMazeSize']
        mazesAllSizes = []
        mazesSingleSize = []

        with open(fileName) as f:
            reader = csv.reader(f, delimiter=',')
            maze = []
            for row in reader:
                if(csvFileReader.sizes is not None):
                    if(row == seperator):
                        objMaze = Maze(None, maze.copy())
                        mazesSingleSize.append(objMaze)
                        maze.clear()
                    elif(row == seperatorNewSize):
                        mazesAllSizes.append(mazesSingleSize.copy())
                        mazesSingleSize.clear()
                    else:
                        for i in range(0, len(row)):
                            row[i] = int(row[i])
                        maze.append(row)
                else:
                    csvFileReader.sizes = row
            print("MAZE FROM READER!!!!!!!!!!!!!!!!!!")
            print(mazesAllSizes[0][0].convertedMaze)
        return mazesAllSizes