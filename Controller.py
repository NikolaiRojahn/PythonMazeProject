import sys
import getopt
from collections import namedtuple
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
        # create a namedtuple to use as return value from update()
        self.updateTuple = namedtuple('updateTuple', 'text obj')

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
        # Start the view.
        self.view.start()

    def update(self, verbose=False) -> ():
        """
        This method is called whenever state has changed in the object this Controller observes.
        The Controller interprets the new state and handles it by use of its model.
        The method then returns an updateTuple with named properties 'text' and 'obj'.
        If the model is working, the controller blocks any action as it awaits the model returning.
        """
        if (model.getState() == Model.WORKING):
            raise Exceptions.UserFriendlyException(
                "Model is busy!\nPlease wait...")

        if (self.view.getState() == self.view.SELECT_ALGORITHM):
            algorithm = self.view.getData()
            if (verbose):
                print("Setting up selected algorithm for solving to " +
                      algorithm)
            # create updateTuple and return it.
            return self.updateTuple(text=self.model.setSolveAlgorithm(algorithm), obj=None)
            # return self.model.setSolveAlgorithm(self.view.getData())

        if (self.view.getState() == self.view.READ_FROM_FILE):
            filename = self.view.getData()
            if (verbose):
                print("Reading from " + filename)
            self.model.inputfile = filename

            # catch any low-level exceptions here and translate into user friendly error msg.:
            try:
                self.model.readFile()
                return self.updateTuple(text=self.model.inputfile + " was successfully read.", obj=None)
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "The file '" + self.model.inputfile + "' could not be read.\n" + str(e))
                # return self.model.inputfile + " could not be read: " + str(e)

        if (self.view.getState() == self.view.WRITE_TO_FILE):
            filename = self.view.getData()
            if (verbose):
                print("Writing to file: " + filename)
            self.model.outputfile = filename
            # catch any low-level exceptions here and translate into user friendly error msg.:
            try:
                self.model.writeFile()
                return self.updateTuple(text=self.model.outputfile + " was successfully written.", obj=None)
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "The file '" + self.model.outputfile + "' could not be written.")

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
                return self.updateTuple(text="The following maze sizes are stored: " + str(self.model.sizes), obj=None)
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "Maze sizes are invalid, " + str(e))

        if (self.view.getState() == self.view.SHOW_MAZE_SIZES):
            if (verbose):
                print("Showing maze sizes...")
            return self.updateTuple(text="The following maze sizes are stored: " + str(self.model.sizes), obj=None)

        if (self.view.getState() == self.view.CLEAR_MAZE_SIZES):
            if (verbose):
                print("clearing maze sizes...")
            self.model.clearMazeSizes()
            return self.updateTuple(text="Maze sizes cleared: " + str(self.model.sizes), obj=None)

        if (self.view.getState() == self.view.GENERATE_MAZES):
            if (verbose):
                print("Generating mazes...")
            try:
                self.model.generateMazes()
                return self.updateTuple(text="Generating mazes, please wait...", obj=None)
                # return self.updateTuple(text=str(len(self.model.sizes) * 10) + " mazes generated.", obj=None)
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "Mazes could not be generated: " + str(e))

        if (self.view.getState() == self.view.SOLVE_MAZES):
            if (verbose):
                print("Solving mazes...")
            try:
                self.model.solveMazes()
                return self.updateTuple(text="Solving mazes, please wait...", obj=None)
                # return self.updateTuple(text="Mazes are solved, select 'Show graphs' to see resulting graphs.", obj=None)
            except BaseException as e:
                raise Exceptions.UserFriendlyException(
                    "Mazes could not be solved: " + str(e))

        if (self.view.getState() == self.view.SHOW_GRAPHS):

            if (verbose):
                print("Showing graphs...")
            try:
                if isinstance(self.view, GUI):
                    pyplot = self.model.makeGraphs(True)
                    return self.updateTuple(text="Showing graphs.", obj=pyplot)
                else:
                    pyplot = self.model.makeGraphs(False)
                    self.model.showGraphs(pyplot)
                    return self.updateTuple(text="Graphs are showing in an external window.", obj=None)

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
        """ Called whenever the model has generated all requested mazes."""
        if self.model.getState() == Model.MAZES_GENERATED:
            print("onMazesGenerated called.")

    def onMazesSolved(self):
        """ Called whenever the model has solved all mazes. """
        if self.model.getState() == Model.MAZES_SOLVED:
            print("onMazesSolved")


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