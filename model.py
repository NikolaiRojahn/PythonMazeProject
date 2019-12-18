# The Model is a container for all class files that reside in the conceptual model.
# Thus, the Model is a Facade towards these underlying class files exposing a public interface for clients.
# The Model is implemented as a singleton.
from Maze import Maze
from Counter import Counter
from CounterTotal import CounterTotal
from Timer import Timer
from TimerTotal import TimerTotal
from csvFileWriter import csvFileWriter
# from Calculator import Calculator
from Interfaces import ISolveAlgorithm
from DepthFirst import DepthFirst
from FileFacade import FileFacade
from Plotting import Plotting
# from Threadpool import ThreadPool
# from threading import Thread, Lock, BoundedSemaphore
from threading import Thread, Lock, Semaphore
import threading
import getopt
import time
import matplotlib


class Model(object):

    # static variables.
    mutex = Lock()
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
        self.observers: list = list()
        self.mazeOptions = {}

        self.solveAlgorithm = "dfs"
        self.solveAlgorithms = ["dfs"]

        self._inputfile = None
        self._outputfile = None
        self._fileFacade = None
        self.generatedMazes = None

        self.state = None

        self.count = 0

        self.MAZES_GENERATED = "mazesGenerated"
        self.MAZES_SOLVED = "mazesSolved"

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

    # @property
    def getState(self):
        return self.state

    # @property
    def setState(self, value):
        self.state = value

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.remove(observer)

    def onEvent(self):
        self.count += 1

    def notify(self):
        for observer in self.observers:
            observer()

    def setup(self, arguments):
        """Checks validity and presence of arguments and sets up the model."""
        result = True  # return value presuming all is ok.

        try:
            opts, _ = getopt.getopt(
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
                if argArray[0][:1] == '-':
                    result = "Requested sizes are not valid."
                # convert to ints and append to sizes.
                for s in argArray:
                    self.addMazeSize(int(s))
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
        # self.timerTotals.append(TimerTotal())
        # self.counterTotals.append(CounterTotal())

    def clearMazeSizes(self):
        """Clears sizes, mazes, timerTotals and counterTotals in the model. """
        self.sizes.clear()
        self.mazes.clear()
        # self.timerTotals.clear()
        # self.counterTotals.clear()

    def setSolveAlgorithm(self, arg: str) -> str:
        """
        Sets the solving algorithm. If arg is invalid, the solving algorithm defaults to "dfs".
        POST: Returns a string confirmation.
        """
        if arg in self.solveAlgorithms:
            self.solveAlgorithm = arg
        return "Solve algorithm set to " + self.solveAlgorithm

    def addSolvingAlgorithm(self, arg: str):
        """Adds an alias for a solving algorithm to the collection"""
        self.solveAlgorithms.append(arg)

    def readFile(self) -> str:
        """Reads from file if input file is set up."""
        if self.inputfile is not None:
            if self._fileFacade is None:
                self._fileFacade = FileFacade.getInstance()
            result = self._fileFacade.read(self.inputfile)

            # clear previous collections.
            self.clearMazeSizes()
            self.mazes = result[0]  # the array of all mazes.
            self.sizes = result[1]  # the sizes read in from file.
            self.makeDictionaryForMazeTimerAndCounter()

    def generateSingleMaze(self, size, mazeSubList):
        obj = Maze(size)
        self.mutex.acquire()
        mazeSubList.append(obj)
        self.onEvent()
        self.mutex.release()
        self.checkGeneratedOrSolved(self.MAZES_GENERATED, "All mazes are generated")

    def generateMazes(self):
        """Generates mazes if sizes are set up."""
        if len(self.sizes) <= 0:
            raise Exception("No maze sizes in system. Try adding sizes first.")

        # self.mazes.clear()
        self.count = 0
        #s = threading.BoundedSemaphore(3)
        #s = threading.Semaphore(3)
        self.makeDictionaryForMazeTimerAndCounter()
        for size in self.sizes:
            mazeSubList = list()
            self.mazes.append(mazeSubList)
            for _ in range(10):
                thread = threading.Thread(target=self.generateSingleMaze, args=(size, mazeSubList))
                thread.start()
                #s.acquire()
                #obj = Maze(size)
                #self.mutex.acquire()
                #mazeSubList.append(obj)
                #self.onEvent()
                #self.mutex.release()
                #s.release()
        #self.checkGeneratedOrSolved(
        #    self.MAZES_GENERATED, "All mazes are generated")

    # def generateMazes(self):
    #     """Generates mazes if sizes are set up."""
    #     if len(self.sizes) <= 0:
    #         raise Exception("No maze sizes in system. Try adding sizes first.")

    #     # self.mazes.clear()
    #     self.count = 0
    #     #s = threading.BoundedSemaphore(3)
    #     s = threading.Semaphore(3)
    #     self.makeDictionaryForMazeTimerAndCounter()
    #     for size in self.sizes:
    #         mazeSubList = list()
    #         self.mazes.append(mazeSubList)
    #         for _ in range(10):
    #             s.acquire()
    #             obj = Maze(size)
    #             self.mutex.acquire()
    #             mazeSubList.append(obj)
    #             self.onEvent()
    #             self.mutex.release()
    #             s.release()
    #     self.checkGeneratedOrSolved(
    #         self.MAZES_GENERATED, "All mazes are generated")  

    def solveSingleMaze(self, sa, maze):
        #s.acquire()
        result: (Timer, Counter) = sa.solve(maze.convertedMaze)
        self.mutex.acquire()
        self.mazeOptions[maze.size][0].addTimeToMazeSolutionTimesList(
            result[0].GetTimer())
        self.mazeOptions[maze.size][1].addCounterToMazeSolutionCountersList(
            result[1].GetNumberOfPointsVisited())
        self.onEvent()
        self.mutex.release()
        self.checkGeneratedOrSolved(self.MAZES_SOLVED, "All mazes are solved")
        #s.release() 

    def solveMazes(self):
        """Solves mazes using selected solving algorithm."""
        # set up instance of solving algorithm.
        sa: ISolveAlgorithm = None
        if self.solveAlgorithm == "dfs":
            sa: ISolveAlgorithm = DepthFirst()
        else:
            raise NotImplementedError

        if len(self.mazes) == 0:
            raise Exception(
                "No generated mazes in system. Try generating mazes first.")

        # # loop through outer maze container collection.
        # for i, mazeList in enumerate(self.mazes):
        #     # get corresponding TimerTotal and Counter objects.
        #     timerTotal = self.timerTotals[i]
        #     counterTotal = self.counterTotals[i]

        #     # loop through actual mazes and time the solution.
        #     for maze in mazeList:
        self.count = 0
        #s = threading.BoundedSemaphore(3)
        for mazeList in self.mazes:
            for maze in mazeList:

        #         s.acquire()
        #         result: (Timer, Counter) = sa.solve(maze.convertedMaze)
        #         self.mutex.acquire()
        #         self.mazeOptions[maze.size][0].addTimeToMazeSolutionTimesList(
        #             result[0].GetTimer())
        #         self.mazeOptions[maze.size][1].addCounterToMazeSolutionCountersList(
        #             result[1].GetNumberOfPointsVisited())
        #         self.onEvent()
        #         self.mutex.release()
        #         s.release()
        # self.checkGeneratedOrSolved(self.MAZES_SOLVED, "All mazes are solved")

                thread = threading.Thread(target=self.solveSingleMaze, args=(sa, maze))
                thread.start()
                #-------------
                #result: (Timer, Counter) = sa.solve(maze)
                #self.mazeOptions[maze.size][0].addTimeToMazeSolutionTimesList(
                #result[0].GetTimer())
                #self.mazeOptions[maze.size][1].addCounterToMazeSolutionCountersList(
                #result[1].GetNumberOfPointsVisited())
                #-------------
                #s.acquire()
                #result: (Timer, Counter) = sa.solve(maze)
                #self.mutex.acquire()
                #self.mazeOptions[maze.size][0].addTimeToMazeSolutionTimesList(
                #    result[0].GetTimer())
                #self.mazeOptions[maze.size][1].addCounterToMazeSolutionCountersList(
                #    result[1].GetNumberOfPointsVisited())
                #self.onEvent()
                #self.mutex.release()
                #s.release()
        #self.checkGeneratedOrSolved(self.MAZES_SOLVED, "All mazes are solved")        

    # def solveMazes(self):
    #     """Solves mazes using selected solving algorithm."""
    #     # set up instance of solving algorithm.
    #     sa: ISolveAlgorithm = None
    #     if self.solveAlgorithm == "dfs":
    #         sa: ISolveAlgorithm = DepthFirst()
    #     else:
    #         raise NotImplementedError

    #     if len(self.mazes) == 0:
    #         raise Exception(
    #             "No generated mazes in system. Try generating mazes first.")

    #     # # loop through outer maze container collection.
    #     # for i, mazeList in enumerate(self.mazes):
    #     #     # get corresponding TimerTotal and Counter objects.
    #     #     timerTotal = self.timerTotals[i]
    #     #     counterTotal = self.counterTotals[i]

    #     #     # loop through actual mazes and time the solution.
    #     #     for maze in mazeList:
    #     self.count = 0
    #     s = threading.BoundedSemaphore(3)
    #     for mazeList in self.mazes:
    #         for maze in mazeList:
    #             s.acquire()
    #             result: (Timer, Counter) = sa.solve(maze)
    #             self.mutex.acquire()
    #             self.mazeOptions[maze.size][0].addTimeToMazeSolutionTimesList(
    #                 result[0].GetTimer())
    #             self.mazeOptions[maze.size][1].addCounterToMazeSolutionCountersList(
    #                 result[1].GetNumberOfPointsVisited())
    #             self.onEvent()
    #             self.mutex.release()
    #             s.release()
    #     self.checkGeneratedOrSolved(self.MAZES_SOLVED, "All mazes are solved")


    def checkGeneratedOrSolved(self, state, text):
        if self.count == (len(self.sizes) * 10):
            # print(text)
            self.setState(state)
            self.notify()

    def writeFile(self):
        """Writes mazes to file if output file is set up."""
        if self.outputfile is not None:
            if self._fileFacade is None:
                self._fileFacade = FileFacade.getInstance()
            if (len(self.mazes) > 0):
                self._fileFacade.write(self.mazes, self.outputfile, self.sizes)
            else:
                raise Exception(
                    "No generated mazes to write to file. Try generating mazes first.")

    def makeGraphs(self, gui: bool = False) -> matplotlib.pyplot:
        """Calls plotting lib for showing graphs of maze solving times and iterations.
           If gui is true, the matplotlib.pyplot instance is returned to the controller. """
        self.plotting = Plotting(self.makeDictionaryWithListToPlotting())
        return self.plotting.plotting(gui)

    def showGraphs(self, plt: matplotlib.pyplot):
        """Displays graphs in external window. Ideal for use cases with CLI-like views"""
        if self.plotting != None:
            self.plotting.showGraphs(plt)
        else:
            raise BaseException(
                "Plotting could not be opened in external window. No self.plotting in Model instance.")

    def makeListToPlotting(self) -> (list, list, list, list, list, list, list):
        sizes = self.sizes
        minTime: list = list()
        maxTime: list = list()
        avgTime: list = list()
        minIterations: list = list()
        maxIterations: list = list()
        avgIterations: list = list()

        for k in self.mazeOptions:
            minTime.append(
                self.mazeOptions[k][0].getMinimumTimeForMazeSolutionTimes())
            maxTime.append(
                self.mazeOptions[k][0].getMaximumTimeForMazeSolutionTimes())
            avgTime.append(
                self.mazeOptions[k][0].getAverageTimeForMazeSolutionTimes())
            minIterations.append(
                self.mazeOptions[k][1].getMinimumCounterForMazeSolutionCounters())
            maxIterations.append(
                self.mazeOptions[k][1].getMaximumCounterForMazeSolutionCounters())
            avgIterations.append(
                self.mazeOptions[k][1].getAverageCounterForMazeSolutionCounters())

        return (sizes, minTime, maxTime, avgTime, minIterations, maxIterations, avgIterations)

    def makeDictionaryWithListToPlotting(self) -> {}:
        plottingDict = {}

        result = self.makeListToPlotting()

        plottingDict["sizes"] = result[0]
        plottingDict["minTime"] = result[1]
        plottingDict["maxTime"] = result[2]
        plottingDict["avgTime"] = result[3]
        plottingDict["minIterations"] = result[4]
        plottingDict["maxIterations"] = result[5]
        plottingDict["avgIterations"] = result[6]

        return plottingDict

    def makeDictionaryForMazeTimerAndCounter(self):
        self.mazeOptions.clear()
        for size in self.sizes:
            if size not in self.mazeOptions:
                self.mazeOptions[size] = [TimerTotal(), CounterTotal()]
