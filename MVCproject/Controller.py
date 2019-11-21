import sys
import getopt
from Maze import Maze
from Counter import Counter
from CounterTotal import CounterTotal
from Timer import Timer
from TimerTotal import TimerTotal
from csvFileWriter import csvFileWriter
from csvFileReader import csvFileReader
from Calculator import Calculator
from Interfaces import ISolveAlgorithm
from DepthFirst import DepthFirst
from FileFacade import FileFacade
from Plotting import Plotting

from Model import Model


class Controller(object):
    # static variables.
    mazes: list = list()
    sizes: list = list()
    timerTotals: list = list()
    counterTotals: list = list()
    solveAlgorithms = ["dfs"]

    inputfile = None
    outputfile = None
    solveAlgorithm = None
    generatedMazes = None
    __instance = None
    fileHandler = FileFacade()

    @staticmethod
    def getInstance():
        # is instance reference None, call constructor.
        if Controller.__instance is None:
            Controller()
        # return the instance
        return Controller.__instance

    # constructor - composition of model, view (dependency injection)
    # def __init__(self, model, view):
    def __init__(self):
        pass
        # self.model = model
        # self.view = view
        self.usage = "Controller usage"
        # Virtually private constructor.
        if Controller.__instance is not None:
            raise Exception("Controller is a singleton.")
        else:
            Controller.__instance = self

    def runProgram(self, arguments):
        # Pseudo code:
        # 1. check arguments
        # 2. set values on model facade
        # 3. read from file
        # 4. generate mazes
        # 5. write mazes to file
        # 6. solve mazes
        # 7. show graphs of solving mazes.

        # get instance of model.
        model: Model = Model.getInstance()

        # get result of setting up model, either True or String
        result = model.setup(arguments)

        if(result is True):
            # 3. read from file
            if model.inputfile is not None:
                model.readFile()
            # 4. generate mazes
            if model.inputfile is None:
                model.generateMazes()
            # 5. write mazes to file
            if model.outputfile is not None:
                model.writeFile()
            # 6. solve mazes
            model.solveMazes()
            # 7. show graphs of solving mazes.
            model.showGraphs()
        else:
            print(result)
            exit(1)


if __name__ == '__main__':
    # print(sys.argv[1:])
    c = Controller.getInstance()
    c.runProgram(sys.argv[1:])
