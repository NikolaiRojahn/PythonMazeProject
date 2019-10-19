from Maze import Maze
from Counter import Counter
from Timer import Timer
from TimerTotal import TimerTotal
from Solve import Solve
from Calculator import Calculator

if __name__ == '__main__':
    sizes = [5, 10, 15, 20, 25, 30]
    runLoop = 2

    for size in sizes:
        print(15 * "*" + str(size) + 15*"*")
        timerTotal = TimerTotal()
        i = 0
        while i < runLoop:
            maze = Maze(size)
            timer = Timer()
            counter = Counter()
            solve = Solve(maze, counter)

            print(maze.pretty_print())
            timer.StartTimer()
            # pass in True as last argument to see print outs from search(...)
            solve.search(1, 1)
            print(counter.GetNumberOfPointsVisitedWithText())
            timer.EndTimer()
            print(timer.GetTimerWithText())
            timerTotal.setTotalTimer(timer.GetTimer())
            i += 1
        calculator = Calculator(timerTotal.GetTimer(), runLoop)
        print(calculator.GetTimerAverage())
