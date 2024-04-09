# Imports
from json import dumps

# Servers
IPL_FANTASY_SERVER = 1217282031336161340

# Users
USER = {
    763115173690867712: "AARAV",
    513839169907458049: "AARNAV",
    803363684801708063: "ABHAYA",
    844571246863712287: "ARYAN",
    786024792800362517: "ISHAAN",
    290606544352182273: "KAUSHAL",
    735615304570241085: "TEJAS",
    915063961777500180: "VIGGY",
}

# Channels
OWNER_LEADERBOARD_CHANNEL = 1224061081207443486
PLAYER_LEADERBOARD_CHANNEL = 1224061135649509416
COMMANDS_CHANNEL = 1224055625290354778
LOGS_CHANNEL = 1224060954971603096

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

# Final Variables
PLAYER_MAXES = {
    "NO": [0, []],
    "Runs": [0, []],
    "Ave": [0, []],
    "SR": [0, []],
    "100": [0, []],
    "50": [0, []],
    "0": [0, []],
    "4s": [0, []],
    "6s": [0, []],
    "Wkts": [0, []],
    "dots": [0, []],
    "Mdns": [0, []],
    "Econ": [float("inf"), []],
    "Ave": [0, []],
    "Ct": [0, []],
    "St": [0, []],
    "MOM": [0, []],
}
TEAM_MAXES = {}
LEADERBOARD = {
    "AARAV": 0,
    "AARNAV": 0,
    "ABHAYA": 0,
    "ARYAN": 0,
    "ISHAAN": 0,
    "KAUSHAL": 0,
    "TEJAS": 0,
    "VIGGY": 0,
}
DATA = dumps([])
