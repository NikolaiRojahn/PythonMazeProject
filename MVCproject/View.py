class View(object):

    def __init__(self):
        self.observers = list()
        self.choiceSelected = None
        self._state = "stateStr"
        self._data = "dataStr"
        # String "constants" for view's state, can be reassigned, just don't do it!
        # dictionary
        self.SELECT_ALGORITHM = "selectAlgorithm"
        self.READ_FROM_FILE = "readFromFile"
        self.WRITE_TO_FILE = "writeToFile"
        self.ADD_MAZE_SIZE = "addMazeSize"
        self.SHOW_MAZE_SIZES = "showMazeSizes"
        self.CLEAR_MAZE_SIZES = "clearMazeSizes"
        self.GENERATE_MAZES = "generateMazes"
        self.SOLVE_MAZES = "solveMazes"
        self.SHOW_GRAPHS = "showGraphs"

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

    def selectAlgorithm(self):
        # prompt for algorithm.
        self._data = input(
            "Type algorithm code: ")
        self._state = self.SELECT_ALGORITHM

        self.notify()

    def readFromFile(self):
        # prompt for filename.
        self._data = input("Type filename: ")
        self._state = self.READ_FROM_FILE
        self.notify()

    def writeToFile(self):
        self._data = input("Type filename: ")
        self._state = self.WRITE_TO_FILE
        self.notify()

    def addMazeSizes(self):
        self._data = input("Type maze sizes separated with commas: ")
        self._state = self.ADD_MAZE_SIZE
        self.notify()

    def showMazeSizes(self):
        self._data = ""
        self._state = self.SHOW_MAZE_SIZES
        self.notify()

    def clearMazeSizes(self):
        self._data = ""
        self._state = self.CLEAR_MAZE_SIZES
        self.notify()

    def generateMazes(self):
        self._state = self.GENERATE_MAZES
        self.notify()

    def solveMazes(self):
        self._state = self.SOLVE_MAZES
        self.notify()

    def showGraphs(self):
        self._state = self.SHOW_GRAPHS
        self.notify()

    def notify(self):
        for observer in self.observers:
            # Q&D just print result of observer.update - we might have more observers in this pattern but not here.
            print(observer.update())

    def menu(self):
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

    view.menu()
