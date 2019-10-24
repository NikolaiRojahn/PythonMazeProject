import csv
import platform
from Maze import Maze


class FileHandler:
    fileNumber = 0

    def testMe(self, maze):
        self.fileNumber += 1
        file_obj = open("mazeFile{}.csv".format(self.fileNumber), "a+")
        output_writer = csv.writer(file_obj)
        for row in maze:
            output_writer.writerow([row])

    def fileInput(self, mazeArray):
        #print("fileInput called.", platform.os.getcwd())

        self.fileNumber += 1
        file_obj = open("mazeFile{}.csv".format(self.fileNumber), "a+")
        output_writer = csv.writer(file_obj)
        for maze in list(mazeArray):
            output_writer.writerow(['#'])

            for row in maze.convertedMaze:
                output_writer.writerow(row)
