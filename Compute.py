from pprint import pprint
import json
import os


output = {}
matches = []

def addMatch(data):
    if data.get("scoreCard", []) != []:
        matches.append(data["scoreCard"][0]["batTeamDetails"]["batTeamName"] + " vs " + data["scoreCard"][0]["bowlTeamDetails"]["bowlTeamName"])
    for inning in range(len(data.get("scoreCard", []))):
        if data["scoreCard"] != []:
            batsmenData = data["scoreCard"][inning]["batTeamDetails"]
            print(data["scoreCard"][inning]["batTeamDetails"]["batTeamName"] + " vs " + data["scoreCard"][inning]["bowlTeamDetails"]["bowlTeamName"])
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
                not_out = batsmenData["batsmenData"][batter]["outDesc"] == "not out"

                # Update Info
                output[batId]["playerID"] = batId
                output[batId]["batting"]["runs"] += runs
                output[batId]["batting"]["4s"] += fours
                output[batId]["batting"]["6s"] += sixes
                output[batId]["batting"]["BF"] += balls
                output[batId]["batting"]["HS"] = max(
                    output[batId]["batting"]["HS"], runs
                )

                if output[batId]["batting"]["BF"] == 0:
                    output[batId]["batting"]["SR"] = 0
                    output[batId]["batting"]["battingAverage"] = 0
                else:
                    output[batId]["batting"]["SR"] = (
                        output[batId]["batting"]["runs"]
                        / output[batId]["batting"]["BF"]
                        * 100
                    )
                    output[batId]["batting"]["battingAverage"] = (
                        output[batId]["batting"]["runs"]
                        / output[batId]["batting"]["BF"]
                    )

                if runs >= 100:
                    output[batId]["batting"]["100s"] += 1
                elif runs >= 50:
                    output[batId]["batting"]["50s"] += 1
                if not_out:
                    output[batId]["batting"]["NOs"] += 1
                elif runs == 0 and balls > 0:
                    output[batId]["batting"]["0s"] += 1

                if batId == 11813:
                    print(
                        f"runs: {runs}, fours: {fours}, sixes: {sixes}, balls: {balls}, not_out: {not_out}"
                    )

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
                output[bowlerId]["bowling"]["overs"] += balls / 6
                output[bowlerId]["bowling"]["economy"] = (
                    output[bowlerId]["bowling"]["runsConceded"]
                    / output[bowlerId]["bowling"]["overs"]
                )
                output[bowlerId]["bowling"]["maiden"] += maidens

                if output[bowlerId]["bowling"]["wickets"] == 0:
                    output[bowlerId]["bowling"]["bowlingAverage"] = -1
                    output[bowlerId]["bowling"]["bSR"] = -1
                else:
                    output[bowlerId]["bowling"]["bowlingAverage"] = (
                        output[bowlerId]["bowling"]["runsConceded"]
                        / output[bowlerId]["bowling"]["wickets"]
                    )
                    output[bowlerId]["bowling"]["bSR"] = (
                        output[bowlerId]["bowling"]["overs"]
                        / output[bowlerId]["bowling"]["wickets"]
                    )

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


for file in os.listdir("Data"):
    with open(f"Data/{file}", "r") as f:
        try:
            addMatch(json.load(f))
        except ValueError:
            pass

with open("Data/Output.json", "w") as f:
    json.dump(output, f, indent=2)

print(len(matches))