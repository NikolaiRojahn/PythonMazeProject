import time

class Timer:
    #Opsætter 3 tomme variabler i konstruktøren til senere brug med tid
    def __init__(self):
        self.timerStart = None
        self.timerEnd = None
        self.timerRuntime = None

    #Sætter en tid i variablen til den nuværende tid "timerStart" fra time-modulet "import time" i toppen
    def StartTimer(self):
        self.timerStart = time.clock()

    #Sætter en tid i variablen til den nuværende tid "timerEnd" fra time-modulet "import time" i toppen
    #Beregner i variablen "timerRuntime" den aktuelt brugte tid mellem start og slut tiden
    def EndTimer(self):
        self.timerEnd = time.clock()
        self.timerRuntime = self.timerEnd - self.timerStart

    #Returnere den beregnede tid i faktuelle millisekunder (millisekunder * 1000) for at bruge det i plotningsaksen til tiderne
    #Eksempel:
    #0.0008185000000011655 som er den faktuelle tid ved beregning mellem start og end
    #0.8185000000011655 som er den returnerede værdi fordi der ganges op med 1000 for at få det faktuelle tal i millisekunder
    #Altså i plotting hvor der står "Time (ms)" vises 0.8 og ikke 0.0008
    def GetTimer(self):
        return self.timerRuntime * 1000