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


class Model(object):

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
