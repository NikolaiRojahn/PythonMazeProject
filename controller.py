import sys
import getopt
import Exceptions
from Maze import Maze
from Counter import Counter
from CounterTotal import CounterTotal
from Timer import Timer
from TimerTotal import TimerTotal
from csvFileWriter import csvFileWriter
from csvFileReader import csvFileReader
# from Calculator import Calculator
from Interfaces import ISolveAlgorithm, IView
from DepthFirst import DepthFirst
from FileFacade import FileFacade
from Plotting import Plotting
from View import View
from Model import Model
from Gui import GUI


class Controller(object):
    # static variables.
    __instance = None

    @staticmethod
    def getInstance(view: IView, model):
        # is instance reference None, call constructor.
        if Controller.__instance is None:
            Controller(view, model)
        # return the instance
        return Controller.__instance

    # constructor - composition of model, view (dependency injection)
    def __init__(self, view, model):
        self.model = model
        self.view = view
        # observe state changes in the view.
        self.view.attach(self)
        self.model.attach(self.onMazesGenerated)
        self.model.attach(self.onMazesSolved)

        self.state = None

        self.usage = "Controller usage"
        # Virtually private constructor.
        if Controller.__instance is not None:
            raise Exception("Controller is a singleton.")
        else:
            Controller.__instance = self

    def runProgram(self):
        # Start the view's menu and listen for changes.
        self.view.start()

    def update(self, verbose=False) -> str:
        """
        This method is called whenever e.g. state has changed in the object this Controller observes.
        The Controller interprets the new state and handles it by use of its model.
        """
        if (self.view.getState() == self.view.SELECT_ALGORITHM):
            if (verbose):
                print("Setting up selected algorithm for solving to " +
                      self.view.getData())
            return self.model.setSolveAlgorithm(self.view.getData())

        if (self.view.getState() == self.view.READ_FROM_FILE):
            if (verbose):
                print("Reading from " + self.view.getData())
            self.model.inputfile = self.view.getData()

            # catch any low-level exceptions here and translate into user friendly error msg.:
            try:
                self.model.readFile()
                return self.model.inputfile + " was successfully read."
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    self.model.inputfile + " could not be read: " + str(e))
                # return self.model.inputfile + " could not be read: " + str(e)

        if (self.view.getState() == self.view.WRITE_TO_FILE):
            if (verbose):
                print("Writing to file: " + self.view.getData())
            self.model.outputfile = self.view.getData()
            # catch any low-level exceptions here and translate into user friendly error msg.:
            try:
                self.model.writeFile()
                return self.model.outputfile + " was successfully written."
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    self.model.outputfile + " could not be written: " + str(e))

        if (self.view.getState() == self.view.ADD_MAZE_SIZE):
            if (verbose):
                print("Adding size: " + self.view.getData())

            # copy current sizes prior to clearing collections.
            currentSizes = self.model.sizes.copy() if self.model.sizes is not None else list()

            # clear previous collections in model.
            self.model.clearMazeSizes()

            try:
                # split input array
                input = map(lambda x: int(x), self.view.getData().split(','))
                # remove any new values already in current values.
                newSizes = list(filter(lambda x: int(
                    x) not in currentSizes, input))

                allsizes = currentSizes + newSizes
                allsizes.sort()
                # store current and new values in model.
                for size in allsizes:
                    self.model.addMazeSize(int(size))
                return "The following maze sizes are stored: " + str(self.model.sizes)
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "Maze sizes are invalid, " + str(e))

        if (self.view.getState() == self.view.SHOW_MAZE_SIZES):
            if (verbose):
                print("Showing maze sizes...")
            return "The following maze sizes are stored: " + str(self.model.sizes)

        if (self.view.getState() == self.view.CLEAR_MAZE_SIZES):
            if (verbose):
                print("clearing maze sizes...")
            self.model.clearMazeSizes()
            return "Maze sizes cleared: " + str(self.model.sizes)

        if (self.view.getState() == self.view.GENERATE_MAZES):
            if (verbose):
                print("Generating mazes...")
            try:
                self.model.generateMazes()
                return str(len(self.model.sizes) * 10) + " mazes generated."
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "Mazes could not be generated: " + str(e))

        if (self.view.getState() == self.view.SOLVE_MAZES):
            if (verbose):
                print("Solving mazes...")
            try:
                self.model.solveMazes()
                return "Mazes are solved, select 'Show graphs' to see resulting graphs."
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "Mazes could not be solved: " + str(e))

        if (self.view.getState() == self.view.SHOW_GRAPHS):
            if (verbose):
                print("Showing graphs...")
            try:
                #timeTuple = self.model.plottingTimeValues()
                #iterationsTuple = self.model.plottingIterationValues()

                # mazesize, timeMin, timeMax, timeAvg, iterationsMin, iterationsMax, iterationsAvg
                # plotting = Plotting(self.model.sizes, timeTuple[0], timeTuple[2], timeTuple[1],
                #                    iterationsTuple[0], iterationsTuple[2], iterationsTuple[1])

                # print(self.model.makeDictionaryWithListToPlotting())

                # plotting = Plotting(self.model.makeDictionaryWithListToPlotting())

                # plotting.plotting()

                self.model.showGraphs()

                return "Graphs are showing in an external window."

            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "Graphs could not be generated: " + str(e))

    def runProgram2(self, arguments):
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
    # Demonstrates the dependency injection.
    # python Controller.py cli -> CLI UI is used, otherwise GUI.
    args = sys.argv[1:]
    if (len(args) >= 1 and args[0] == "cli"):
        view = View()
    else:
        view = GUI()
    model = Model.getInstance()
    c = Controller.getInstance(view, model)
    c.runProgram()
    # c.runProgram2(sys.argv[1:])
