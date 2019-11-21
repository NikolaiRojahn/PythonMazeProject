class View:
    def __init__(self):
        self.choiceSelected = None
        self.choices = {
            # each entry in the map has a string for the
            # menu and a method to call upon selection.

            0: ("Exit Program", lambda: {}),  # do nothing
            1: ("Select algorithm", self.setAlgorithm),
            2: ("Read from file", self.readFromFile),
            3: ("Write to file", self.writeToFile),
            4: ("Add maze size(s)", self.addMazeSizes),
            5: ("Solve mazes", self.solveMazes),
            6: ("Show graphs", self.showGraphs)


        }

    def setAlgorithm(self):
        print("setAlgorithm")

    def readFromFile(self):
        print("readFromFile")

    def writeToFile(self):
        pass

    def addMazeSizes(self):
        pass

    def solveMazes(self):
        pass

    def showGraphs(self):
        pass

    def menu(self):
        """ Prints a menu of strings in self.choices, reads user input and stores it in self.selection. """
        while(self.choiceSelected != 0):
            if self.choiceSelected is not None:
                if len(self.choices) > self.choiceSelected >= 0:
                    print("You chose: " +
                          self.choices.get(self.choiceSelected)[0])
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
    view.menu()
