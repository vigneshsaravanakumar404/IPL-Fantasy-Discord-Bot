import json
from pprint import pprint

teams = "Data\Teams.json"
players = "Data\Players.json"

with open(players, "r") as file:
    players = json.load(file)

    # get a list of all the values in the dictionary
    temp = list(players.values())

with open(teams, "r") as file:
    teams = json.load(file)

    for team in teams:
        for key in team:
            if key != "discord":
                for player in team[key]:
                    if player not in temp:
                        print(player)  # Varun Chakaravarthy
