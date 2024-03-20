# Imports
from Functions import clear, get_team_data, get_4_5_plus_wickets, combine_stats, compute_points
import json
from pprint import pprint

# Variables
TEST_TEAM_URLS = ["https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4343", "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4344"]
TEAM_URLS = [
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4343",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4344",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=6904",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4341",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=6903",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4346",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4342",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4345",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4340",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=5143"
]
FOURFIVE_PLUS_WICKETS_URL = "https://www.espncricinfo.com/records/tournament/bowling-most-5wi-career/indian-premier-league-2023-15129"
DATA = json.dumps([])
EXTRA_DATA = json.loads(open("backend\Data.json").read())

#! Start
clear()




#! Get Data 
#? Missing: Dot Balls, 6+ Wickets, Hat-Tricks
print("\033[92mGetting Data\033[0m")

FOURFIVE_WICKET_DATA = get_4_5_plus_wickets(FOURFIVE_PLUS_WICKETS_URL)
DATA = json.dumps([get_team_data(team_url) for team_url in TEAM_URLS])

print("\n")




#! Parse Data
print("\033[92mParsing Data\033[0m")

FOURFIVE_WICKET_DATA = json.dumps(FOURFIVE_WICKET_DATA)
DATA = json.dumps(combine_stats(DATA, FOURFIVE_WICKET_DATA))
DATA = json.loads(DATA)

for owner in EXTRA_DATA:
    for player in owner["Squad"]:
        if player["new_name"] in DATA:
            DATA[player["new_name"]].update({
                "Owner": owner["Owner"],
                "old_name": player["old_name"],
                "isBowler": player["isBowler"],
                "isBatsman": player["isBatsman"],
                "Team": player["Team"],
                "Position": player["Position"]
            })
        else:
            DATA[player["new_name"]] = {
                "Owner": owner["Owner"],
                "old_name": player["old_name"],
                "isBowler": player["isBowler"],
                "isBatsman": player["isBatsman"],
                "Team": player["Team"]
            }



print("\n")

#! Compute
print("\033[92mComputing Data\033[0m")

for player in DATA:
    # TODO: Include Maxes
    #TODO: Add 6+ wickets and hat-tricks and dots
    temp = compute_points(DATA[player])
    DATA[player]["points"] = temp[0]
print("\n")

# print the points for the player F du Plessis
pprint(DATA["F du Plessis"]["points"])


#* Debugging
DATA = json.dumps(DATA)
with open("backend\Example JSON\data_combined.json", "w") as file:
    file.write(DATA)

