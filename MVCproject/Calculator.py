class Calculator:
     
    def __init__(self, time, amount):
        self.time = time
        self.amount = amount
    
    def CalculateTimeAverage(self):
        return self.time / self.amount

    def GetTimerAverage(self):
        return str(self.CalculateTimeAverage()) + " " + "seconds - average time!"