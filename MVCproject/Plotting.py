import matplotlib.pyplot as plt

class Plotting:

    def __init__(self, mazesize, timeMin, timeMax, timeAvg, iterationsMin, iterationsMax, iterationsAvg):
        self.mazesize = mazesize
        self.timeMin = timeMin
        self.timeMax = timeMax
        self.timeAvg = timeAvg
        self.iterationsMin = iterationsMin
        self.iterationsMax = iterationsMax
        self.iterationsAvg = iterationsAvg

    def plotting(self):
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

        iterations.plot(x, self.iterationsMin, color='red', label='Minimum Iterations')
        iterations.plot(x, self.iterationsMax, color='green', label='Maximum Iterations')
        iterations.plot(x, self.iterationsAvg, color='orange', label='Average Iterations')
        iterations.set_title("Maze solution iterations")
        plt.sca(size)
        plt.xticks(range(len(self.mazesize)), self.mazesize)
        iterations.set_xlabel("Maze size")
        iterations.set_ylabel("Iterations")
        iterations.legend(loc='best')

        mng = plt.get_current_fig_manager()
        mng.window.showMaximized()

        plt.show()

    #def plottingTime(self):
        #plt.figure()
        #plt.title("Maze solution time", fontsize=24)
        #plt.xlabel("Maze size", fontsize=14)
        #plt.ylabel("Time (ms)", fontsize=14)
        #plt.plot(self.mazesize, self.timeMin, color='red', label='Minimum Time')
        #plt.plot(self.mazesize, self.timeMax, color='green', label='Maximum Time')
        #plt.plot(self.mazesize, self.timeAvg, color='orange', label='Average Time')
        #plt.legend(loc='best')
        #plt.show()

    #def plottingIterations(self):
        #plt.figure()
        #plt.title("Maze solution iterations", fontsize=24)
        #plt.xlabel("Maze size", fontsize=14)
        #plt.ylabel("Iterations", fontsize=14)
        #plt.plot(self.mazesize, self.iterationsMin, color='red', label='Minimum Iterations')
        #plt.plot(self.mazesize, self.iterationsMax, color='green', label='Maximum Iterations')
        #plt.plot(self.mazesize, self.iterationsAvg, color='orange', label='Average Iterations')
        #plt.legend(loc='best')
        #plt.show()