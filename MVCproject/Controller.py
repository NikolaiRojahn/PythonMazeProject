from Maze import Maze
from Counter import Counter
from Timer import Timer
from TimerTotal import TimerTotal
from Solve import Solve
from Calculator import Calculator

if __name__ == '__main__':
    i = 1
    size = 5
    runLoop = 10
    timerTotal = TimerTotal()
    while i < runLoop:
        maze = Maze(size)
        timer = Timer()
        counter = Counter()
        solve = Solve(maze, counter)

        print(maze.pretty_print())
        timer.StartTimer()
        solve.search(1, 1)
        print(counter.GetNumberOfPointsVisitedWithText())
        timer.EndTimer()
        print(timer.GetTimerWithText())
        timerTotal.setTotalTimer(timer.GetTimer())
        i += 1
    calculator = Calculator(timerTotal.GetTimer(), runLoop)
    print(calculator.GetTimerAverage())