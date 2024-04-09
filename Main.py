# Imports
import json
from bs4 import BeautifulSoup
from time import time
from pprint import pprint
from Functions import (
    clear,
    get_team_data,
    get_4_5_plus_wickets,
    combine_stats,
    compute_points,
    PLAYER_MAXES,
)

# Variables
TEAM_URLS = [
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=4343",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=4344",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=6904",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=4341",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=6903",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=4346",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=4342",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=4345",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=4340",
    "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2024-15940?team=5143",
]
FOURFIVE_PLUS_WICKETS_URL = "https://www.espncricinfo.com/records/tournament/bowling-most-5wi-career/indian-premier-league-2024-15940?team=4343"
DATA = json.dumps([])
EXTRA_DATA = json.loads(open("backend\Data.json").read())

# * Start
clear()
# * Finish


# * Get Data
start = time()
print("\033[92mGetting Data\033[0m", end=" ")

FOURFIVE_WICKET_DATA = get_4_5_plus_wickets(FOURFIVE_PLUS_WICKETS_URL)
DATA = json.dumps([get_team_data(team_url) for team_url in TEAM_URLS])
DOTS = {}

with open("backend\Example HTMLs\DOTS.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")
    table_body = soup.find("tbody")
    DOTS = {}

    for row in table_body.find_all("tr"):
        row_list = []
        for cell in row.find_all("td"):
            row_list.append(
                cell.text.strip()
                .replace("\n", "")
                .replace("  ", "")
                .replace("PBKS", "")
                .replace("DC", "")
                .replace("CSK", "")
                .replace("MI", "")
                .replace("KKR", "")
                .replace("RR", "")
                .replace("RCB", "")
                .replace("SRH", "")
            )
        if len(row_list) > 0:
            DOTS[row_list[1]] = row_list[7]
print(f" - {round(time() - start, 3):.3f}s")

pprint(DOTS)
# * Finish


# * Parse Data
start = time()
print("\033[92mParsing Data\033[0m", end=" ")

FOURFIVE_WICKET_DATA = json.dumps(FOURFIVE_WICKET_DATA)
DATA = json.dumps(combine_stats(DATA, FOURFIVE_WICKET_DATA))
DATA = json.loads(DATA)

for owner in EXTRA_DATA:
    for player in owner["Squad"]:
        if player["new_name"] in DATA:
            DATA[player["new_name"]].update(
                {
                    "Owner": owner["Owner"],
                    "old_name": player["old_name"],
                    "isBowler": player["isBowler"],
                    "isBatsman": player["isBatsman"],
                    "Team": player["Team"],
                    "Position": player["Position"],
                    "MOM": player["MOM"],
                    "6+": player["6+"],
                    "HT": player["HT"],
                }
            )

        else:
            DATA[player["new_name"]] = {
                "Owner": owner["Owner"],
                "old_name": player["old_name"],
                "isBowler": player["isBowler"],
                "isBatsman": player["isBatsman"],
                "Team": player["Team"],
                "MOM": player["MOM"],
                "6+": player["6+"],
                "HT": player["HT"],
            }
        try:
            DATA[player["new_name"]]["bowling"]["dots"] = int(
                DOTS.get(player["old_name"], 0)
            )
        except:
            pass
print(f" - {round(time() - start, 3):.3f}s")
# * Finish


# * Compute
start = time()
print("\033[92mComputing Data\033[0m", end=" ")

# General Points
for player in DATA:
    DATA[player]["points"] = compute_points(DATA[player])

# Maxes
for max in PLAYER_MAXES:
    category = PLAYER_MAXES[max][0]
    if max == "0":
        DATA[PLAYER_MAXES[max][2]]["points"] -= 1000
        DATA[PLAYER_MAXES[max][2]]["category"] = category
    if len(PLAYER_MAXES[max]) > 2:
        DATA[PLAYER_MAXES[max][2]]["points"] += 1000
        DATA[PLAYER_MAXES[max][2]]["category"] = category

# Team Maxes
TEAM_MAXES = {}

print(f" - {round(time() - start, 3):.3f}s")
# * Finish


# * Leaderboard
start = time()
print("\033[92mLeaderboard\033[0m - 0.000s")
leaderboard = {
    "AARAV": 0,
    "AARNAV": 0,
    "ABHAYA": 0,
    "ARYAN": 0,
    "ISHAAN": 0,
    "KAUSHAL": 0,
    "TEJAS": 0,
    "VIGGY": 0,
}

for player in DATA:
    if "Owner" in DATA[player] and DATA[player]["Owner"] in leaderboard:
        leaderboard[DATA[player]["Owner"]] += DATA[player]["points"]

sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
rank = 1

print("\n{:<10s} {:<10s} {:<10s}".format("Rank", "Owner", "Points"))
for owner, points in sorted_leaderboard:
    print("{:<10d} {:<10s} {:<10d}".format(rank, owner, int(points)))
    rank += 1
# * Finish


# ! Debugging
DATA = json.dumps(DATA)
with open("backend\Example JSON\data_combined.json", "w") as file:
    file.write(DATA)

# pprint(PLAYER_MAXES)
# ! Finish
