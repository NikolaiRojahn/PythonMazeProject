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

    # state variables.
    WORKING = "working"
    MAZES_GENERATED = "mazesGenerated"
    MAZES_SOLVED = "mazesSolved"
    READY = "ready"  # dummy default state

    # static variables.
    #Mutex er et udtryk for at tråd er låst, og først giver en ny tråd mulighed for at tilgå de resourcer som er låst, når der åbnes igen'
    #Her sættes mutex til "Lock()"-objektet som kommer fra "threading"-modulet
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
        #Laver en tom liste som skal indeholde en subliste med x antal "Maze"-objekter - f.eks. 10 hvis der laves 10 af hver maze.
        self.mazes: list = list()
        #Laver en tom liste som skal indeholde en liste over angivet størrelser f.eks. [5,10,15]
        self.sizes: list = list()
        #Laver en tom liste til brug for observer pattern hvor der kan lægges metoder til brug ved senere "notify"-metode
        self.observers: list = list()
        #Laver et tomt dictionary dette skal senere bruges til at hve hver størrelse/size som key og en liste med "TimerTotal" og "CounterTotal"-objekterne som value
        self.mazeOptions = {}

        self.solveAlgorithm = "dfs"
        self.solveAlgorithms = ["dfs"]

        self._inputfile = None
        self._outputfile = None
        self._fileFacade = None
        self.generatedMazes = None

        self.state = None

        #Initialiserer en tæller startende på 0, denne tæller bruges når vi skal tælle vores tråde op til generering og løsning af mazes for at tjekke om alle tråde er færdige.
        self.count = 0

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

    #Bruges til tråde hvor den tæller en fælles tæller "self.count" op med 1 når tråden er kørt færdig
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
        """Clears sizes, mazes and mazeOptions in the model. """
        self.sizes.clear()
        self.mazes.clear()
        self.mazeOptions = {}
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

    #Generering af en enkelt/single maze, som bruges i tråde
    def generateSingleMaze(self, size, mazeSubList):
        #Danner et Maze-objekt ud fra den størrelse (size) som kommer som input
        obj = Maze(size)
        #Her låser vi den "mazeSubList" som kommer som input da vi skal tilføje en element til listen
        #Efterfølgende kalder vi metoden "self.onEvent()" som tæller den fælles tæller "self.count" op med 1
        self.mutex.acquire()
        mazeSubList.append(obj)
        self.onEvent()
        #Efter ovenstående åbner vi låsen igen og giver adgang for næste tråd til at tilgå de to ovenstående resourcer
        self.mutex.release()
        #Metode som tjekker efter hver tråd om det er den sidste - altså om alle tråede en er færdige
        self.checkGeneratedOrSolved(
            self.MAZES_GENERATED, "All mazes are generated")

    def generateMazes(self):
        """Generates mazes if sizes are set up."""
        if len(self.sizes) <= 0:
            self.setState(Model.READY)
            raise Exception("No maze sizes in system. Try adding sizes first.")

        self.setState(Model.WORKING)

        #Sætter en fælles tæller for tråedene til 0, således at man sikre at tælleren "self.count" starter fra 0
        self.count = 0
        #Nedenstående laver et dictionary hvor hver angiver størrelse/size er key og value er en liste med et "TimerTotal" og "counterTotal"-objekt
        self.makeDictionaryForMazeTimerAndCounter()
        #Gennemløber alle sizes i "self.sizes"-listen
        for size in self.sizes:
            #For hver størrelse danne en subliste som skal indeholde et antal mazes af den angivne størrelse
            mazeSubList = list()
            #Sublisten tilføjes listen "self.mazes".
            self.mazes.append(mazeSubList)
            #Gennemløb af 10 iterationer
            for _ in range(10):
                #Nedenstående angiver en definition af en tråd - "target" er metoden tråden skal køre - "args" er de parameter som "target"-metoden tager ind
                #i vores tilfælde tager den en size som værdi og listen til indsættes af Maze-objektet 
                thread = threading.Thread(
                    target=self.generateSingleMaze, args=(size, mazeSubList))
                #Starter den ovenstående definerede tråd    
                thread.start()

    def solveSingleMaze(self, sa, maze):
        """ Solves a single maze and updates the count of solved mazes in total. """
        # s.acquire()
        #Løser den angivne maze ved hjælp af "solve"-metoden som returnerer en tuple med ("Timer" er tiden for løsningen, "Counter" er antal punkter besøgt for løsningen)
        #Efterfølgende låser vi "self.mazeOptions" dictionary, således at kun denne tråd kan tilgå det og tælle en fælles tæller "self.onEvent"-metoden
        result: (Timer, Counter) = sa.solve(maze.convertedMaze)
        self.mutex.acquire()
        #mazeOptions has TimerTotal on index 0 and CounterTotal on index 1
        #Nedenstående tager size fra den maze som tages ind og slår værdien op i dictionry "[maze.size]" efterfølgende referes til value som er en liste og der for "[]" efterfølgende
        #"[maze.size][0]" er "TimerTotal"-objektet - inde i dette objekt ligger "addTime..."-metode som tager ovenstående "result"-tuple position for "Timer" som er [0] og "getTimer"-metoden
        #"[maze.size][1]" er "CounterTotal"-objektet - inde i dette objekt ligger "addCounter..."-metode som tager ovenstående "result"-tuple position for "Counter" som er [1]
        # og "GetNumberOfPointsVisited"-metoden
        self.mazeOptions[maze.size][0].addTimeToMazeSolutionTimesList(
            result[0].GetTimer())
        self.mazeOptions[maze.size][1].addCounterToMazeSolutionCountersList(
            result[1].GetNumberOfPointsVisited())
        #Efterfølgende kalder vi metoden "self.onEvent()" som tæller den fælles tæller "self.count" op med 1
        self.onEvent()
        #Efter ovenstående åbner vi låsen igen og giver adgang for næste tråd til at tilgå de to ovenstående resourcer
        self.mutex.release()
        #Metode som tjekker efter hver tråd om det er den sidste - altså om alle tråede en er færdige
        self.checkGeneratedOrSolved(
            self.MAZES_SOLVED, "All mazes are solved")
        # s.release()

    def solveMazes(self):
        """Solves mazes using selected solving algorithm."""
        self.setState(Model.WORKING)
        # set up instance of solving algorithm.
        sa: ISolveAlgorithm = None
        if self.solveAlgorithm == "dfs":
            sa: ISolveAlgorithm = DepthFirst()
        else:
            self.setState(Model.READY)
            raise NotImplementedError

        if len(self.mazes) == 0:
            raise Exception(
                "No generated mazes in system. Try generating mazes first.")

        # loop through actual mazes and time the solution.
        #Sætter en fælles tæller for tråedene til 0, således at man sikre at tælleren "self.count" starter fra 0
        self.count = 0
        #s = threading.BoundedSemaphore(3)
        #Gennemløber listen af mazes
        for mazeList in self.mazes:
            #Gennemløb af ovenstående subliste "mazeList" hvor den tager et "Maze"-objekt "maze"
            for maze in mazeList:
                #Nedenstående angiver en definition af en tråd - "target" er metoden tråden skal køre - "args" er de parameter som "target"-metoden tager ind
                #i vores tilfælde tager den en løsningsalgoritme "sa" og et "Maze"-objekt
                thread = threading.Thread(
                    target=self.solveSingleMaze, args=(sa, maze))
                #Starter den ovenstående definerede tråd
                thread.start()

    #Metode til at tjekke for alle tråde er færdig enten for generering af mazes eller løsning af mazes
    def checkGeneratedOrSolved(self, state, text):
        #Tjekker om alle tråde er færdig ved at tjekke om fælles tælleren matcher værdien af "self.count" og længden listen "self.sizes"*gennemløb(10)
        if self.count == (len(self.sizes) * 10):
            # print(text)
            #Hvis ovenstående værdier matcher sættes en ny state og køre "notify"-metoden
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

    #Metode som klargør værdierne til plotning i listerne - listerne returneres i en tuple
    def makeListToPlotting(self) -> (list, list, list, list, list, list, list):
        #Opretter de angivne lister som skal bruges til plotning - kun listen "sizes" har en værdi fra start som er "self.sizes"
        sizes = self.sizes
        minTime: list = list()
        maxTime: list = list()
        avgTime: list = list()
        minIterations: list = list()
        maxIterations: list = list()
        avgIterations: list = list()

        ##Gennemløber hver en key i dictionary "self.mazeOptions" [k] efterfølgende referes til value som er en liste og der for "[]" efterfølgende
        #"[k][0]" er "TimerTotal"-objektet - inde i dette objekt tages 3 metoder og lægger værdierne i listen til plotningen - "get..."-metoderne henter 
        # værdierne fra "TimerTotal"-objektet for den pågældende key [k]
        #"[k][1]" er "CounterTotal"-objektet - inde i dette objekt tages 3 metoder og lægger værdierne i listen til plotningen - "get..."-metoderne henter 
        # værdierne fra "CounterTotal"-objektet for den pågældende key [k]
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

        #Returnerer en tuple med alle ovenstående lister
        return (sizes, minTime, maxTime, avgTime, minIterations, maxIterations, avgIterations)

    #Nedenstående opsætter ovenstående metode med tupler som retur værdi til et samlet Dictionary med færdige lister til plotningen
    def makeDictionaryWithListToPlotting(self) -> {}:
        #Opretter et nyt tomt dictionary med navnet "plottingDict"
        plottingDict = {}

        #Køre metoden "self.makeListToPlotting" og indsætter retur værdi som "result"
        result = self.makeListToPlotting()

        #Nedenstående indsætter hver en liste fra "result"-tuplen ovenfor med en key i "plottingDict" key er defineret i ['tekst']
        #"result"-tuplen indeholder flere lister og derfor er det "result['index']"
        plottingDict["sizes"] = result[0]
        plottingDict["minTime"] = result[1]
        plottingDict["maxTime"] = result[2]
        plottingDict["avgTime"] = result[3]
        plottingDict["minIterations"] = result[4]
        plottingDict["maxIterations"] = result[5]
        plottingDict["avgIterations"] = result[6]

        #Returnerer dictionary "plottingDict"
        return plottingDict

    def makeDictionaryForMazeTimerAndCounter(self):
        #Clear "self.mazeOptions" dictionary således det er fri for gamle værdier og klar ved ny generering 
        self.mazeOptions.clear()
        print("Adding keys to mazeOptions: " + str(self.sizes))
        #Løber hver en størrelse/size igennem
        for size in self.sizes:
            #Tjekker at den nuværende størrelse/size ikke allerede ligger i dictionary - altså at den ikke prøver at danne 2 keys med samme navn
            if size not in self.mazeOptions:
                #Nedenstående danner en key i "self.mazeOptions" dictionary med størrelse/size som key og value med en liste med "TimerTotal" og "CounterTotal"-objekt
                self.mazeOptions[size] = [TimerTotal(), CounterTotal()]
