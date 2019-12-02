import Exceptions
from Interfaces import IView


class View(IView):

    def __init__(self):
        self.observers = list()
        self.choiceSelected = None
        self._state = "stateStr"
        self._data = "dataStr"

        self.choices = {
            # each entry in the map has a string for the
            # menu and a method to call upon selection.
            0: ("Exit Program", lambda: {}),  # do nothing
            1: ("Select algorithm", self.selectAlgorithm),
            2: ("Read from file", self.readFromFile),
            3: ("Write to file", self.writeToFile),
            4: ("Add maze size(s)", self.addMazeSizes),
            5: ("Show maze size(s)", self.showMazeSizes),
            6: ("Clear maze size(s)", self.clearMazeSizes),
            7: ("Generate mazes", self.generateMazes),
            8: ("Solve mazes", self.solveMazes),
            9: ("Show graphs", self.showGraphs)
        }

    @property
    def state(self):
        return self._state

    @property
    def data(self):
        return self._data

    def attach(self, observer):
        self.observers.append(observer)

    def getState(self) -> str:
        return self.state

    def getData(self):
        return self.data

    def selectAlgorithm(self):
        # prompt for algorithm.
        self._data = input(
            "Type algorithm code: ")
        self._state = View.SELECT_ALGORITHM

        self.notify()

    def readFromFile(self):
        # prompt for filename.
        self._data = input("Type filename: ")
        self._state = View.READ_FROM_FILE
        self.notify()

    def writeToFile(self):
        self._data = input("Type filename: ")
        self._state = View.WRITE_TO_FILE
        self.notify()

    def addMazeSizes(self):
        self._data = input("Type maze sizes separated with commas: ")
        self._state = View.ADD_MAZE_SIZE
        self.notify()

    def showMazeSizes(self):
        self._data = ""
        self._state = View.SHOW_MAZE_SIZES
        self.notify()

    def clearMazeSizes(self):
        self._data = ""
        self._state = View.CLEAR_MAZE_SIZES
        self.notify()

    def generateMazes(self):
        self._state = View.GENERATE_MAZES
        self.notify()

    def solveMazes(self):
        self._state = View.SOLVE_MAZES
        self.notify()

    def showGraphs(self):
        self._state = View.SHOW_GRAPHS
        self.notify()

    def notify(self):
        for observer in self.observers:
            # Q&D this view just prints result of observer update if no exception is thrown.
            try:
                print(observer.update())
            except Exceptions.UserFriendlyException as e:
                print(str(e))

    def start(self):
        """ Prints a menu of strings in self.choices, reads user input and stores it in self.selection. """
        while(self.choiceSelected != 0):
            if self.choiceSelected is not None:
                if len(self.choices) > self.choiceSelected >= 0:
                    pass
                else:
                    print("Invalid choice, try again!")
            print("-----")
            print("MENU:")
            print("-----")

            # use list comprehension to build menulist of choices without choice 0:
            # This will actually build us a list of ints coming from self.choices.
            menulist = [choice for choice in self.choices if choice != 0]
            # append first choice last.
            menulist.append(0)

            for c in menulist:
                item = self.choices.get(c)
                print(str(c) + ". " + str(item[0]))
            # read input as string
            selection = input(
                "Your choice (1-{max} or 0): ".format(max=len(self.choices)-1))
            # convert input to int if possible.
            try:
                self.choiceSelected = int(selection)
                # call the method selected.
                choice = self.choices.get(self.choiceSelected)
                if choice is not None:
                    choice[1]()

            except ValueError:
                self.choiceSelected = None

    def test(self):
        pass


if __name__ == '__main__':
    # print(sys.argv[1:])
    view = View()

    print(view.state)
    print(view.data)

    view.start()
