import matplotlib
from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import showerror
from Interfaces import IView
import Exceptions


class GUI(IView):
    _state = ""
    _data = ""

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        #print("state going from " + self.state + " to " + value)
        self._state = value

    def __init__(self):
        self.observers = list()
        self.tk_widget = None

    def start(self):
        self.initTemplate()

    # IView methods
    def getData(self):
        return self._data

    def getState(self):
        return self.state

    def attach(self, observer):

        # print(hex(id(self.observers)))
        # print(len(self.observers))
        self.observers.append(observer)
        # print(len(self.observers))

    def notify(self):

        #print("Notifying " + str(len(self.observers)) + " observers")
        for observer in self.observers:
            # Q&D this view just prints result of observer update if no exception is thrown.
            # try:
            text, obj = observer.update()

            if (self.state == IView.SHOW_GRAPHS):
                if self.tk_widget is not None:
                    self.tk_widget.pack_forget()
                self.canvas = FigureCanvasTkAgg(obj, master=self.labelFrame2)
                self.tk_widget = self.canvas.get_tk_widget()
                self.canvas.draw()
                self.tk_widget.pack(side=TOP, fill=BOTH, expand=1)

            self.statusBar['text'] = text

            # except Exceptions.UserFriendlyException as e:
            #    self.errorMsg = str(e)
            #    self.handleErrorMessage()

    # Method which updates the current chosen algorithm.

    def updateChosenAlgorithm(self, value):
        self.chosenAlgorithm = value

    # Method which is called when RUN button is clicked.
    def runProgram(self):
        try:
            if(self.checkForWrongInput()):
                self.setFileName()

                # Handle _state and _data in order for the backend to fetch.
                self._data = self.inputSizes.get()
                self.state = self.ADD_MAZE_SIZE
                self.notify()

                self.state = self.GENERATE_MAZES
                self.notify()

                self._data = self.filename
                self.state = self.chosenFileJob
                self.notify()

                self._data = self.chosenAlgorithm
                self.state = self.SELECT_ALGORITHM
                self.notify()

                self.state = self.SOLVE_MAZES
                self.notify()
            else:
                print("One or more fields are missing input!")
        except BaseException as e:
            print("Catched BaseException in RunProgram method")
            self.errorMsg = str(e)
            self.handleErrorMessage()

    # Calls backend to create graphs.

    def getPlotting(self):
        print("Requested plotting")
        try:
            self.state = self.SHOW_GRAPHS
            self.notify()
        except Exception as e:
            self.errorMsg = e
            self.handleErrorMessage()

    # Checks the selected option for filejob, and sets the variable chosenFileJob with the syntax the backend needs.
    def handleFileInput(self, value):
        if(value == "write"):
            self.chosenFileJob = "writeToFile"
            self.createFilenameInputField()

        else:
            self.chosenFileJob = "readFromFile"
            self.createFilenameInputField()

    # Checks if any of the input field or option menu's has wrong input.
    def checkForWrongInput(self):
        if(self.inputSizes.get() is not "" and self.selectedFileJob.get() is not "read"):
            return True
        if(self.selectedFileJob is "read" and self.inputSizes.get() is ""):
            return True
        return False

    def setFileName(self):
        self.filename = self.inputFilename.get()

    def createFilenameInputField(self):
        # Create input field for filename
        self.labelFilename = Label(self.labelFrame1, text="Filename")
        self.labelFilename.grid(row=8, column=1)
        self.inputFilename = Entry(self.labelFrame1)
        self.inputFilename.grid(row=9, column=1)

    # Returns the value depending on the filejob
    def handleFileResult(self):
        if(self.chosenFileJob == "writeToFile"):
            return "-o"
        else:
            return "-i"

    def handleErrorMessage(self):
        showerror(title="Error", message=self.errorMsg)

    def initTemplate(self):
        padx = 10
        pady = 10
        self.master = Tk()
        self.master.geometry('500x500')
        self.master.title("MAZE APPLICATION")
        self.algorithms = ['dfs']
        self.selectedFileJob = StringVar()
        self.selectedFileJob.set("")
        self.selectedAlgorithm = StringVar()
        self.selectedAlgorithm.set(self.algorithms[0])
        self.chosenAlgorithm = "dfs"
        self.chosenFileJob = ""
        self.filename = ""
        self.sizes = ""
        self.errorMsg = "Dette er en fejl som er predefineret"

        filehandling = ['write', 'read']

        # Create a status bar.
        self.statusBar = Label(
            self.master, text="Ready to work...", bd=1, relief=SUNKEN, anchor=W, padx=5, pady=5)
        self.statusBar.pack(side=BOTTOM, fill=X)
        # Create 2 labelled frames
        # 1 for the buttons and functions part
        # 1 for the graphs part.
        self.labelFrame2 = LabelFrame(
            self.master, text="Maze graphs", width=300, padx=padx, pady=pady)
        self.labelFrame2.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.labelFrame1 = LabelFrame(
            self.master, text="Configuration", padx=padx, pady=pady)
        self.labelFrame1.pack(expand=YES, fill=BOTH)

        # Create and display sizes label and input field.
        self.labelSizes = Label(self.labelFrame1, text="Sizes")
        self.labelSizes.grid(row=1, column=1)  # pack(side = LEFT)
        self.inputSizes = Entry(self.labelFrame1)
        self.inputSizes.grid(row=2, column=1)

        # Create and display alg. label & dropdown menu.
        self.labelAlgorithm = Label(self.labelFrame1, text="Gen. alg")
        self.labelAlgorithm.grid(row=4, column=1)
        self.popupAlgorithm = OptionMenu(
            self.labelFrame1, self.selectedAlgorithm, *self.algorithms, command=self.updateChosenAlgorithm)
        self.popupAlgorithm.grid(row=5, column=1)

        # Create option menu for filehandling.
        self.labelFileJob = Label(self.labelFrame1, text="Filehandling")
        self.labelFileJob.grid(row=6, column=1)
        self.popupFileJob = OptionMenu(
            self.labelFrame1, self.selectedFileJob, *filehandling, command=self.handleFileInput)
        self.popupFileJob.grid(row=7, column=1)

        # Create and display RUN PROGRAM button.
        self.buttonSizes = Button(
            self.labelFrame1, text="RUN PROGRAM", command=self.runProgram)
        self.buttonSizes.grid(row=10, column=1)

        # Create and display plotting button.
        self.buttonGetPlotting = Button(
            self.labelFrame2, text="Get plotting", command=self.getPlotting)
        self.buttonGetPlotting.pack(side=TOP)

        # #Create and display message box.
        # self.labelMessageBox = Label(self.master, text="Message box")
        # self.labelMessageBox.grid(row=2, column=3)
        # self.entryMessage = Entry(self.master, state=DISABLED, size=)
        # self.entryMessage.grid(row=3, column=3)

        # self.buttonTestError = Button(self.master, text="Test Exception", command=self.handleErrorMessage)
        # self.buttonTestError.grid(row=10, column=4)
        self.master.mainloop()
