import csv
from Maze import Maze


class csvFileReader:

    # static sizes no like.
    # sizes: list = list()

    def __init__(self):
        pass

    #Returnere listen over sizes fra csv-filen som er øverste linie i filen
    def getSizes(self):
        return self.sizes

    #Indlæser den valgte/indtastede csv-fil
    def read(self, fileName):
        #Seperator mellem samme størrelse, men en ny maze af samme størrelse - på denne måde ved vi at en maze er færdig en ny starter
        seperator = ['#']
        #Seperator som adskiller størrelserne af mazes fra hinanden - f.eks. har man 10 af samme maze med størrelser 5 og 10 - vil denne seperator stå efter alle med størrelse 5 for
        #at markere at ny begynder en ny størrelse mazes - altså størrelsen 10 i eksemplet ovenfor.
        seperatorNewSize = ['EndOfMazeSize']
        #Laver en tom og klar liste til alle mazes for en given størrelse - dette vil altså være en 2 dimensionelt fordi dette vil indeholde 10 lister af hver størrelse
        #Ligesom en liste af mazes i "Model" (self.mazes) ville se ud hvis man havde indtastet mazes uden filer og genererede dem efterfølgende.
        mazesAllSizes = []
        #Laver en tom liste klar som holder den enkelte maze indtil man når en '#'-seperator.
        mazesSingleSize = []

        with open(fileName) as f:
            #Laver en tom liste som senere skal bruges til de sizes som er angivet i den fil der bliver indlæst
            self.sizes = list()  # holds read in sizes from file.

            #Tæller til brug ved index placering i listen "self.sizes" ovenfor - dette bruges til Maze objektet længere nede
            a = 0
            #Åbner CSV-filen og splitter den på ,
            reader = csv.reader(f, delimiter=',')
            #Laver en tom liste som skal indeholde hver række af en mazes fra den indlæste CSV-fil - hver række af lister lægges ind i denne maze indtil der mødes en seperator
            maze = []
            #Løber alle række igennem fra den indlæste CSV-fil
            for row in reader:
                #Vi tjekker på om der er indhold i listen "self.sizes", det er der ikke ved første iteration - og derfor hopper den ned i "else"
                if len(self.sizes) != 0:
                    #Tjekker om indholdet af row er lig med "seperator"-variablen ovenfor - hvilket betyder at mazen er færdig og en ny maze på samme størrelse kommer
                    if row == seperator:
                        #Laver et objekt af Maze med elementet fra "self.sizes" index placering = værdien af a samt en kopi af listen fra maze
                        #Dette giver Maze-objektet variablerne size og convertedMaze
                        #Vi laver en kopi for at skabe en unik version af maze listen, som vi ellers "clear" længere nede
                        objMaze = Maze(self.sizes[a], maze.copy())
                        #Når ovenstående objekt er lavet lægger vi det i en liste af alle mazes med samme størrelse, således vi en liste med f.eks. 10 Maze objekter
                        mazesSingleSize.append(objMaze)
                        #Vi clear maze listen således denne er klar til at blive brugt igen som tom liste til en ny maze som starter efter seperatoren
                        maze.clear()
                    #Tjekker om indholdet af row er lig med "seperatorNewsize"-variablen ovenfor
                    elif row == seperatorNewSize:
                        #Tilføjer listen fra de enkelte størrelser "mazeSingleSize" til den samlede liste over mazes "mazesAllSizes"
                        #Dette gør at "mazesAllSizes" indeholder x antal lister med hver 10 Maze objekter - altså er denne lige med hoved-listen, som har en række
                        #sublister med Maze objekter i
                        #Vi laver en kopi for at skabe en unik version af "mazeSingleSize"-listen, som vi ellers "clear" længere nede
                        mazesAllSizes.append(mazesSingleSize.copy())
                        #Vi clear "mazeSingleSize"-listen, således den er klar til næste maze
                        mazesSingleSize.clear()
                        #Variablen a tælles op med 1 fordi vi er færdig med en hel gennemlæb af en størrelse og skifter til en ny
                        #har vi f.eks. en sizes med [5,10,15] skal vi flytte index placeringen + 1 for at vise at mazen har en ny size
                        a += 1
                    #Tjekker om indholdet af row IKKE er lig med hverken "seperator"-variablen eller "seperatorNewSize" ovenfor
                    else:
                        #Gennemløber rækken og konvertere elementerne til Int
                        for i in range(0, len(row)):
                            row[i] = int(row[i])
                        #Row med elementerne lægges i listen maze, som dermed bliver den indlæste maze fra CSV-filen række eftil den møder en "seperator"
                        maze.append(row)
                #Hvis listen "self.sizes" er tom køres denne else kommando
                else:
                    #Gennemløber hvert element i "row" og appender til listen "self.sizes" - dette gøres med range syntaxen, hvor hvert element b converteres til Int og tilføjes listen
                    #"self.sizes" med "append"-syntaxen
                    #Eksempel:
                    #5,10,15,20,25,30 - er første linie i CSV-filen - denne gennemløbes og lægges i listen "self.sizes" som bliver til [5,10,15,20,25,30]
                    for b in range(0, len(row)):
                        self.sizes.append(int(row[b]))
        #Returnerer den samlede liste over alle indlæste mazes fra CSV-filen lige som i "Model" (self.mazes)
        return mazesAllSizes
