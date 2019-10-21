import sys
import getopt
from Maze import Maze
from Counter import Counter
from Timer import Timer
from TimerTotal import TimerTotal
from Solve import Solve
from Calculator import Calculator


class Controller(object):

    sizes = [5, 10, 15, 20, 25, 30]
    genAlgorithms = ["dfg"]
    solveAlgorithms = ["dfs"]
    usage = 'Controller.py -s <size> [-i <inputfile> -o <outputfile> --alg-generate=<name> --alg-solve=<name>]'
    inputfile = None
    outputfile = None
    size = None
    genAlgorithm = None
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
                print("here we will read in {}.".format(self.inputfile))
                # parse the read in labyrinths.
                # solve using selected algorithm.
            else:  # (no input file)
                pass
                # create using chosen algorithm.
                # if output file is given
                # write file with mazes.
                # solve using selected algorithm.

        else:
            sys.exit()

    def createMazes(self, numLoops: int, size: int, genAlgorithm: str):
        pass

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
            elif opt == '-s':  # maze size
                if int(arg) not in self.sizes:
                    print("Requested size not valid.")
                    return False
                else:
                    self.size = int(arg)
            elif opt == '-i':  # input file
                self.inputfile = arg
            elif opt == '-o':  # output file
                self.outputfile = arg
            elif opt == '--alg-generate':
                if arg in self.genAlgorithms:
                    self.genAlgorithm = arg
                else:
                    self.genAlgorithm = self.genAlgorithms[0]
            elif opt == '--alg-solve':
                if arg in self.solveAlgorithms:
                    self.solveAlgorithm = arg
                else:
                    self.solveAlgorithm = self.solveAlgorithms[0]

        return True
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
