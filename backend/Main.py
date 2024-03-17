# Imports
from Functions import format_batter_table, format_bowler_table, clear, create_team
from requests import get
from Data import O, W, B, A, S, P

# Variables
BATTING_DATA_SOURCE = "https://www.espncricinfo.com/records/tournament/averages-batting/indian-premier-league-2023-15129"
BOWLING_DATA_SOURCE = "https://www.espncricinfo.com/records/tournament/bowling-most-wickets-career/indian-premier-league-2023-15129"

#! Main
clear()
print("\033[91mIPL Fantasy Points Calculator:\033[0m\n")


#! Batting Calculations
print("\033[92mBatting Calculations...\033[0m")
print("\033[90mRuns, Strike Rate, 0s, 50s, 100s, NOs\033[0m")
response = get(BATTING_DATA_SOURCE)
batting_data = format_batter_table(response.text)
print("\n")


#! Bowling Calculations
print("\033[92mBowling Calculations...\033[0m")
print("\033[90mWickets, Maidens, Hat-Tricks, 4+ Wickets, 5+ Wickets, 6+ Wickets, Economy Rate\033[0m")
response = get(BOWLING_DATA_SOURCE)
bowling_data = format_bowler_table(response.text)
print("\n")


#! Create Players and Teams
print("\033[92mCreate Players and Teams\033[0m")
teams = []
teams.append(create_team(batting_data, bowling_data, "Team O", O))
teams.append(create_team(batting_data, bowling_data, "Team W", W))
teams.append(create_team(batting_data, bowling_data, "Team B", B))
teams.append(create_team(batting_data, bowling_data, "Team A", A))
teams.append(create_team(batting_data, bowling_data, "Team S", S))
teams.append(create_team(batting_data, bowling_data, "Team P", P))

print("\n")

#! Generate Reports
print("\033[92mGenerate Reports\033[0m")