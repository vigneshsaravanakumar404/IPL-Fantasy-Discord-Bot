from bs4 import BeautifulSoup
from os import system, name
from pprint import pprint
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
    soup = BeautifulSoup(html_data, 'html.parser')
    table_body = soup.find('tbody')

    # Extract table rows
    player_data = {}
    for row in table_body.find_all('tr'):
        player_info = [cell.text.strip() for cell in row.find_all('td')]
        player_name = player_info[0].split('(')[0].strip()
        player_data[player_name] = {
            "Player": player_name,
            "Mat": int(player_info[1]) if player_info[1] != '-' else player_info[1],
            "Inns": int(player_info[2]) if player_info[2] != '-' else player_info[2],
            "NO": int(player_info[3]) if player_info[3] != '-' else player_info[3],
            "Runs": int(player_info[4]) if player_info[4] != '-' else player_info[4],
            "BF": int(player_info[5]) if player_info[5] != '-' else player_info[5],
            "HS": player_info[6],
            "Ave": float(player_info[7]) if player_info[7] != '-' else player_info[7],
            "SR": float(player_info[8]) if player_info[8] != '-' else player_info[8],
            "100": int(player_info[9]) if player_info[9] != '-' else player_info[9],
            "50": int(player_info[10]) if player_info[10] != '-' else player_info[10],
            "0": int(player_info[11]) if player_info[11] != '-' else player_info[11],
            "4s": int(player_info[12]) if player_info[12] != '-' else player_info[12],
            "6s": int(player_info[13]) if player_info[13] != '-' else player_info[13]
        }

    return player_data

# Missing: Dot Balls, 6s, Hat-Tricks
# Get 4s from: https://www.espncricinfo.com/records/tournament/bowling-most-4wi-career/indian-premier-league-2023-15129
# Get 5s from: https://www.espncricinfo.com/records/tournament/bowling-most-5wi-career/indian-premier-league-2023-15129
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
    soup = BeautifulSoup(html_data, 'html.parser')
    table_body = soup.find('tbody')

    # Extract table rows
    player_data = {}
    for row in table_body.find_all('tr'):
        player_info = [cell.text.strip() for cell in row.find_all('td')]
        player_name = player_info[0]
        player_data[player_name] = {
            "Player": player_name,
            "Span": player_info[1],
            "Mat": int(player_info[2]) if player_info[2] != '-' else player_info[2],
            "Inns": int(player_info[3]) if player_info[3] != '-' else player_info[3],
            "Overs": float(player_info[4]) if player_info[4] != '-' else player_info[4],
            "Mdns": int(player_info[5]) if player_info[5] != '-' else player_info[5],
            "Runs": int(player_info[6]) if player_info[6] != '-' else player_info[6],
            "Wkts": int(player_info[7]) if player_info[7] != '-' else player_info[7],
            "BBI": player_info[8],
            "Ave": float(player_info[9]) if player_info[9] != '-' else player_info[9],
            "Econ": float(player_info[10]) if player_info[10] != '-' else player_info[10],
            "SR": float(player_info[11]) if player_info[11] != '-' else player_info[11],
            "5": int(player_info[12]) if player_info[12] != '-' else player_info[12],
            "10": int(player_info[13]) if player_info[13] != '-' else player_info[13],
            "Ct": int(player_info[14]) if player_info[14] != '-' else player_info[14],
            "St": int(player_info[15]) if player_info[15] != '-' else player_info[15]
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
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    
    batting_table = tables[0]
    bowling_table = tables[1]

    return {
        "batting": format_batter_table(str(batting_table)),
        "bowling": format_bowler_table(str(bowling_table))
    }


def clear():
    """
    Clears the console screen.
    """
    system('cls' if name == 'nt' else 'clear')
