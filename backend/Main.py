# Imports
from Functions import clear, get_team_data
from requests import get
from flask import *


# Variables
TEAM_URLS = ["https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4343"]

#! Main
clear()

#! Team Data
for team_url in TEAM_URLS:
    print(get_team_data(team_url))
