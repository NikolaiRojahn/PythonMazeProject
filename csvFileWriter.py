import csv
import platform
from Maze import Maze


class csvFileWriter:

    def write(self, mazeArray, fileName, sizes):
        file_obj = open(fileName, "w", newline='')
        #Laver en instans af CSV-writer på fil objektet fra ovenfor
        output_writer = csv.writer(file_obj)
        #Giver mulighed for at bruge "writerow"-syntaxen til at skrive til CSv-filen i liste for [.....]
        #Her indskrives f.eks. listen "sizes" i første linie af CSv-filen, men vel og mærke uden [] liste syntaxen i selve CSV-filen
        #EKSEMPEL:
        #[1,2,3] bliver til '1','2','3'
        output_writer.writerow(sizes)
        #Gennemløber alle sublisterne i "mazeArray", som får "self.mazes" fra "Model" som input - altså en liste som indeholder sublister med Maze-objekter
        for sizeOfMaze in list(mazeArray):
            #Gennemløber sublisten af ovenstående "mazeArray" for Maze-objekter
            for maze in list(sizeOfMaze):
                #Gennemløber hver række i listen "convertedMaze" på den pågældende Maze-objekt element
                #Dette giver mulighed for at skrive direkte til CSv-filen som ovenfor med "sizes"
                #Altså fordi mazes ligger med [....] i "convertedMaze" listen
                for row in maze.convertedMaze:
                    #Som ovenfor fortalt kan vi direkte til CSV-filen skrive hver række i listen ud, da en "convertedMaze" er en liste med flere sublister i sig
                    #for at danne en maze som den ser ud hvis man ser den udskrevet - disse lister skrive enkeltvis til CSV-filen her
                    output_writer.writerow(row)
                #Efter hver et Maze-objekt med "convertedMaze" indsættes nedenstående som seperator, dette for at indikere at en maze er færdigskrevet til CSV-filen,
                #men at der kommer flere med samme size, altså vil den skrives 10 gange når mn laver 10 af hver size af mazes
                output_writer.writerow(['#'])
            #Denne seperator indsættes når en hel gennemløb af en size er færdig, denne indikere at alle mazes for en given størrelse er skrevet til filen, og at der ny kommer en mazes
            #med en ny størrelse - f.eks. ved skift fra 5 til 10 i en size-liste [5,10,15]
            output_writer.writerow(['EndOfMazeSize'])
