import matplotlib.pyplot as plt
import matplotlib as mpl

# import multiprocessing


class Plotting:
    def __init__(self, plottingDict):
        #Modtager et dictionary fra "Model" med værdierne klar til plotting
        self.mazesize = plottingDict["sizes"]
        self.timeMin = plottingDict["minTime"]
        self.timeMax = plottingDict["maxTime"]
        self.timeAvg = plottingDict["avgTime"]
        self.iterationsMin = plottingDict["minIterations"]
        self.iterationsMax = plottingDict["maxIterations"]
        self.iterationsAvg = plottingDict["avgIterations"]

    def plotting(self, gui: bool = False) -> mpl.pyplot:
        """ Creates a mpl.pyplot.Figure based on plottingDict values and returns a referece to matplotlib.pyplot.
            The method also sets up rendering backend on matplotlib if we use tkinter gui (pass true for gui)
        """
        # def plottingGUI(self):
        if gui:  # use tKinter as rendering backend if we use a Tkinter GUI.
            mpl.use('TkAgg')

        #x laves til en liste med nummeriske værdier ud fra længden af størrelser - altså hvor mange størrelser der er indtastet/indlæst fra filen
        x = list(range(len(self.mazesize)))

        #Danner et subplot - altså 2 plotting vinduer i samme billede
        #Det er angivet i paratesen at det skal være 1 række med 2 elementer (1, 2)
        _, (size, iterations) = plt.subplots(1, 2)

        #OBS!! Kommentarer til nedenstående blok af kode gælder også for "iterations" - det er samme struktur bare med andet subplot navn
        #Nedenstående 3 "plot" danner en linie på hver værdi som er angivet i listen ved at starte på første index og videre til næste indtil alle værdier løbet igennem og linie er dannet
        #x er ovenstående liste og viser hvor den pågældende værdi fra listen skal indsættes - color er farven på linie - label er teksten som bruges til at vise i tekstboksen
        size.plot(x, self.timeMin, color='red', label='Minimum Time')
        size.plot(x, self.timeMax, color='green', label='Maximum Time')
        size.plot(x, self.timeAvg, color='orange', label='Average Time')
        #Sætter en title/overskrift
        size.set_title("Maze solution time")
        #Nedenstående "sca"-metode sætter fokus på hvilket plotting man skal bruge til nedenstående "xticks"-metode
        plt.sca(size)
        #Nedenstående "xticks"-metode viser de specifikke værdier som er angivet - altså har den en låste med nummeriske værdier, men disse tages så fra andet parameter "self.mazesize"
        #og dermed vises de præcise værdier som er angivet på x
        plt.xticks(range(len(self.mazesize)), self.mazesize)
        #Nedenstående "set_xlabel" og "set_ylabel"-metode er en tekst på hver akse som viser hvad som er hvad
        size.set_xlabel("Maze size")
        size.set_ylabel("Time (ms)")
        #Nedenstående "legend"-metode viser tekstboksen til forklaring af farverne på linierne og den label tekst der er på hver af dem
        #"loc='best'" gør at den finder det bedste sted selv at placere boksen ud fra hvordan linierne er tegnet.
        size.legend(loc='best')

        #OBS!!! SAMME SOM OVENFOR MED "SIZE"
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

        #Returnerer selve figuren som er lavet i "plt"
        return plt

    def showGraphs(self, plt):
        """Shows graphs in external window invoked by the matplotlib.pyplot instance passed in."""
        #Tager en tegnet plotning - ovenstående metode - ind som parameter og finder den "Figure Manager"
        mng = plt.get_current_fig_manager()
        #Nedenstående gør at det er muligt ved hjælp af ovenstående "Figure Manager" at vise billedet af plotning i maximeret størrelse
        mng.window.showMaximized()
        #Nedenstående viser selve den tegnede plotning fra input parameter "plt"
        plt.show()
