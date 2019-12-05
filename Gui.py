from tkinter import *
from Interfaces import IView
import Exceptions

class GUI(IView):
    
    chosenAlgorithm = "dfs"
    chosenFileJob = ""
    filename = ""
    variables = {}
    sizes = ""
    _state = ""
    _data = ""

    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, value):
        print("state going from " + self.state + " to " + value)
        self._state = value
        
    
    def __init__(self):
        self.observers = list()
        
    def start(self):
        self.initTemplate()

    #IView methods
    def getData(self):
        return self._data
    
    def getState(self):
        return self.state

    def attach(self, observer):
        
        # print(hex(id(self.observers)))
        print(len(self.observers))
        self.observers.append(observer)
        print(len(self.observers))

    def notify(self):

        print("Notifying " + str(len(self.observers)) + " observers")
        for observer in self.observers:
            # Q&D this view just prints result of observer update if no exception is thrown.
            try:
                print(observer.update())
            except Exceptions.UserFriendlyException as e:
                print(str(e))


    #Method which updates the current chosen algorithm.
    def func(self, value):
        self.chosenAlgorithm = value

    #Method which is called when RUN button is clicked.
    def runProgram(self):
        if(self.checkForWrongInput()):
            self.setFileName()

            #Handle _state and _data in order for the backend to fetch.
            self._data = self.inputSizes.get()
            self.state = self.ADD_MAZE_SIZE
            self.notify()
            
            self._data = self.chosenAlgorithm
            self.state = self.SELECT_ALGORITHM
            self.notify()

            self._data = self.filename
            self.state = self.chosenFileJob
            self.notify()

            self.state = self.GENERATE_MAZES
            self.notify()
            self.state = self.SOLVE_MAZES
            self.notify()
        else:
            print("One or more fields are missing input!")


    #Calls backend to open up plotting window.
    def getPlotting(self):
        print("Requested plotting")
        self.state = self.SHOW_GRAPHS
        self.notify()
        #Somehow calls backend with a reference to the plotting recently created.


    #Checks the selected option for filejob, and sets the variable chosenFileJob with the syntax the backend needs.    
    def handleFileInput(self, value):
        if(value == "write"):
            self.chosenFileJob = "writeToFile"
            self.createFilenameInputField()

        else:
            self.chosenFileJob = "readFromFile"
            self.createFilenameInputField()

    #Checks if any of the input field or option menu's has wrong input.
    def checkForWrongInput(self): 
        if(self.inputSizes.get() is not "" and self.inputFilename.get() is not ""):
            return True
        return False


    def setFileName(self):
        self.filename = self.inputFilename.get()


    def createFilenameInputField(self):
        #Create input field for filename
        self.labelFilename = Label(self.master, text="Filename")
        self.labelFilename.grid(row=7, column=2)
        self.inputFilename = Entry(self.master)
        self.inputFilename.grid(row=8, column=2)

    #Returns the value depending on the filejob
    def handleFileResult(self):
        if(self.chosenFileJob == "writeToFile"):
            return "-o"
        else:
            return "-i"


    def initTemplate(self):
        self.master = Tk()
        self.master.title("MAZE APPLICATION")
        algorithms = ['dfs'] 
        selectedAlgorithm = StringVar()
        selectedAlgorithm.set(algorithms[0])

        filehandling = ['write', 'read']
        selectedFileJob = StringVar()
        selectedFileJob.set("")

        #Create and display sizes label and input field.
        self.labelSizes = Label(self.master, text="Sizes")
        self.labelSizes.grid(row=1, column=1) #pack(side = LEFT)
        self.inputSizes = Entry(self.master)
        self.inputSizes.grid(row=2, column=1)

        #Create and display alg. label & dropdown menu.
        self.labelAlgorithm = Label(self.master, text="Gen. alg")
        self.labelAlgorithm.grid(row=4, column=1)
        self.popupAlgorithm = OptionMenu(self.master, selectedAlgorithm, *algorithms, command=self.func)
        self.popupAlgorithm.grid(row=5, column=1)

        #Create option menu for filehandling.
        self.labelFileJob = Label(self.master, text="Filehandling")
        self.labelFileJob.grid(row=7, column=1)
        self.popupFileJob = OptionMenu(self.master, selectedFileJob, *filehandling, command=self.handleFileInput)
        self.popupFileJob.grid(row=8, column=1)
        
        #Create and display RUN PROGRAM button.
        self.buttonSizes = Button(self.master, text="RUN PROGRAM", command=self.runProgram)
        self.buttonSizes.grid(row=10, column=2)

        #Create and display plotting button.
        self.buttonGetPlotting = Button(self.master, text="Get plotting", command=self.getPlotting)
        self.buttonGetPlotting.grid(row=10, column=3)

        self.master.mainloop()


