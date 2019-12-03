from tkinter import *
from Interfaces import IView as view
import Exceptions

class GUI(view):
    observers = list()
    chosenAlgorithm = "dfs"
    chosenFileJob = ""
    filename = ""
    variables = {}
    sizes = []
    _state = ""
    _data = ""

    def __init__(self, master):
        self.initTemplate(master)

    #IView methods
    def getData(self):
        return self._data
    
    def getState(self):
        return self._state

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self):
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
            self.handleSizesInput()
            self.setFileName()

            #Handle _state and _data in order for the backend to fetch.
            self._data = self.sizes
            self._state = self.ADD_MAZE_SIZE
            self.notify()
            
            self._data = self.chosenAlgorithm
            self._state = self.SELECT_ALGORITHM
            self.notify()

            self._data = self.filename
            self._state = self.chosenFileJob
            self.notify()

            self._state = self.GENERATE_MAZES
            self.notify()
            self._state = self.SOLVE_MAZES
            self.notify()




            #self.variables["sizes"] = self.sizes
            #self.variables[self.chosenFileJob] = self.handleFileResult()
            #self.variables["filename"] = self.filename
            #self.variables["alg"] = self.chosenAlgorithm
            #print(self.variables)
        else:
            print("One or more fields are missing input!")


    #Calls backend to open up plotting window.
    def getPlotting(self):
        print("Requested plotting")
        #Somehow calls backend with a reference to the plotting recently created.


    #Seperate sizes (split, trim) and convert these to integers which will be stored in sizes array.
    def handleSizesInput(self) -> []:
        arraySizes = self.inputSizes.get().split(",")
        for i in range(0, len(arraySizes)): 
            arraySizes[i] = int(arraySizes[i].strip()) 
        self.sizes = arraySizes


    #Checks the selected option for filejob, and sets the variable chosenFileJob with the syntax the backend needs.    
    def handleFileInput(self, value):
        if(value == "write"):
            self.chosenFileJob = "writeToFile"
        else:
            self.chosenFileJob = "readFromFile"

    #Checks if any of the input field or option menu's has wrong input.
    def checkForWrongInput(self): 
        if(self.inputSizes.get() is not "" and self.inputFilename.get() is not ""):
            return True
        return False


    def setFileName(self):
        self.filename = self.inputFilename.get()


    #Returns the value depending on the filejob
    def handleFileResult(self):
        if(self.chosenFileJob == "writeToFile"):
            return "-o"
        else:
            return "-i"


    def initTemplate(self, master):
        self.master = master
        master.title("MAZE APPLICATION")
        algorithms = ['dfs'] 
        selectedAlgorithm = StringVar()
        selectedAlgorithm.set(algorithms[0])

        filehandling = ['write', 'read']
        selectedFileJob = StringVar()
        selectedFileJob.set("")

        #Create and display sizes label and input field.
        self.labelSizes = Label(master, text="Sizes")
        self.labelSizes.grid(row=1, column=1) #pack(side = LEFT)
        self.inputSizes = Entry(master)
        self.inputSizes.grid(row=2, column=1)

        #Create and display alg. label & dropdown menu.
        self.labelAlgorithm = Label(master, text="Gen. alg")
        self.labelAlgorithm.grid(row=4, column=1)
        self.popupAlgorithm = OptionMenu(master, selectedAlgorithm, *algorithms, command=self.func)
        self.popupAlgorithm.grid(row=5, column=1)

        #Create option menu for filehandling.
        self.labelFileJob = Label(master, text="Filehandling")
        self.labelFileJob.grid(row=7, column=1)
        self.popupFileJob = OptionMenu(master, selectedFileJob, *filehandling, command=self.handleFileInput)
        self.popupFileJob.grid(row=8, column=1)

        #Create input field for filename
        self.labelFilename = Label(master, text="Filename")
        self.labelFilename.grid(row=7, column=2)
        self.inputFilename = Entry(master)
        self.inputFilename.grid(row=8, column=2)
        
        #Create and display RUN PROGRAM button.
        self.buttonSizes = Button(master, text="RUN PROGRAM", command=self.runProgram)
        self.buttonSizes.grid(row=10, column=2)

        #Create and display plotting button.
        self.buttonGetPlotting = Button(master, text="Get plotting", command=self.getPlotting)
        self.buttonGetPlotting.grid(row=10, column=3)


master = Tk()
my_gui = GUI(master)
master.mainloop()

