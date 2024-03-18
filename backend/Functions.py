from bs4 import BeautifulSoup
from os import system, name
import json
from requests import get


def format_batter_table(html_data: str):
    """
    Formats the HTML data of a batter table and returns a dictionary containing player information.

    Args:
        html_data (str): The HTML data of the batter table.

    Returns:
        dict: A dictionary containing player information, where the player name is the key and the player data is the value.

    """
    # Parse HTML data
    soup = BeautifulSoup(html_data, "html.parser")
    table_body = soup.find("tbody")

    # Extract table rows
    player_data = {}
    for row in table_body.find_all("tr"):
        player_info = [cell.text.strip() for cell in row.find_all("td")]
        player_info[6] = player_info[6].replace("*", "")
        player_name = player_info[0].split("(")[0].strip()
        player_data[player_name] = {
            "Player": player_name,
            "Mat": int(player_info[1]) if player_info[1] != "-" else 0,
            "Inns": int(player_info[2]) if player_info[2] != "-" else 0,
            "NO": int(player_info[3]) if player_info[3] != "-" else 0,
            "Runs": int(player_info[4]) if player_info[4] != "-" else 0,
            "BF": int(player_info[5]) if player_info[5] != "-" else 0,
            "HS": int(player_info[6]) if player_info[6] != "-" else 0,
            "Ave": float(player_info[7]) if player_info[7] != "-" else 0,
            "SR": float(player_info[8]) if player_info[8] != "-" else 0,
            "100": int(player_info[9]) if player_info[9] != "-" else 0,
            "50": int(player_info[10]) if player_info[10] != "-" else 0,
            "0": int(player_info[11]) if player_info[11] != "-" else 0,
            "4s": int(player_info[12]) if player_info[12] != "-" else 0,
            "6s": int(player_info[13]) if player_info[13] != "-" else 0,
        }

    return player_data


def format_bowler_table(html_data: str):
    """
    Parses the HTML data and extracts information from the bowler table.

    Args:
        html_data (str): The HTML data containing the bowler table.

    Returns:
        dict: A dictionary containing the formatted bowler data.

    Example:
        html_data = "<html>...</html>"
        bowler_data = format_bowler_table(html_data)
    """

    # Parse HTML data
    soup = BeautifulSoup(html_data, "html.parser")
    table_body = soup.find("tbody")

    # Extract table rows
    player_data = {}
    for row in table_body.find_all("tr"):
        player_info = [cell.text.strip() for cell in row.find_all("td")]
        player_name = player_info[0]
        player_data[player_name] = {
            "Player": player_name,
            "Span": player_info[1],
            "Mat": int(player_info[2]) if player_info[2] != "-" else 0,
            "Inns": int(player_info[3]) if player_info[3] != "-" else 0,
            "Overs": float(player_info[4]) if player_info[4] != "-" else 0,
            "Mdns": int(player_info[5]) if player_info[5] != "-" else 0,
            "Runs": int(player_info[6]) if player_info[6] != "-" else 0,
            "Wkts": int(player_info[7]) if player_info[7] != "-" else 0,
            "BBI": player_info[8] if player_info[8] != "-" else 0,
            "Ave": float(player_info[9]) if player_info[9] != "-" else 0,
            "Econ": float(player_info[10]) if player_info[10] != "-" else 0,
            "SR": float(player_info[11]) if player_info[11] != "-" else 0,
            "5": int(player_info[12]) if player_info[12] != "-" else 0,
            "10": int(player_info[13]) if player_info[13] != "-" else 0,
            "Ct": int(player_info[14]) if player_info[14] != "-" else 0,
            "St": int(player_info[15]) if player_info[15] != "-" else 0,
        }

    return player_data


def get_team_data(url: str):
    """
    Fetches the batting and bowling data for a team.

    Args:
        url (str): The URL of the team data.

    Returns:
        dict: A dictionary containing the batting and bowling data for a team.

    Example:
        url = "https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4343"
        team_data = get_team_data(url)
    """
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    batting_table = tables[0]
    bowling_table = tables[1]

    return {
        "batting": format_batter_table(str(batting_table)),
        "bowling": format_bowler_table(str(bowling_table)),
    }


def get_4_5_plus_wickets(url: str):

    # Parse HTML data
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table_body = soup.find("tbody")

    # Extract table rows
    wicket_data = {}
    for row in table_body.find_all("tr"):
        player_info = [cell.text.strip() for cell in row.find_all("td")]
        player_name = player_info[0]
        wicket_data[player_name] = {
            "Player": player_name,
            "4": int(player_info[13]) if player_info[13] != "-" else 0,
            "5": int(player_info[14]) if player_info[14] != "-" else 0,
        }

    return wicket_data


def clear():
    """
    Clears the console screen.
    """
    system("cls" if name == "nt" else "clear")


