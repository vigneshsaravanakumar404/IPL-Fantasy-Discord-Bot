from pprint import pprint
from bs4 import BeautifulSoup
from re import sub
from json import load, dump
from os import listdir
import prettytable


# Varibales
RUNS, FOURS, SIXES, DUCKS, FIFTIES, CENTURIES, SR, BATTING_AVERAGE, N, HS = (
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
)
(
    WICKETS,
    DOTS,
    FOURWICKETS,
    FIVEWICKETS,
    SIXWICKETS,
    MAIDENS,
    ECONOMY,
    BOWL_AVERAGE,
    BSR,
    OVERS,
) = ([], [], [], [], [], [], [], [], [], [])
PLAYER_LEADERBOARD_BATTING = {
    "runs": RUNS,
    "4s": FOURS,
    "6s": SIXES,
    "0s": DUCKS,
    "50s": FIFTIES,
    "100s": CENTURIES,
    "SR": SR,
    "battingAverage": BATTING_AVERAGE,
    "NOs": N,
    "HS": HS,
}
PLAYER_LEADERBOARD_BOWLING = {
    "wickets": WICKETS,
    "dots": DOTS,
    "4H": FOURWICKETS,
    "5H": FIVEWICKETS,
    "6H": SIXWICKETS,
    "maiden": MAIDENS,
    "economy": ECONOMY,
    "bowlingAverage": BOWL_AVERAGE,
    "bSR": BSR,
    "overs": OVERS,
}
PLAYER_LEADERBOARD_FIELDING = {"playerOfTheMatch": []}
SCORES = {}
EMBEDS = {}


# TODO
def computePlayerBaseStats():

    with open("Final Data/Scores.json", "r") as f:
        data = load(f)
    with open("Final Data/Players.json", "r") as f:
        conversions = load(f)

    playerPoints = {}
    for player in data:

        # Data
        points = 0
        batting = data[player]["batting"]
        bowling = data[player]["bowling"]
        playerOfMatch = data[player]["playerOfTheMatch"]

        # Batting Points
        battingPoints = 0
        battingPoints += batting["runs"] * 2
        battingPoints += batting["4s"] * 4
        battingPoints += batting["6s"] * 8
        battingPoints += batting["0s"] * -6
        battingPoints += batting["50s"] * 50
        battingPoints += batting["100s"] * 100

        if batting["BF"] >= 15:
            if batting["SR"] > 200:
                battingPoints += 1000
            elif batting["SR"] >= 175:
                battingPoints += 800
            elif batting["SR"] >= 150:
                battingPoints += 600
            elif batting["SR"] >= 125:
                battingPoints += 400
            elif batting["SR"] >= 100:
                battingPoints += 200
            elif batting["SR"] < 75:
                battingPoints -= 200
            elif batting["SR"] < 50:
                battingPoints -= 300
            elif batting["SR"] < 25:
                battingPoints -= 500
            else:
                battingPoints -= 100

            if batting["runs"] > 850:
                battingPoints += 5000
            elif batting["runs"] >= 800:
                battingPoints += 4500
            elif batting["runs"] >= 750:
                battingPoints += 4000
            elif batting["runs"] >= 700:
                battingPoints += 3500
            elif batting["runs"] >= 650:
                battingPoints += 3000
            elif batting["runs"] >= 600:
                battingPoints += 2500
            elif batting["runs"] >= 550:
                battingPoints += 2000
            elif batting["runs"] >= 500:
                battingPoints += 1500
            elif batting["runs"] >= 450:
                battingPoints += 1000
            elif batting["runs"] >= 400:
                battingPoints += 750
            elif batting["runs"] >= 350:
                battingPoints += 500
            elif batting["runs"] >= 300:
                battingPoints += 250

        # Bowling Points
        bowlingPoints = 0
        bowlingPoints += bowling["wickets"] * 50
        bowlingPoints += bowling["dots"] * 5
        bowlingPoints += bowling["4H"] * 250
        bowlingPoints += bowling["5H"] * 500
        bowlingPoints += bowling["6H"] * 1000
        bowlingPoints += bowling["maiden"] * 150

        if bowling["overs"] >= 5:
            if bowling["economy"] < 5:
                bowlingPoints += 500
            elif bowling["economy"] < 6:
                bowlingPoints += 250
            elif bowling["economy"] < 8:
                bowlingPoints += 100
            elif bowling["economy"] < 9:
                bowlingPoints -= 100
            elif bowling["economy"] < 10:
                bowlingPoints -= 200
            elif bowling["economy"] < 11:
                bowlingPoints -= 400
            else:
                bowlingPoints -= 500

        if bowling["wickets"] > 35:
            bowlingPoints += 5000
        elif bowling["wickets"] > 30:
            bowlingPoints += 4000
        elif bowling["wickets"] > 25:
            bowlingPoints += 3000
        elif bowling["wickets"] > 20:
            bowlingPoints += 2000
        elif bowling["wickets"] > 15:
            bowlingPoints += 1000

        # TODO: Position Points

        # TODO: Fielding Points
        fieldingPoints = 0
        fieldingPoints += playerOfMatch * 100

        points += battingPoints + bowlingPoints + fieldingPoints
        playerPoints[conversions[player]] = points

    playerPoints = dict(
        sorted(playerPoints.items(), key=lambda item: item[1], reverse=True)
    )
    with open("Final Data\PlayerPoints.json", "w") as f:
        dump(playerPoints, f, indent=2)


