from Interfaces import ISolveAlgorithm
from Counter import Counter
from Timer import Timer
from Maze import Maze


class DepthFirst(ISolveAlgorithm):

    def __init__(self):
        pass

    # implement ISolveAlgorithm.
    def solve(self, convertedMaze) -> (Timer, Counter):
        """Solves a maze and counts iterations and time consumption."""
        #For hver en maze skal vi angive hvor mange steder der er besøgt (iterations) og hvor lang tid det tog (time)
        #Derfor laves nedenfor ved hver maze et objekt af "Counter" og "Timer"
        counter = Counter()
        timer = Timer()

        #Denne starter timeren
        timer.StartTimer()
        #Nendenstående metode bruger bl.a. "counter", som tilføjer en string hver gang mazes har besøgt et punkt i sin søgen på løsningen
        self.search(convertedMaze, 1, 1, counter)
        #Denne slutter timeren og beregner tiden for løsningen mellem "start" og "end"
        timer.EndTimer()
        #Her returnerer vi værdierne fra "timer" og "counter" objekterne
        return (timer, counter)

    #  method that implements depth first solving algorithm.
    def search(self, convertedMaze: list, x, y, counter: Counter, verbose=False) -> bool:
        if convertedMaze[x][y] == 2:
            if verbose:
                print("found at %d,%d" % (x, y))
            return True
        elif convertedMaze[x][y] == 1:
            if verbose:
                print('wall at %d,%d' % (x, y))
            return False
        elif convertedMaze[x][y] == 3:
            counter.AddToCounterList('visited at %d,%d' % (x, y))
            if verbose:
                print('visited at %d,%d' % (x, y))
            return False
        if verbose:
            print('visiting %d,%d' % (x, y))
        # mark as visited
        convertedMaze[x][y] = 3

        if ((x < (len(convertedMaze)-1) and self.search(convertedMaze, x+1, y, counter, verbose))
            or (y > 0 and self.search(convertedMaze, x, y-1, counter, verbose))
            or (x > 0 and self.search(convertedMaze, x-1, y, counter, verbose))
                or (y < len(convertedMaze)-1 and self.search(convertedMaze, x, y+1, counter, verbose))):
            return True
        return False
