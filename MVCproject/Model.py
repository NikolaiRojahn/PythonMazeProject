# The Model is a container for all class files that reside in the conceptual model.
# Thus, the Model is a Facade towards these underlying class files exposing a public interface for clients.
# The Model is implemented as a singleton.
from Maze import Maze
from Counter import Counter
from CounterTotal import CounterTotal
from Timer import Timer
from TimerTotal import TimerTotal
from csvFileWriter import csvFileWriter
from Calculator import Calculator
from Interfaces import ISolveAlgorithm
from DepthFirst import DepthFirst
from FileFacade import FileFacade
from Plotting import Plotting
import getopt


class Model(object):

    # static variables.
    # mazes: list = list()
    # sizes: list = list()
    # timerTotals: list = list()
    # counterTotals: list = list()

    # solveAlgorithm = "dfs"
    # solveAlgorithms = ["dfs"]

    # inputfile = None
    # outputfile = None
    # generatedMazes = None
    __instance = None
    usage = 'Controller.py -s size1,size2,...,sizeN --alg-solve=<name> [-i <inputfile> -o <outputfile>]'

    @staticmethod
    def getInstance():
        # if instance is None, call constructor
        if Model.__instance is None:
            Model()
        # return instance
        return Model.__instance

    # constructor
    def __init__(self):
        # do we already have an instance, raise exeption.
        if Model.__instance is not None:
            raise Exception(
                "Model is a singleton, use Model.getInstance() to obtain instance.")
        else:  # no instance yet, store self as instance.
            Model.__instance = self

            # set up instance variables.
            self.mazes: list = list()
            self.sizes: list = list()
            self.timerTotals: list = list()
            self.counterTotals: list = list()

            self.solveAlgorithm = "dfs"
            self.solveAlgorithms = ["dfs"]

            self._inputfile = None
            self._outputfile = None
            self._fileFacade = None
            self.generatedMazes = None

    # inputfile getter
    @property
    def inputfile(self):
        return self._inputfile
    # inputfile setter
    @inputfile.setter
    def inputfile(self, value: str):
        self._inputfile = value

    # outputfile getter
    @property
    def outputfile(self):
        return self._outputfile
    # outputfile setter
    @outputfile.setter
    def outputfile(self, value: str):
        self._outputfile = value

    def setup(self, arguments):
        """Checks validity and presence of arguments and sets up the model."""
        result = True  # return value presuming all is ok.

        try:
            opts, args = getopt.getopt(
                arguments, "hs:i:o:", ["alg-generate", "alg-solve"])
        except getopt.GetoptError as err:
            result = err.msg + "\n" + self.usage

        for opt, arg in opts:

            print("opt: " + opt + ", arg: " + arg)
            if opt == '-h':  # help
                result = self.usage
            elif opt == '-s':  # maze sizes
                # try to split arg into array.
                argArray = arg.split(',')
                # convert to ints and append to sizes.
                for s in argArray:
                    self.addMazeSize(int(s))
                if len(self.sizes) <= 0:
                    result = "Requested sizes are not valid."
            elif opt == '-i':  # input file
                self.inputfile = arg
            elif opt == '-o':  # output file
                self.outputfile = arg
            elif opt == '--alg-solve':
                self.setSolveAlgorithm(arg)

        return result

    def addMazeSize(self, size: int):
        """Adds a maze size, TimerTotal and CounterTotal objects to the collections."""
        self.sizes.append(abs(size))
        self.timerTotals.append(TimerTotal())
        self.counterTotals.append(CounterTotal())

    # def setInputFile(self, arg: str):
    #     """Sets input file to read from."""
    #     self.inputfile = arg

    # def setOutputFile(self, arg: str):
    #     """Sets output file to write to."""
    #     self.outputfile = arg

    def setSolveAlgorithm(self, arg):
        """Sets the solving algorithm. If arg is invalid, the solving algorithm defaults to "dfs"."""
        if arg in self.solveAlgorithms:
            self.solveAlgorithm = arg

    def addSolvingAlgorithm(self, arg: str):
        """Adds an alias for a solving algorithm to the collection"""
        self.solveAlgorithms.append(arg)

    def readFile(self):
        """Reads from file if input file is set up."""
        if self.inputfile is not None:
            if self._fileFacade is None:
                self._fileFacade = FileFacade.getInstance()
            result = self._fileFacade.read(self.inputfile)

            self.mazes = result[0]  # the array of all mazes.
            self.sizes = result[1]  # the sizes read in from file.

            # print(self.mazes)

            # add counters and timers to collections, needed for calculating averages for plotting.
            for size in self.sizes:
                self.timerTotals.append(TimerTotal())
                self.counterTotals.append(CounterTotal())

    def generateMazes(self):
        """Generates mazes if sizes are set up."""
        for size in self.sizes:
            # create 10 mazes of each given size, store in placeholder array.
            mazeSubList = list()
            for x in range(10):
                mazeSubList.insert(x, Maze(size))

            # store sublist in mazes.
            self.mazes.append(mazeSubList)
            # print(self.mazes)

    def solveMazes(self):
        """Solves mazes using selected solving algorithm."""
        # set up instance of solving algorithm.
        sa: ISolveAlgorithm = None
        if self.solveAlgorithm == "dfs":
            sa: ISolveAlgorithm = DepthFirst()
        else:
            raise NotImplementedError

        # loop through outer maze container collection.
        for i, mazeList in enumerate(self.mazes):

            # get corresponding TimerTotal and Counter objects.
            timerTotal = self.timerTotals[i]
            counterTotal = self.counterTotals[i]
            # counter = Counter()
            # loop through actual mazes and time the solution.
            for maze in mazeList:
                print(maze)
                result: (Timer, Counter) = sa.solve(maze)
                timerTotal.addTimeToMazeSolutionTimesList(
                    result[0].GetTimer())
                counterTotal.addCounterToMazeSolutionCountersList(
                    result[1].GetNumberOfPointsVisited())
                result = None

    def writeFile(self):
        """Writes mazes to file if output file is set up."""
        if self.outputfile is not None:
            if self._fileFacade is None:
                self._fileFacade = FileFacade.getInstance()
            self._fileFacade.write(self.mazes, self.outputfile, self.sizes)

    def showGraphs(self):
        """Calls plotting lib for showing graphs of maze solving times and iterations."""
        timeTuple = self.plottingTimeValues()
        iterationsTuple = self.plottingIterationValues()

        # mazesize, timeMin, timeMax, timeAvg, iterationsMin, iterationsMax, iterationsAvg
        plotting = Plotting(self.sizes, timeTuple[0], timeTuple[2], timeTuple[1],
                            iterationsTuple[0], iterationsTuple[2], iterationsTuple[1])

        plotting.plotting()

    def plottingTimeValues(self) -> (list, list, list):
        """Calculates min, avg and max times for each maze size."""
        minTime = []
        avgTime = []
        maxTime = []

        for i, j in enumerate(self.sizes):
            timerTotal = self.timerTotals[i]
            minTime.append(timerTotal.getMinimumTimeForMazeSolutionTimes())
            avgTime.append(timerTotal.getAverageTimeForMazeSolutionTimes())
            maxTime.append(timerTotal.getMaximumTimeForMazeSolutionTimes())

        return (minTime, avgTime, maxTime)

    def plottingIterationValues(self) -> (list, list, list):
        """Calculates min, avg and max iterations for each maze size."""
        minIterations = []
        avgIterations = []
        maxIterations = []

        for i, j in enumerate(self.sizes):
            counterTotal = self.counterTotals[i]
            minIterations.append(
                counterTotal.getMinimumCounterForMazeSolutionCounters())
            avgIterations.append(
                counterTotal.getAverageCounterForMazeSolutionCounters())
            maxIterations.append(
                counterTotal.getMaximumCounterForMazeSolutionCounters())

        return (minIterations, avgIterations, maxIterations)