# TODO
def computeBonusStats():
    return None


# TODO
def computeTeamBaseStats():
    return None


# TODO
def computeTeamBonusStats():
    return None


def getDots():
    players = {}
    with open("Final Data/Players.json", "r") as f:
        players = load(f)
    players = {value: key for key, value in players.items()}

    with open("Data\DOTS.html", "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        table_body = soup.find("tbody")

        for row in table_body.find_all("tr"):
            row_list = []
            for cell in row.find_all("td"):
                row_list.append(
                    cell.text.strip()
                    .replace("\n", "")
                    .replace("PBKS", "")
                    .replace("DC", "")
                    .replace("CSK", "")
                    .replace("MI", "")
                    .replace("KKR", "")
                    .replace("RR", "")
                    .replace("RCB", "")
                    .replace("SRH", "")
                    .replace("GT", "")
                    .replace("LSG", "")
                    .replace("Naveen-Ul-Haq", "Naveen-ul-Haq")
                )
            if len(row_list) > 0:
                name = row_list[1].split(" ")
                name = (
                    sub(" +", " ", row_list[1])
                    .replace("M Siddharth", "Manimaran Siddharth")
                    .replace("Sai Kishore", "Ravisrinivasan Sai Kishore")
                    .replace("Vyshak Vijaykumar", "Vijaykumar Vyshak")
                    .replace("Rasikh Salam", "Rasikh Dar Salam")
                    .replace("Nitish Kumar Reddy", "Nitish Reddy")
                )
                name = int(players[name.rstrip()])
                SCORES[name]["bowling"]["dots"] = int(row_list[7])


def addMatch(data):

    for inning in range(len(data.get("scoreCard", []))):

        if data["scoreCard"] != []:
            batsmenData = data["scoreCard"][inning]["batTeamDetails"]
            bowlersData = data["scoreCard"][inning]["bowlTeamDetails"]

            for batter in batsmenData["batsmenData"]:
                batId = int(batsmenData["batsmenData"][batter]["batId"])

                # Add Player if not in output
                if batId not in SCORES:
                    SCORES[batId] = {
                        "playerID": -1,
                        "batting": {
                            "runs": 0,
                            "4s": 0,
                            "6s": 0,
                            "0s": 0,
                            "50s": 0,
                            "100s": 0,
                            "SR": -1,
                            "BF": 0,
                            "battingAverage": -1,
                            "dissmissals": 0,
                            "NOs": 0,
                            "HS": 0,
                        },
                        "bowling": {
                            "wickets": 0,
                            "dots": 0,
                            "economy": -1,
                            "runsConceded": 0,
                            "4H": 0,
                            "5H": 0,
                            "6H": 0,
                            "maiden": 0,
                            "bowlingAverage": -1,
                            "bSR": 0,
                            "overs": 0,
                        },
                        "fielding": {"catches": 0, "stumpings": 0},
                        "playerOfTheMatch": 0,  #
                    }

                # Get Info
                runs = batsmenData["batsmenData"][batter]["runs"]
                fours = batsmenData["batsmenData"][batter]["fours"]
                sixes = batsmenData["batsmenData"][batter]["sixes"]
                balls = batsmenData["batsmenData"][batter]["balls"]

                # Update Info
                SCORES[batId]["playerID"] = batId
                SCORES[batId]["batting"]["runs"] += runs
                SCORES[batId]["batting"]["4s"] += fours
                SCORES[batId]["batting"]["6s"] += sixes
                SCORES[batId]["batting"]["BF"] += balls
                SCORES[batId]["batting"]["HS"] = max(
                    SCORES[batId]["batting"]["HS"], runs
                )

                if runs >= 100:
                    SCORES[batId]["batting"]["100s"] += 1
                elif runs >= 50:
                    SCORES[batId]["batting"]["50s"] += 1
                if batsmenData["batsmenData"][batter]["outDesc"] == "not out":
                    SCORES[batId]["batting"]["NOs"] += 1
                else:
                    SCORES[batId]["batting"]["dissmissals"] += 1
                    if runs == 0 and balls > 0:
                        SCORES[batId]["batting"]["0s"] += 1

                if SCORES[batId]["batting"]["BF"] == 0:
                    SCORES[batId]["batting"]["SR"] = 0
                    SCORES[batId]["batting"]["battingAverage"] = 0
                else:
                    SCORES[batId]["batting"]["SR"] = round(
                        SCORES[batId]["batting"]["runs"]
                        / SCORES[batId]["batting"]["BF"]
                        * 100,
                        3,
                    )
                    if SCORES[batId]["batting"]["dissmissals"] == 0:
                        SCORES[batId]["batting"]["battingAverage"] = (
                            SCORES[batId]["batting"]["runs"] / 1
                        )
                    else:
                        SCORES[batId]["batting"]["battingAverage"] = round(
                            SCORES[batId]["batting"]["runs"]
                            / SCORES[batId]["batting"]["dissmissals"],
                            3,
                        )

            for bowler in bowlersData["bowlersData"]:
                bowlerId = bowlersData["bowlersData"][bowler]["bowlerId"]

                # Add Player if not in output
                if bowlerId not in SCORES:
                    SCORES[bowlerId] = {
                        "playerID": -1,
                        "batting": {
                            "runs": 0,
                            "4s": 0,
                            "6s": 0,
                            "0s": 0,
                            "50s": 0,
                            "100s": 0,
                            "SR": -1,
                            "BF": 0,
                            "battingAverage": -1,
                            "dissmissals": 0,
                            "NOs": 0,
                            "HS": 0,
                        },
                        "bowling": {
                            "wickets": 0,
                            "dots": 0,
                            "economy": -1,
                            "runsConceded": 0,
                            "4H": 0,
                            "5H": 0,
                            "6H": 0,
                            "maiden": 0,
                            "bowlingAverage": -1,
                            "bSR": 0,
                            "overs": 0,
                        },
                        "fielding": {"catches": 0, "stumpings": 0},
                        "playerOfTheMatch": 0,  #
                    }

                # Get Info
                wickets = bowlersData["bowlersData"][bowler]["wickets"]
                dots = bowlersData["bowlersData"][bowler]["dots"]

                runs = bowlersData["bowlersData"][bowler]["runs"]
                balls = (bowlersData["bowlersData"][bowler]["balls"] % 10) + (
                    int(bowlersData["bowlersData"][bowler]["balls"] / 10) * 6
                )

                maidens = bowlersData["bowlersData"][bowler]["maidens"]

                # Update Info
                SCORES[bowlerId]["playerID"] = bowlerId
                SCORES[bowlerId]["bowling"]["wickets"] += wickets
                SCORES[bowlerId]["bowling"]["dots"] += dots
                SCORES[bowlerId]["bowling"]["runsConceded"] += runs
                SCORES[bowlerId]["bowling"]["overs"] += round(balls / 6, 1)
                SCORES[bowlerId]["bowling"]["economy"] = round(
                    SCORES[bowlerId]["bowling"]["runsConceded"]
                    / SCORES[bowlerId]["bowling"]["overs"],
                    3,
                )
                SCORES[bowlerId]["bowling"]["maiden"] += maidens

                if SCORES[bowlerId]["bowling"]["wickets"] == 0:
                    SCORES[bowlerId]["bowling"]["bowlingAverage"] = -1
                    SCORES[bowlerId]["bowling"]["bSR"] = -1
                else:
                    SCORES[bowlerId]["bowling"]["bowlingAverage"] = round(
                        SCORES[bowlerId]["bowling"]["runsConceded"]
                        / SCORES[bowlerId]["bowling"]["wickets"],
                        3,
                    )
                    SCORES[bowlerId]["bowling"]["bSR"] = round(
                        SCORES[bowlerId]["bowling"]["overs"]
                        * 6
                        / SCORES[bowlerId]["bowling"]["wickets"],
                        3,
                    )

                if wickets >= 4:
                    SCORES[bowlerId]["bowling"]["4H"] += 1
                if wickets >= 5:
                    SCORES[bowlerId]["bowling"]["5H"] += 1
                if wickets >= 6:
                    SCORES[bowlerId]["bowling"]["6H"] += 1

        # Player of the Match
        if data["matchHeader"]["playersOfTheMatch"] != []:
            playerOfTheMatch = data["matchHeader"]["playersOfTheMatch"][0]["id"]
            if playerOfTheMatch in SCORES:
                SCORES[playerOfTheMatch]["playerOfTheMatch"] += 0.5
            else:
                SCORES[playerOfTheMatch] = {
                    "playerID": -1,
                    "batting": {
                        "runs": 0,
                        "4s": 0,
                        "6s": 0,
                        "0s": 0,
                        "50s": 0,
                        "100s": 0,
                        "SR": -1,
                        "BF": 0,
                        "battingAverage": -1,
                        "dissmissals": 0,
                        "NOs": 0,
                        "HS": 0,
                    },
                    "bowling": {
                        "wickets": 0,
                        "dots": 0,
                        "economy": -1,
                        "runsConceded": 0,
                        "4H": 0,
                        "5H": 0,
                        "6H": 0,
                        "maiden": 0,
                        "bowlingAverage": -1,
                        "bSR": 0,
                        "overs": 0,
                    },
                    "fielding": {"catches": 0, "stumpings": 0},
                    "playerOfTheMatch": 0,  #
                }
                SCORES[playerOfTheMatch]["playerOfTheMatch"] = 0.5


def computeLeaderboard():

    with open("Final Data/Scores.json", "r") as f:
        data = load(f)
    with open("Final Data\Players.json", "r") as f:
        players = load(f)

    for player in data:
        for stat in PLAYER_LEADERBOARD_BATTING:
            if data[player]["batting"][stat] != -1:
                PLAYER_LEADERBOARD_BATTING[stat].append(
                    [
                        data[player]["batting"][stat],
                        players[str(data[player]["playerID"])],
                    ]
                )

        for stat in PLAYER_LEADERBOARD_BOWLING:
            if data[player]["bowling"][stat] != -1:
                PLAYER_LEADERBOARD_BOWLING[stat].append(
                    [
                        data[player]["bowling"][stat],
                        players[str(data[player]["playerID"])],
                    ]
                )

        for stat in PLAYER_LEADERBOARD_FIELDING:
            if data[player][stat] != -1:
                PLAYER_LEADERBOARD_FIELDING[stat].append(
                    [data[player][stat], players[str(data[player]["playerID"])]]
                )

    # Sorting
    PLAYER_LEADERBOARD_BATTING["runs"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["4s"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["6s"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["0s"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["50s"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["100s"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["SR"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["battingAverage"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["NOs"].sort(reverse=True)
    PLAYER_LEADERBOARD_BATTING["HS"].sort(reverse=True)

    PLAYER_LEADERBOARD_BOWLING["wickets"].sort(reverse=True)
    PLAYER_LEADERBOARD_BOWLING["dots"].sort(reverse=True)
    PLAYER_LEADERBOARD_BOWLING["4H"].sort(reverse=True)
    PLAYER_LEADERBOARD_BOWLING["5H"].sort(reverse=True)
    PLAYER_LEADERBOARD_BOWLING["6H"].sort(reverse=True)
    PLAYER_LEADERBOARD_BOWLING["maiden"].sort(reverse=True)
    PLAYER_LEADERBOARD_BOWLING["economy"].sort()
    PLAYER_LEADERBOARD_BOWLING["bowlingAverage"].sort()
    PLAYER_LEADERBOARD_BOWLING["bSR"].sort()
    PLAYER_LEADERBOARD_BOWLING["overs"].sort(reverse=True)

    PLAYER_LEADERBOARD_FIELDING["playerOfTheMatch"].sort(reverse=True)


def updateComputation():

    # Add all matches
    for file in listdir("Data"):
        with open(f"Data/{file}", "r") as f:
            try:
                int(file.split(".")[0])
                addMatch(load(f))
            except ValueError:
                pass
    getDots()
    with open("Final Data/Scores.json", "w") as f:
        dump(SCORES, f, indent=2)

    # Compute Leaderboard
    computeLeaderboard()
    with open("Final Data/Leaderboard.json", "w") as f:
        final = {
            "batting": PLAYER_LEADERBOARD_BATTING,
            "bowling": PLAYER_LEADERBOARD_BOWLING,
            "fielding": PLAYER_LEADERBOARD_FIELDING,
        }
        dump(final, f, indent=2)


updateComputation()
