import sys
import getopt
from Maze import Maze
from Counter import Counter
from Timer import Timer
from TimerTotal import TimerTotal
from csvFileWriter import csvFileWriter
from Calculator import Calculator
from Interfaces import ISolveAlgorithm
from DepthFirst import DepthFirst
from FileFacade import FileFacade


class Controller(object):
    mazes = list()
    sizes = list()
    timerTotals = list()
    counters = list()
    solveAlgorithms = ["dfs"]
    usage = 'Controller.py -s size1,size2,...,sizeN --alg-solve=<name> [-i <inputfile> -o <outputfile>]'
    inputfile = None
    outputfile = None
    # size = None
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
                self.counters.clear()

                for s in self.sizes:
                    # create counter and timertotal for current maze size.
                    self.timerTotals.append(TimerTotal())
                    self.counters.append(Counter())

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
            # todo view.showResults(self.solveMazes())
            print(self.solveMazes())

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
    def solveMazes(self) -> (list, list):
        accCounter: Counter = Counter()
        timer: Timer = Timer()
        accTimer: TimerTotal = TimerTotal()

        if self.solveAlgorithm == "dfs":
            sa: ISolveAlgorithm = DepthFirst()

        else:
            raise NotImplementedError

        timer.StartTimer()
        for maze in self.mazes:
            sa.solve(maze, accCounter)
        timer.EndTimer()

        accTimer.setTotalTimer(timer.GetTimer())

        return (accTimer, accCounter)

        # check if arguments[0] is in sizes
        # check if arguments[1] is in genAlgorithms
        # check if arguments[2] is in solveAlgorithms
        # return int(arguments[0]) in sizes and arguments[1] in genAlgorithms and arguments[2] in solveAlgorithms

        # sizes = [5, 10, 15, 20, 25, 30]
        # runLoop = 2


        # for size in sizes:
        #     print(15 * "*" + str(size) + 15*"*")
        #     timerTotal = TimerTotal()
        #     i = 0
        #     while i < runLoop:
        #         maze = Maze(size)
        #         timer = Timer()
        #         counter = Counter()
        #         solve = Solve(maze, counter)
        #         print(maze.pretty_print())
        #         timer.StartTimer()
        #         # pass in True as last argument to see print outs from search(...)
        #         solve.search(1, 1)
        #         print(counter.GetNumberOfPointsVisitedWithText())
        #         timer.EndTimer()
        #         print(timer.GetTimerWithText())
        #         timerTotal.setTotalTimer(timer.GetTimer())
        #         i += 1
        #     calculator = Calculator(timerTotal.GetTimer(), runLoop)
        #     print(calculator.GetTimerAverage())
if __name__ == '__main__':
    # print(sys.argv[1:])
    c = Controller.getInstance()
    c.runProgram(sys.argv[1:])
