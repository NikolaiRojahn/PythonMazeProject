import csv
import platform
from Maze import Maze


class csvFileWriter:

    def write(self, mazeArray, fileName):
        #print("fileInput called.", platform.os.getcwd())
        file_obj = open(fileName, "a+")
        output_writer = csv.writer(file_obj)
        for maze in list(mazeArray):
            output_writer.writerow(['#'])

            for row in maze.convertedMaze:
                output_writer.writerow(row)
