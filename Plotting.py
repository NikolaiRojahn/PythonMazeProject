import matplotlib.pyplot as plt
import matplotlib as mpl

# import multiprocessing


class Plotting:
    def __init__(self, plottingDict):
        self.mazesize = plottingDict["sizes"]
        self.timeMin = plottingDict["minTime"]
        self.timeMax = plottingDict["maxTime"]
        self.timeAvg = plottingDict["avgTime"]
        self.iterationsMin = plottingDict["minIterations"]
        self.iterationsMax = plottingDict["maxIterations"]
        self.iterationsAvg = plottingDict["avgIterations"]

    def plotting(self, gui: bool = False) -> mpl.pyplot.Figure:
        """ Creates a mpl.pyplot.Figure based on plottingDict values and returns it.
            The method also sets up rendering backend on matplotlib if we use tkinter gui.
        """
        # def plottingGUI(self):
        if gui:  # use tKinter as rendering backend if we use a Tkinter GUI.
            mpl.use('TkAgg')

        x = list(range(len(self.mazesize)))

        fig, (size, iterations) = plt.subplots(1, 2)

        size.plot(x, self.timeMin, color='red', label='Minimum Time')
        size.plot(x, self.timeMax, color='green', label='Maximum Time')
        size.plot(x, self.timeAvg, color='orange', label='Average Time')
        size.set_title("Maze solution time")
        plt.sca(size)
        plt.xticks(range(len(self.mazesize)), self.mazesize)
        size.set_xlabel("Maze size")
        size.set_ylabel("Time (ms)")
        size.legend(loc='best')

        iterations.plot(x, self.iterationsMin, color='red',
                        label='Minimum Iterations')
        iterations.plot(x, self.iterationsMax, color='green',
                        label='Maximum Iterations')
        iterations.plot(x, self.iterationsAvg, color='orange',
                        label='Average Iterations')
        iterations.set_title("Maze solution iterations")
        plt.sca(iterations)
        plt.xticks(range(len(self.mazesize)), self.mazesize)
        iterations.set_xlabel("Maze size")
        iterations.set_ylabel("Iterations")
        iterations.legend(loc='best')

        # mng = plt.get_current_fig_manager()

        # mng.window.showMaximized()

        # plt.show()
        return fig

    def showGraphs(self):
        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()
        plt.show()
