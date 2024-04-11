import json


path = "Data\Players.json"


with open(path, "r") as f:
    data = json.load(f)

    players_dict = {}

    for team in data:
        for player_info in team["player"]:
            if not player_info.get("isHeader", False):
                players_dict[player_info["id"]] = player_info["name"]

    # Write the players dictionary to a JSON file
    with open("players.json", "w") as json_file:
        json.dump(players_dict, json_file, indent=4)