import sys
import getopt
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


class Controller(object):
    # static variables.
    mazes: list = list()
    sizes: list = list()
    timerTotals: list = list()
    counterTotals: list = list()
    solveAlgorithms = ["dfs"]
    usage = 'Controller.py -s size1,size2,...,sizeN --alg-solve=<name> [-i <inputfile> -o <outputfile>]'
    inputfile = None
    outputfile = None
    solveAlgorithm = None
    generatedMazes = None
    __instance = None

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

        # Virtually private constructor.
        if Controller.__instance is not None:
            raise Exception("Controller is a singleton.")
        else:
            Controller.__instance = self

    def runProgram(self, arguments):

        # run only if arguments are valid
        if self.checkArguments(arguments):

            # if input file is given
            if self.inputfile is not None:
                # read in file
                print("Reading mazes from {}.".format(self.inputfile))
                # todo self.mazes = FileFacade.read(self.inputfile)

                # solve using selected algorithm.
                # todo view.showResults(self.solveMazes())

            else:
                # clear relevant arrays if previously filled.
                self.mazes.clear()
                self.timerTotals.clear()
                self.counterTotals.clear()

                for s in self.sizes:
                    # create counter and timertotal for current maze size.
                    self.timerTotals.append(TimerTotal())
                    self.counterTotals.append(CounterTotal())

                    # create 10 mazes of each given size, store in array.
                    mazeSubList = list()

                    # create 10 mazes of current size.
                    for x in range(10):
                        mazeSubList.insert(x, Maze(s))

                    # store sublist in mazes.
                    self.mazes.append(mazeSubList)

                # if output file is given, write file with mazes.
                if self.outputfile is not None:
                    print("Writing mazes to file...")
                    writer = FileFacade()
                    writer.createWriter(self.mazes, self.outputfile)

            # solve using selected algorithm.
            self.solveMazes()
            # todo call view with needed info
            for i, timerTotal in enumerate(self.timerTotals):
                print("{}".format(i), str(
                    timerTotal.getAverageTimeForMazeSolutionTimes()), str(timerTotal))

            for i, counterTotal in enumerate(self.counterTotals):
                print("{}".format(i), str(
                    counterTotal.getAverageCounterForMazeSolutionCounters()), str(counterTotal))

            self.plottingValues()

        else:
            sys.exit()

    # Checks arguments and sets up globals.
    # If values are invalid, an error message is displayed.

    def checkArguments(self, arguments):
        try:
            opts, args = getopt.getopt(
                arguments, "hs:i:o:", ["alg-generate", "alg-solve"])
        except getopt.GetoptError as err:
            print(err.msg + "\n" + self.usage)
            return False

        for opt, arg in opts:
            if opt == '-h':  # help
                print(self.usage)
                sys.exit(0)
            elif opt == '-s':  # maze sizes
                # try to split arg into array.
                argArray = arg.split(',')
                # convert to ints and append to sizes.
                for s in argArray:
                    self.sizes.append(int(s))
                # if int(arg) not in self.sizes:
                #   print("Requested size not valid.")
                if len(self.sizes) <= 0:
                    print("Requested sizes are not valid.")
                    return False
                # else:
                #     self.size = int(arg)
            elif opt == '-i':  # input file
                self.inputfile = arg
            elif opt == '-o':  # output file
                self.outputfile = arg
            elif opt == '--alg-solve':
                if arg in self.solveAlgorithms:
                    self.solveAlgorithm = arg
                else:
                    self.solveAlgorithm = self.solveAlgorithms[0]

        return True

    # helper method that solves mazes with selected algorithm and returns a tuple with lists of total time and steps.
    def solveMazes(self):

        # set up instance of solving algorithm.
        if self.solveAlgorithm == "dfs":
            sa: ISolveAlgorithm = DepthFirst()
        else:
            raise NotImplementedError

        # loop through outer maze container collection.
        for i, mazeList in enumerate(self.mazes):

            # get corresponding TimerTotal and Counter objects.
            timerTotal = self.timerTotals[i]

            counterTotal = self.counterTotals[i]
            counter = Counter()
            # loop through actual mazes and time the solution.
            for maze in mazeList:
                timer = Timer()
                timer.StartTimer()
                sa.solve(maze, counter)
                timer.EndTimer()

                timerTotal.addTimeToMazeSolutionTimesList(timer.GetTimer())
                counterTotal.addCounterToMazeSolutionCountersList(counter)

    def plottingValues(self):
        minTime = []
        maxTime = []
        avgTime = []

        for i, j in enumerate(self.sizes):
            timerTotal = self.timerTotals[i]
            minTime.append(timerTotal.getMinimumTimeForMazeSolutionTimes())
            maxTime.append(timerTotal.getMaximumTimeForMazeSolutionTimes())
            avgTime.append(timerTotal.getAverageTimeForMazeSolutionTimes())

        print("mazesize = " + str(self.sizes))
        print("minTime = " + str(minTime))
        print("maxTime = " + str(maxTime))
        print("avgTime = " + str(avgTime))


if __name__ == '__main__':
    # print(sys.argv[1:])
    c = Controller.getInstance()
    c.runProgram(sys.argv[1:])
