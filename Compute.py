from pprint import pprint
from bs4 import BeautifulSoup
from re import sub
from json import load, dump
from os import listdir
import prettytable
import time


# Varibale
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
    "N": N,
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
OUTPUT = {}


# TODO
def computePlayerBaseStats():

    return None
    with open("Final Data/Scores.json", "r") as f:
        data = load(f)

    for player in data:

        # Batting Points
        batting = data[player]["batting"]

        # Bowling Points
        bowling = data[player]["bowling"]

        pprint(batting)
        pprint(bowling)
        exit()


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
                OUTPUT[int(players[name])]["bowling"]["dots"] = int(row_list[7])


def addMatch(data):

    for inning in range(len(data.get("scoreCard", []))):

        if data["scoreCard"] != []:
            batsmenData = data["scoreCard"][inning]["batTeamDetails"]
            bowlersData = data["scoreCard"][inning]["bowlTeamDetails"]

            for batter in batsmenData["batsmenData"]:
                batId = int(batsmenData["batsmenData"][batter]["batId"])

                # Add Player if not in output
                if batId not in OUTPUT:
                    OUTPUT[batId] = {
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
                            "N": 0,
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
                OUTPUT[batId]["playerID"] = batId
                OUTPUT[batId]["batting"]["runs"] += runs
                OUTPUT[batId]["batting"]["4s"] += fours
                OUTPUT[batId]["batting"]["6s"] += sixes
                OUTPUT[batId]["batting"]["BF"] += balls
                OUTPUT[batId]["batting"]["HS"] = max(
                    OUTPUT[batId]["batting"]["HS"], runs
                )

                if runs >= 100:
                    OUTPUT[batId]["batting"]["100s"] += 1
                elif runs >= 50:
                    OUTPUT[batId]["batting"]["50s"] += 1
                if batsmenData["batsmenData"][batter]["outDesc"] == "not out":
                    OUTPUT[batId]["batting"]["N"] += 1
                else:
                    OUTPUT[batId]["batting"]["dissmissals"] += 1
                    if runs == 0 and balls > 0:
                        OUTPUT[batId]["batting"]["0s"] += 1

                if OUTPUT[batId]["batting"]["BF"] == 0:
                    OUTPUT[batId]["batting"]["SR"] = 0
                    OUTPUT[batId]["batting"]["battingAverage"] = 0
                else:
                    OUTPUT[batId]["batting"]["SR"] = round(
                        OUTPUT[batId]["batting"]["runs"]
                        / OUTPUT[batId]["batting"]["BF"]
                        * 100,
                        3,
                    )
                    if OUTPUT[batId]["batting"]["dissmissals"] == 0:
                        OUTPUT[batId]["batting"]["battingAverage"] = (
                            OUTPUT[batId]["batting"]["runs"] / 1
                        )
                    else:
                        OUTPUT[batId]["batting"]["battingAverage"] = round(
                            OUTPUT[batId]["batting"]["runs"]
                            / OUTPUT[batId]["batting"]["dissmissals"],
                            3,
                        )

            for bowler in bowlersData["bowlersData"]:
                bowlerId = bowlersData["bowlersData"][bowler]["bowlerId"]

                # Add Player if not in output
                if bowlerId not in OUTPUT:
                    OUTPUT[bowlerId] = {
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
                            "N": 0,
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
                OUTPUT[bowlerId]["playerID"] = bowlerId
                OUTPUT[bowlerId]["bowling"]["wickets"] += wickets
                OUTPUT[bowlerId]["bowling"]["dots"] += dots
                OUTPUT[bowlerId]["bowling"]["runsConceded"] += runs
                OUTPUT[bowlerId]["bowling"]["overs"] += round(balls / 6, 1)
                OUTPUT[bowlerId]["bowling"]["economy"] = round(
                    OUTPUT[bowlerId]["bowling"]["runsConceded"]
                    / OUTPUT[bowlerId]["bowling"]["overs"],
                    3,
                )
                OUTPUT[bowlerId]["bowling"]["maiden"] += maidens

                if OUTPUT[bowlerId]["bowling"]["wickets"] == 0:
                    OUTPUT[bowlerId]["bowling"]["bowlingAverage"] = -1
                    OUTPUT[bowlerId]["bowling"]["bSR"] = -1
                else:
                    OUTPUT[bowlerId]["bowling"]["bowlingAverage"] = round(
                        OUTPUT[bowlerId]["bowling"]["runsConceded"]
                        / OUTPUT[bowlerId]["bowling"]["wickets"],
                        3,
                    )
                    OUTPUT[bowlerId]["bowling"]["bSR"] = round(
                        OUTPUT[bowlerId]["bowling"]["overs"]
                        * 6
                        / OUTPUT[bowlerId]["bowling"]["wickets"],
                        3,
                    )

                if wickets >= 4:
                    OUTPUT[bowlerId]["bowling"]["4H"] += 1
                if wickets >= 5:
                    OUTPUT[bowlerId]["bowling"]["5H"] += 1
                if wickets >= 6:
                    OUTPUT[bowlerId]["bowling"]["6H"] += 1

        # Player of the Match
        if data["matchHeader"]["playersOfTheMatch"] != []:
            playerOfTheMatch = data["matchHeader"]["playersOfTheMatch"][0]["id"]
            if playerOfTheMatch in OUTPUT:
                OUTPUT[playerOfTheMatch]["playerOfTheMatch"] += 1
            else:
                OUTPUT[playerOfTheMatch] = {
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
                        "N": 0,
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
                OUTPUT[playerOfTheMatch]["playerOfTheMatch"] = 1


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
    PLAYER_LEADERBOARD_BATTING["N"].sort(reverse=True)
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
    PLAYER_LEADERBOARD_BOWLING["overs"].sort()

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
        dump(OUTPUT, f, indent=2)

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
