from bs4 import BeautifulSoup
from os import system, name
import json
from requests import get

# General Source by team: https://www.espncricinfo.com/records/tournament/averages-batting-bowling-by-team/indian-premier-league-2023-15129?team=4343


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
        player_name = player_info[0].split("(")[0].strip()
        player_data[player_name] = {
            "Player": player_name,
            "Mat": int(player_info[1]) if player_info[1] != "-" else player_info[1],
            "Inns": int(player_info[2]) if player_info[2] != "-" else player_info[2],
            "NO": int(player_info[3]) if player_info[3] != "-" else player_info[3],
            "Runs": int(player_info[4]) if player_info[4] != "-" else player_info[4],
            "BF": int(player_info[5]) if player_info[5] != "-" else player_info[5],
            "HS": player_info[6],
            "Ave": float(player_info[7]) if player_info[7] != "-" else player_info[7],
            "SR": float(player_info[8]) if player_info[8] != "-" else player_info[8],
            "100": int(player_info[9]) if player_info[9] != "-" else player_info[9],
            "50": int(player_info[10]) if player_info[10] != "-" else player_info[10],
            "0": int(player_info[11]) if player_info[11] != "-" else player_info[11],
            "4s": int(player_info[12]) if player_info[12] != "-" else player_info[12],
            "6s": int(player_info[13]) if player_info[13] != "-" else player_info[13],
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
            "Mat": int(player_info[2]) if player_info[2] != "-" else player_info[2],
            "Inns": int(player_info[3]) if player_info[3] != "-" else player_info[3],
            "Overs": float(player_info[4]) if player_info[4] != "-" else player_info[4],
            "Mdns": int(player_info[5]) if player_info[5] != "-" else player_info[5],
            "Runs": int(player_info[6]) if player_info[6] != "-" else player_info[6],
            "Wkts": int(player_info[7]) if player_info[7] != "-" else player_info[7],
            "BBI": player_info[8],
            "Ave": float(player_info[9]) if player_info[9] != "-" else player_info[9],
            "Econ": float(player_info[10])
            if player_info[10] != "-"
            else player_info[10],
            "SR": float(player_info[11]) if player_info[11] != "-" else player_info[11],
            "5": int(player_info[12]) if player_info[12] != "-" else player_info[12],
            "10": int(player_info[13]) if player_info[13] != "-" else player_info[13],
            "Ct": int(player_info[14]) if player_info[14] != "-" else player_info[14],
            "St": int(player_info[15]) if player_info[15] != "-" else player_info[15],
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
            "4": int(player_info[13]) if player_info[13] != "-" else player_info[13],
            "5": int(player_info[14]) if player_info[14] != "-" else player_info[14],
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

        # Bowling
        for player, bowling_stats in team["bowling"].items():
            if player not in combined_stats:
                combined_stats[player] = {"batting": {}, "bowling": {}, "4": "-", "5": "-", "6": "-", "dots": "-", "Hat-Tricks": "-"}

            combined_stats[player]["bowling"] = bowling_stats
            combined_stats[player]["bowling"]["4"] = "-"
            combined_stats[player]["bowling"]["5"] = "-"

            #TODO: Add 6+ wickets and hat-tricks and dots
            combined_stats[player]["bowling"]["6"] = "-"
            combined_stats[player]["bowling"]["dots"] = "-"
            combined_stats[player]["bowling"]["Hat-Tricks"] = "-"

    # Process additional data
    for player, stats in additional_stats.items():
        player_name = player.split(" (")[0]

        # If the player is not already in the combined stats, add them
        if player_name not in combined_stats:
            combined_stats[player_name] = {"batting": {}, "bowling": {}, "4": "-", "5": "-", "6": "-", "dots": "-", "Hat-Tricks": "-"}

        # Update 4 and 5 wicket hauls
        combined_stats[player_name]["bowling"]["4"] = stats.get("4", 0)
        combined_stats[player_name]["bowling"]["5"] = stats.get("5", 0)

    return combined_stats
