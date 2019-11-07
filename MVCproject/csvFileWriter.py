import csv
import platform
from Maze import Maze


class csvFileWriter:

    def write(self, mazeArray, fileName):
        #print("fileInput called.", platform.os.getcwd())
        file_obj = open(fileName, "w", newline='')
        output_writer = csv.writer(file_obj)
        for sizeOfMaze in list(mazeArray):
            for maze in list(sizeOfMaze):
                for row in maze.convertedMaze:
                    output_writer.writerow(row)
                output_writer.writerow(['#'])
            output_writer.writerow(['EndOfMazeSize'])
