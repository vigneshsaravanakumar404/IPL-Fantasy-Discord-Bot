class Player:

    def __init__(self, team: str, name: str, runs: int, sr: float, fours: int, sixes: int, zeroDismisals: int, fifties: int, centuries: int, notOuts: int, isBowler: bool, ballsFaced: int, wickets: int, fourplus: int, fiveplus: int, sixplus: int, maidens: int, hattrick: int, economy: float, oversBowled: int, dotBalls: int, isVC: bool, isC: bool, catches: int, stumpings: int) -> None:
        
        # Initial Variables
        self.team = team
        self.name = name
        self.isVC = isVC
        self.isC = isC
        self.catches = catches
        self.stumpings = stumpings

        self.runs = runs
        self.sr = sr
        self.fours = fours
        self.sixes = sixes
        self.zeroDismisals = zeroDismisals
        self.fifties = fifties
        self.centuries = centuries
        self.notOuts = notOuts
        self.isBowler = isBowler
        self.ballsFaced = ballsFaced
        self.total = 0

        self.wickets = wickets
        self.fourplus = fourplus
        self.fiveplus = fiveplus
        self.sixplus = sixplus
        self.maidens = maidens
        self.hattrick = hattrick
        self.economy = economy
        self.oversBowled = oversBowled
        self.dotBalls = dotBalls
        
        
        # Calculate Points
        self.calculate_batting_points()
        self.calculate_bowling_points()
        self.total += self.catches * 25
        self.total += self.stumpings * 50

        # If the player is a VC or C, multiply the points
        if self.isVC == True:
                self.total *= 1.5
        elif self.isC == True:
            self.total *= 2

    def calculate_batting_points(self):
        
        # Yellow
        yellow = 0
        yellow += self.runs * 2 # 2 points per run
        yellow += self.fours * 4 # 4 point per 4
        yellow += self.sixes * 8 # 8 points per 6
        yellow -= self.zeroDismisals * 6 # -6 points per 0 dismissal
        yellow += self.fifties * 50 # 50 points per 50
        yellow += int(self.centuries) * 100 # 100 points per 100
        
        # Green
        green = 0
        if self.ballsFaced > 15:
            if self.sr > 200.00:
                green += 1000
            elif 175.00 <= self.sr <= 200.00:
                green += 800
            elif 150.00 <= self.sr < 175.00:
                green += 600
            elif 125.00 <= self.sr < 150.00:
                green += 400
            elif 100.00 <= self.sr < 125.00:
                green += 200
            elif 75.00 <= self.sr < 100.00:
                green -= 100
            elif 50.00 <= self.sr < 75.00:
                green -= 200
            elif 25.00 <= self.sr < 50.00:
                green -= 300
            else:
                green -= 500

        # Cyan
        cyan = 0
        if self.ballsFaced > 15:
            if self.sr > 850:
                cyan += 5000
            elif self.sr > 800:
                cyan += 4500
            elif self.sr > 750:
                cyan += 4000
            elif self.sr > 700:
                cyan += 3500
            elif self.sr > 650:
                cyan += 3000
            elif self.sr > 600:
                cyan += 2500
            elif self.sr > 550:
                cyan += 2000
            elif self.sr > 500:
                cyan += 1500
            elif self.sr > 450:
                cyan += 1000
            elif self.sr > 400:
                cyan += 750
            elif self.sr > 350:
                cyan += 500
            elif self.sr > 300:
                cyan += 250

        # If the player is a bowler, double the points
        if self.isBowler == True: 
            cyan *= 2
            green *= 2
            yellow *= 2
            
        # Total
        self.total = yellow + green + cyan

        """ Calculations for MAXES are done else where"""

    def calculate_bowling_points(self):
            
        # Yellow
        yellow = 0
        yellow += self.wickets * 50 # 50 points per wicket
        yellow += self.dotBalls * 5 # 5 points per dot ball
        yellow += self.fourplus * 250 # 250 points per 4 wickets
        yellow += self.fiveplus * 500 # 500 points per 5 wickets
        yellow += self.sixplus * 1000 # 1000 points per 6 wickets
        yellow += self.maidens * 150 # 150 points per maiden
        yellow += self.hattrick * 750 # 750 points per hattrick
        
        # Green
        green = 0
        if self.wickets > 35:
            green += 5000
        elif self.wickets > 30:
            green += 4000
        elif self.wickets > 25:
            green += 3000
        elif self.wickets > 20:
            green += 2000
        elif self.wickets > 15:
            green += 1000

        # Purple
        purple = 0
        if self.oversBowled > 5:
            if self.economy > 11:
                purple -= 500
            elif self.economy > 10:
                purple -= 400
            elif self.economy > 9:
                purple -= 200
            elif self.economy > 8:
                purple -= 100
            elif self.economy > 6:
                purple += 100
            elif self.economy > 5:
                purple += 250
            elif self.economy > 4:
                purple += 500
            elif self.economy > 3:
                purple += 800
            elif self.economy > 2:
                purple += 1200
            elif self.economy > 1:
                purple += 1500
            else:
                purple += 2000

        # If the player is a batsman, double the points
        if self.isBowler == False: 
            green *= 2
            yellow *= 2
            purple *= 2

        # Total
        self.total += yellow + green + purple

    # Getter Methods for MAX calculations 
    def getAverage(self):
        return self.runs / self.ballsFaced

    def getStrikeRate(self):
        return (self.runs / self.ballsFaced) * 100

    def getScore(self):
        return self.runs
    
    def get4s(self):
        return self.fours

    def get6s(self):
        return self.sixes

    def get50s(self):
        return self.fifties

    def get100s(self):
        return self.centuries

    def get0s(self):
        return self.zeroDismisals

    def getNOs(self):
        return self.notOuts
    
    def getMaidens(self):
        return self.maidens

    def getWickets(self):
        return self.wickets
    
    def getEconomy(self):
        return self.economy
    
    def getfourplus(self):
        return self.fourplus

    def getfiveplus(self):
        return self.fiveplus
    
    def getsixplus(self):
        return self.sixplus
    
    def getHattrick(self):
        return self.hattrick

    def getOversBowled(self):   
        return self.oversBowled
    
    def getDotBalls(self):
        return None
    
    def allMaxes(self):
        return [self.getAverage(), self.getStrikeRate(), self.getScore(), self.get4s(), self.get6s(), self.get50s(), self.get100s(), self.get0s(), self.getNOs(), self.getMaidens(), self.getWickets(), self.getEconomy(), self.getfourplus(), self.getfiveplus(), self.getsixplus(), self.getHattrick(), self.getOversBowled(), self.getDotBalls()]

    def __str__(self) -> str:
        return f"{self.name} from {self.team}"