def combine_stats(json_data, additional_data):
    """
    Combines the batting and bowling statistics from JSON data and additional data.

    Args:
        json_data (str): JSON data containing batting and bowling statistics.
        additional_data (str): Additional data containing player statistics.

    Returns:
        dict: Combined statistics of players, including batting and bowling details.

    """
    combined_stats = {}

    # Parse JSON
    data = json.loads(json_data)
    additional_stats = json.loads(additional_data)

    for team in data:

        # Batting
        for player, batting_stats in team["batting"].items():
            if player not in combined_stats:
                combined_stats[player] = {"batting": {}, "bowling": {}}

            combined_stats[player]["batting"] = batting_stats
            combined_stats[player]["batting"]["boundaries"] = batting_stats["4s"] + batting_stats["6s"]

            combined_stats[player]["points"] = 0
            combined_stats[player]["position"] = ""

        # Bowling
        for player, bowling_stats in team["bowling"].items():
            if player not in combined_stats:
                combined_stats[player] = {"batting": {}, "bowling": {}, "4": 0, "5": 0, "6": 0, "dots": 0, "Hat-Tricks": 0}

            combined_stats[player]["bowling"] = bowling_stats
            combined_stats[player]["bowling"]["4"] = 0
            combined_stats[player]["bowling"]["5"] = 0

            #TODO: Add 6+ wickets and hat-tricks and dots
            combined_stats[player]["bowling"]["6"] = 0
            combined_stats[player]["bowling"]["dots"] = 0
            combined_stats[player]["bowling"]["Hat-Tricks"] = 0


    # Process additional data
    for player, stats in additional_stats.items():
        player_name = player.split(" (")[0]

        # If the player is not already in the combined stats, add them
        if player_name not in combined_stats:
            combined_stats[player_name] = {"batting": {}, "bowling": {}, "4": 0, "5": 0, "6": 0, "dots": 0, "Hat-Tricks": 0}

        # Update 4 and 5 wicket hauls
        combined_stats[player_name]["bowling"]["4"] = stats.get("4", 0)
        combined_stats[player_name]["bowling"]["5"] = stats.get("5", 0)

    return combined_stats

def compute_points(player):

    total = 0

    # Bowling Points
    bowling = 0

    # Yellow
    bowling += player["bowling"]["Wkts"] * 50
    bowling += player["bowling"]["dots"] * 50
    bowling += player["bowling"]["4"] * 250
    bowling += player["bowling"]["5"] * 500
    bowling += player["bowling"]["6"] * 1000
    bowling += player["bowling"]["Mdns"] * 150

    # Purple
    if player["bowling"]["Overs"] > 5:
        if player["bowling"]["Econ"] > 11:
            bowling -= 500
        elif player["bowling"]["Econ"] > 10:
            bowling -= 400
        elif player["bowling"]["Econ"] > 9:
            bowling -= 200
        elif player["bowling"]["Econ"] > 8:
            bowling -= 100
        elif player["bowling"]["Econ"] > 6:
            bowling += 100
        elif player["bowling"]["Econ"] > 5:
            bowling += 250
        elif player["bowling"]["Econ"] > 4:
            bowling += 500
        elif player["bowling"]["Econ"] > 3:
            bowling += 800
        elif player["bowling"]["Econ"] > 2:
            bowling += 1200
        elif player["bowling"]["Econ"] > 1:
            bowling += 1500
        else:
            bowling += 2000
    
    # Green
    if player["bowling"]["Wkts"] > 35:
        bowling += 5000
    elif player["bowling"]["Wkts"] > 30:
        bowling += 4000
    elif player["bowling"]["Wkts"] > 25:
        bowling += 3000
    elif player["bowling"]["Wkts"] > 20:
        bowling += 2000
    elif player["bowling"]["Wkts"] > 15:
        bowling += 1000

    # TODO: Include Maxes
    
    # Batting Points
    batting = 0

    # Yellow
    batting += player["batting"]["Runs"] * 2
    batting += player["batting"]["boundaries"] * 4
    batting += player["batting"]["6s"] * 8
    batting += player["batting"]["0"] * -6
    batting += player["batting"]["50"] * 50
    batting += player["batting"]["100"] * 100

    # Green
    if player["batting"]["BF"] > 500:
        if player["batting"]["SR"] > 200:
            batting += 1000
        elif player["batting"]["SR"] > 175:
            batting += 800
        elif player["batting"]["SR"] > 150:
            batting += 600
        elif player["batting"]["SR"] > 125:
            batting += 400
        elif player["batting"]["SR"] > 100:
            batting += 200
        elif player["batting"]["SR"] < 75:
            batting -= 200
        elif player["batting"]["SR"] < 50:
            batting -= 300
        elif player["batting"]["SR"] < 25:
            batting -= 500
        else:
            batting -= 100
    
    # Cyan
    if player["batting"]["Runs"] > 850:
        batting += 5000
    elif player["batting"]["Runs"] > 800:
        batting += 4500
    elif player["batting"]["Runs"] > 750:
        batting += 4000
    elif player["batting"]["Runs"] > 700:
        batting += 3500
    elif player["batting"]["Runs"] > 650:
        batting += 3000
    elif player["batting"]["Runs"] > 600:
        batting += 2500
    elif player["batting"]["Runs"] > 550:
        batting += 2000
    elif player["batting"]["Runs"] > 500:
        batting += 1500
    elif player["batting"]["Runs"] > 450:
        batting += 1000
    elif player["batting"]["Runs"] > 400:
        batting += 750
    elif player["batting"]["Runs"] > 350:
        batting += 500
    elif player["batting"]["Runs"] > 300:
        batting += 250

    # TODO: Include Maxes
        
    # TODO: Include Position Points (double for bowlers/batters, vc/captain, etc.)
    total += player["batting"]["St"] * 50
    total += player["batting"]["Ct"] * 25
    total = batting + bowling

    return (total, None)
    

