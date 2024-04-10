from pprint import pprint
import json
import os


output = {}
template = {
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
        "battingAverage": [],
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
        "bowlingAverage": [],
        "bSR": 0,
        "overs": 0,
    },
    "fielding": {
        "catches": 0,
        "stumpings": 0
    },
    "playerOfTheMatch": 0 #
}

def addMatch(data):
    for inning in range(len(data["scoreCard"])):
        if data["scoreCard"] != []:
            batsmenData = data["scoreCard"][inning]["batTeamDetails"]
            bowlersData = data["scoreCard"][inning]["bowlTeamDetails"]
            
            for batter in batsmenData["batsmenData"]:
                
                # Add Player if not in output
                if batsmenData["batsmenData"][batter]["batId"] not in output:
                    output[batsmenData["batsmenData"][batter]["batId"]] = template

                # Get Info
                id = batsmenData["batsmenData"][batter]["batId"]
                runs = batsmenData["batsmenData"][batter]["runs"]
                fours = batsmenData["batsmenData"][batter]["fours"]
                sixes = batsmenData["batsmenData"][batter]["sixes"]
                balls = batsmenData["batsmenData"][batter]["balls"]
                not_out = batsmenData["batsmenData"][batter]["outDesc"] == "not out"

                # Update Info
                output[id]["playerID"] = id
                output[id]["batting"]["runs"] += runs
                output[id]["batting"]["4s"] += fours
                output[id]["batting"]["6s"] += sixes
                output[id]["batting"]["BF"] += balls
                output[id]["batting"]["SR"] = output[id]["batting"]["runs"] / output[id]["batting"]["BF"] * 100
                output[id]["batting"]["battingAverage"].append(runs)
                output[id]["batting"]["HS"] = max(output[id]["batting"]["HS"], runs)
                if runs >= 100:
                    output[id]["batting"]["100s"] += 1
                elif runs >= 50:
                    output[id]["batting"]["50s"] += 1
                if not_out:
                    output[id]["batting"]["NOs"] += 1
                elif runs == 0 and balls > 0:
                    output[id]["batting"]["0s"] += 1
                
            for bowler in bowlersData["bowlersData"]:

                # Add Player if not in output
                if bowlersData["bowlersData"][bowler]["bowlerId"] not in output:
                    output[bowlersData["bowlersData"][bowler]["bowlerId"]] = template

                # Get Info
                id = bowlersData["bowlersData"][bowler]["bowlerId"]
                wickets = bowlersData["bowlersData"][bowler]["wickets"]
                dots = bowlersData["bowlersData"][bowler]["dots"]
                runs = bowlersData["bowlersData"][bowler]["runs"]
                balls = bowlersData["bowlersData"][bowler]["balls"]
                maidens = bowlersData["bowlersData"][bowler]["maidens"]

                # Update Info
                output[id]["playerID"] = id
                output[id]["bowling"]["wickets"] += wickets
                output[id]["bowling"]["dots"] += dots
                output[id]["bowling"]["runsConceded"] += runs
                output[id]["bowling"]["overs"] += balls / 6
                output[id]["bowling"]["economy"] = output[id]["bowling"]["runsConceded"] / output[id]["bowling"]["overs"]
                output[id]["bowling"]["bowlingAverage"].append(runs)
                output[id]["bowling"]["maiden"] += maidens
                output[id]["bowling"]["bSR"] = output[id]["bowling"]["overs"] * 6 / output[id]["bowling"]["wickets"]
                if wickets >= 4:
                    output[id]["bowling"]["4H"] += 1
                if wickets >= 5:
                    output[id]["bowling"]["5H"] += 1
                if wickets >= 6:
                    output[id]["bowling"]["6H"] += 1
            
            # Copare IDs
            print(id, bowlersData["bowlersData"][bowler]["bowlerId"], batsmenData["batsmenData"][batter]["batId"])


        # Fielding
        #TODO: Award Catches and Stumpings

        # Player of the Match
        playerOfTheMatch = data["matchHeader"]["playersOfTheMatch"][0]["id"]
        if playerOfTheMatch in output:
            output[playerOfTheMatch]["playerOfTheMatch"] += 1
        else:
            output[playerOfTheMatch] = template
            output[playerOfTheMatch]["playerOfTheMatch"] = 1

for file in os.listdir("Data"):
    with open(f"Data/{file}", "r") as f:
        try:
            print(int(file.split(".")[0]))
            addMatch(json.load(f))
        except ValueError:
            print(f"Skipping {file}")

with open("Data/Output.json", "w") as f:
    json.dump(output, f, indent=2)

