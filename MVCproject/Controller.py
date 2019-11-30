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
    __instance = None

    @staticmethod
    def getInstance(model):
        # is instance reference None, call constructor.
        if Controller.__instance is None:
            Controller(model)
        # return the instance
        return Controller.__instance

    # constructor - composition of model, view (dependency injection)
    def __init__(self, model):
        self.model = model
        self.model.attach(self)

        self.state = None

        self.usage = "Controller usage"
        # Virtually private constructor.
        if Controller.__instance is not None:
            raise Exception("Controller is a singleton.")
        else:
            Controller.__instance = self

    def runProgram(self, arguments):
        result = self.model.setup(arguments)

        if(result is True):
            if self.model.inputfile is not None:
                self.model.readFile()
                self.model.solveMazes()
                if self.onMazesSolved() is True:
                    self.model.showGraphs()
            if self.model.inputfile is None:
                self.model.generateMazes()
                if self.onMazesGenerated() is True:
                    if self.model.outputfile is not None:
                        self.model.writeFile()
                    self.model.solveMazes()
                    if self.onMazesSolved() is True:
                        self.model.showGraphs()
        else:
            print(result)
            exit(1)

    def update(self):
        self.onMazesGenerated()
        self.onMazesSolved()

    def onMazesGenerated(self):
        self.state = self.model.getState()
        if (self.state == self.model.MAZES_GENERATED):
            return True
        return False

    def onMazesSolved(self):
        self.state = self.model.getState()
        if (self.state == self.model.MAZES_SOLVED):
            return True
        return False

if __name__ == '__main__':
    model = Model.getInstance()
    c = Controller.getInstance(model)
    c.runProgram(sys.argv[1:])