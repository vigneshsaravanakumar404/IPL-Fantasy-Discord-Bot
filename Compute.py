from pprint import pprint
import json
import os
import prettytable

output = {}

def addMatch(data):

    for inning in range(len(data.get("scoreCard", []))):

        if data["scoreCard"] != []:
            batsmenData = data["scoreCard"][inning]["batTeamDetails"]
            bowlersData = data["scoreCard"][inning]["bowlTeamDetails"]

            for batter in batsmenData["batsmenData"]:
                batId = int(batsmenData["batsmenData"][batter]["batId"])


                # Add Player if not in output
                if batId not in output:
                    output[batId] = {
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

                if batsmenData["batsmenData"][batter]["outDesc"] == "not out":
                    out = "Not Out"
                elif batsmenData["batsmenData"][batter]["outDesc"] == "":
                    out = "Did Not Bat"
                else:
                    out = "Out"

                # Update Info
                output[batId]["playerID"] = batId
                output[batId]["batting"]["runs"] += runs
                output[batId]["batting"]["4s"] += fours
                output[batId]["batting"]["6s"] += sixes
                output[batId]["batting"]["BF"] += balls
                output[batId]["batting"]["HS"] = max(
                    output[batId]["batting"]["HS"], runs
                )

                if runs >= 100:
                    output[batId]["batting"]["100s"] += 1
                elif runs >= 50:
                    output[batId]["batting"]["50s"] += 1
                if out == "not out":
                    output[batId]["batting"]["NOs"] += 1
                elif out == "Out":
                    output[batId]["batting"]["dissmissals"] += 1
                elif runs == 0 and balls > 0:
                    output[batId]["batting"]["0s"] += 1
                

                if output[batId]["batting"]["BF"] == 0:
                    output[batId]["batting"]["SR"] = 0
                    output[batId]["batting"]["battingAverage"] = 0
                else:
                    output[batId]["batting"]["SR"] = (
                        round(output[batId]["batting"]["runs"]
                        / output[batId]["batting"]["BF"]
                        * 100, 3)
                    )
                    if output[batId]["batting"]["dissmissals"] == 0:
                        output[batId]["batting"]["battingAverage"] = output[batId]["batting"]["runs"] / 1
                    else:
                        output[batId]["batting"]["battingAverage"] = (
                            round(output[batId]["batting"]["runs"] 
                            / output[batId]["batting"]["dissmissals"], 3)
                        )

                # if batId == 11813:
                #     print(
                #         f"runs: {runs}, fours: {fours}, sixes: {sixes}, balls: {balls}, not_out: {not_out}"
                #     )
                

            for bowler in bowlersData["bowlersData"]:
                bowlerId = bowlersData["bowlersData"][bowler]["bowlerId"]

                # Add Player if not in output
                if bowlerId not in output:
                    output[bowlerId] = {
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
                balls = bowlersData["bowlersData"][bowler]["balls"]
                maidens = bowlersData["bowlersData"][bowler]["maidens"]

                # Update Info
                output[bowlerId]["playerID"] = bowlerId
                output[bowlerId]["bowling"]["wickets"] += wickets
                output[bowlerId]["bowling"]["dots"] += dots
                output[bowlerId]["bowling"]["runsConceded"] += runs
                output[bowlerId]["bowling"]["overs"] += round(balls / 6, 1)
                output[bowlerId]["bowling"]["economy"] = (
                    round(output[bowlerId]["bowling"]["runsConceded"]
                    / output[bowlerId]["bowling"]["overs"], 3)
                )
                output[bowlerId]["bowling"]["maiden"] += maidens

                if output[bowlerId]["bowling"]["wickets"] == 0:
                    output[bowlerId]["bowling"]["bowlingAverage"] = -1
                    output[bowlerId]["bowling"]["bSR"] = -1
                else:
                    output[bowlerId]["bowling"]["bowlingAverage"] = (
                        round(output[bowlerId]["bowling"]["runsConceded"]
                        / output[bowlerId]["bowling"]["wickets"], 3)
                    )
                    output[bowlerId]["bowling"]["bSR"] = (
                        round(output[bowlerId]["bowling"]["overs"]
                        / output[bowlerId]["bowling"]["wickets"], 3)
                    )
                    print(round(output[bowlerId]["bowling"]["overs"]
                        / output[bowlerId]["bowling"]["wickets"], 3))

                if wickets >= 4:
                    output[bowlerId]["bowling"]["4H"] += 1
                if wickets >= 5:
                    output[bowlerId]["bowling"]["5H"] += 1
                if wickets >= 6:
                    output[bowlerId]["bowling"]["6H"] += 1

        # Fielding
        # TODO: Award Catches and Stumpings

        # Player of the Match
        if data["matchHeader"]["playersOfTheMatch"] != []:
            playerOfTheMatch = data["matchHeader"]["playersOfTheMatch"][0]["id"]
            if playerOfTheMatch in output:
                output[playerOfTheMatch]["playerOfTheMatch"] += 1            
            else:
                output[playerOfTheMatch] = {
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
                output[playerOfTheMatch]["playerOfTheMatch"] = 1


# TODO
def computePlayerBaseStats():

    return None
    with open ("Data/Output.json", "r") as f:
        data = json.load(f)
    
    for player in data:
        
        # Batting Points
        batting = data[player]["batting"]

        # Bowling Points
        bowling = data[player]["bowling"]

        pprint(batting)
        pprint(bowling)
        exit()

# TODO
def computeLeaderboard():
    #TODO: Remove players that dont meet balls faced or overs bowled criteria

    RUNS = []
    FOURS = []
    SIXES = []
    DUCKS = []
    FIFTIES = []
    CENTURIES = []
    SR = []
    BATTING_AVERAGE = []
    NOS = []
    HS = []

    WICKETS = []
    DOTS = []
    FOURWICKETS = []
    FIVEWICKETS = []
    SIXWICKETS = []
    MAIDENS = []
    ECONOMY = []
    BOWL_AVERAGE = []
    BSR = []

    LEADERBOARD_BATTING = { "runs" : RUNS, "4s" : FOURS, "6s" : SIXES, "0s" : DUCKS, "50s" : FIFTIES, "100s" : CENTURIES, "SR" : SR, "battingAverage" : BATTING_AVERAGE, "NOs" : NOS, "HS" : HS }
    LEADERBOARD_BOWLING = { "wickets" : WICKETS, "dots" : DOTS, "4H" : FOURWICKETS, "5H" : FIVEWICKETS, "6H" : SIXWICKETS, "maiden" : MAIDENS, "economy" : ECONOMY, "bowlingAverage" : BOWL_AVERAGE, "bSR" : BSR }                                  
    with open ("Data/Output.json", "r") as f:
        data = json.load(f)
    
    with open("Data\Players.json", "r") as f:
        players = json.load(f)

    pprint(players["1413"])

    for player in data:
        for stat in LEADERBOARD_BATTING:
            if data[player]["batting"][stat] != -1:
                LEADERBOARD_BATTING[stat].append([data[player]["batting"][stat], players[str(data[player]["playerID"])]])
        
        for stat in LEADERBOARD_BOWLING:
            if data[player]["bowling"][stat] != -1:
                LEADERBOARD_BOWLING[stat].append([data[player]["bowling"][stat], players[str(data[player]["playerID"])]])

    # Sorting
    LEADERBOARD_BATTING["runs"].sort(reverse=True)
    LEADERBOARD_BATTING["4s"].sort(reverse=True)
    LEADERBOARD_BATTING["6s"].sort(reverse=True)
    LEADERBOARD_BATTING["0s"].sort(reverse=True)
    LEADERBOARD_BATTING["50s"].sort(reverse=True)
    LEADERBOARD_BATTING["100s"].sort(reverse=True)
    LEADERBOARD_BATTING["SR"].sort(reverse=True)
    LEADERBOARD_BATTING["battingAverage"].sort(reverse=True)
    LEADERBOARD_BATTING["NOs"].sort(reverse=True)
    LEADERBOARD_BATTING["HS"].sort(reverse=True)

    LEADERBOARD_BOWLING["wickets"].sort(reverse=True)
    LEADERBOARD_BOWLING["dots"].sort(reverse=True)
    LEADERBOARD_BOWLING["4H"].sort(reverse=True)
    LEADERBOARD_BOWLING["5H"].sort(reverse=True)
    LEADERBOARD_BOWLING["6H"].sort(reverse=True)
    LEADERBOARD_BOWLING["maiden"].sort(reverse=True)
    LEADERBOARD_BOWLING["economy"].sort()
    LEADERBOARD_BOWLING["bowlingAverage"].sort()
    LEADERBOARD_BOWLING["bSR"].sort()

    pprint(LEADERBOARD_BOWLING["bSR"])


    # Print the top 10 in each category using prett table
    output = ""
    for stat in LEADERBOARD_BATTING:
        table = prettytable.PrettyTable()
        table.field_names = [stat, "Player ID"]
        for entry in LEADERBOARD_BATTING[stat]:
            table.add_row(entry)
        print(table, "\n\n\n")
        output += str(str(table) + "\n\n\n")

    for stat in LEADERBOARD_BOWLING:
        table = prettytable.PrettyTable()
        table.field_names = [stat, "Player ID"]
        for entry in LEADERBOARD_BOWLING[stat]:
            table.add_row(entry)
        print(table, "\n\n\n")
        output += str(str(table) + "\n\n\n")

    with open("Data/Leaderboard.txt", "w") as f:
        f.write(output)
    

    


# TODO
def computeBonusStats():
    return None

# TODO
def computeTeamBaseStats():
    return None

# TODO
def computeTeamBonusStats():
    return None


def updateComputation():
    for file in os.listdir("Data"):
        with open(f"Data/{file}", "r") as f:
            try:
                addMatch(json.load(f))
            except ValueError:
                pass

    with open("Data/Output.json", "w") as f:
        json.dump(output, f, indent=2)

updateComputation()
computeLeaderboard()