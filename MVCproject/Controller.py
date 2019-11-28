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

    # @staticmethod
    # def getInstance():
    #     # is instance reference None, call constructor.
    #     if Controller.__instance is None:
    #         Controller()
    #     # return the instance
    #     return Controller.__instance

    @staticmethod
    def getInstance(model):
        # is instance reference None, call constructor.
        if Controller.__instance is None:
            Controller(model)
        # return the instance
        return Controller.__instance

    # # constructor - composition of model, view (dependency injection)
    # def __init__(self):
    #     pass
    #     self.usage = "Controller usage"
    #     # Virtually private constructor.
    #     if Controller.__instance is not None:
    #         raise Exception("Controller is a singleton.")
    #     else:
    #         Controller.__instance = self

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
        model.setup(arguments)

    def update(self):
        self.state = self.model.getState()

        if (self.state == self.model.SIZES_INPUT):
            self.model.generateMazes()

        if (self.state == self.model.SIZES_INPUT_TO_FILE):
            self.model.writeFile()

        if (self.state == self.model.SIZES_INPUTFILE):
            self.model.readFile()

        if (self.state == self.model.MAZES_SOLVE):
            self.model.solveMazes()

        if (self.state == self.model.MAZES_PLOTTING):
            self.model.showGraphs()

    # def runProgram(self, arguments):
    #     # get instance of model.
    #     model: Model = Model.getInstance()

    #     model.attach(model.solveMazes) # attach solving mazes to observer pattern
    #     model.attach(model.showGraphs) # attach method for show plotting to observer pattern
    #     model.attach(model.writeFile) # attach method for write mazes to file

    #     # get result of setting up model, either True or String
    #     result = model.setup(arguments)

    #     # attach methods to run later after threads for generating mazes is finish
    #     #model.attach(model.solveMazes) # attach solving mazes to observer pattern
    #     #model.attach(model.showGraphs) # attach method for show plotting to observer pattern
    #     #if model.outputfile is not None: # attach method for write mazes to file
    #     #    model.attach(model.writeFile)

    #     if(result is True):
    #         # Read from file
    #         if model.inputfile is not None:
    #             model.detach(model.observers[0]) # detach methods for solve mazes from observer pattern - run directly in model
    #             model.readFile()
    #         # Generate mazes
    #         if model.inputfile is None:
    #             model.generateMazes()
    #         # Write mazes to file
    #         #if model.outputfile is not None:
    #         #    model.attach(model.writeFile)
    #     else:
    #         print(result)
    #         exit(1)

if __name__ == '__main__':
    model = Model.getInstance()
    c = Controller.getInstance(model)
    c.runProgram(sys.argv[1:])


# import sys
# import getopt
# from Maze import Maze
# from Counter import Counter
# from CounterTotal import CounterTotal
# from Timer import Timer
# from TimerTotal import TimerTotal
# from csvFileWriter import csvFileWriter
# from csvFileReader import csvFileReader
# from Calculator import Calculator
# from Interfaces import ISolveAlgorithm
# from DepthFirst import DepthFirst
# from FileFacade import FileFacade
# from Plotting import Plotting
# from Model import Model


# class Controller(object):
#     # static variables.
#     __instance = None

#     @staticmethod
#     def getInstance():
#         # is instance reference None, call constructor.
#         if Controller.__instance is None:
#             Controller()
#         # return the instance
#         return Controller.__instance

#     # constructor - composition of model, view (dependency injection)
#     def __init__(self):
#         pass
#         self.usage = "Controller usage"
#         # Virtually private constructor.
#         if Controller.__instance is not None:
#             raise Exception("Controller is a singleton.")
#         else:
#             Controller.__instance = self

#     def runProgram(self, arguments):
#         # get instance of model.
#         model: Model = Model.getInstance()

#         # get result of setting up model, either True or String
#         result = model.setup(arguments)

#         # attach methods to run later after threads for generating mazes is finish
#         model.attach(model.solveMazes) # attach solving mazes to observer pattern
#         model.attach(model.showGraphs) # attach method for show plotting to observer pattern
#         if model.outputfile is not None: # attach method for write mazes to file
#             model.attach(model.writeFile)

#         if(result is True):
#             # Read from file
#             if model.inputfile is not None:
#                 model.detach(model.observers[0]) # detach methods for solve mazes from observer pattern - run directly in model
#                 model.readFile()
#             # Generate mazes
#             if model.inputfile is None:
#                 model.generateMazes()
#             # Write mazes to file
#             #if model.outputfile is not None:
#             #    model.attach(model.writeFile)
#         else:
#             print(result)
#             exit(1)

# if __name__ == '__main__':
#     c = Controller.getInstance()
#     c.runProgram(sys.argv[1:])