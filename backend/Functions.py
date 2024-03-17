from bs4 import BeautifulSoup
from os import system, name
from Player import Player
from Team import Team
from pprint import pprint

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
        player_name = player_info[0].split('(')[0].strip()  # Extracting player name from the first cell
        player_data[player_name] = {
            "Span": player_info[1],
            "Mat": int(player_info[2]) if player_info[2] != '-' else player_info[2],
            "Inns": int(player_info[3]) if player_info[3] != '-' else player_info[3],
            "NO": int(player_info[4]) if player_info[4] != '-' else player_info[4],
            "Runs": int(player_info[5]) if player_info[5] != '-' else player_info[5],
            "HS": player_info[6],
            "Ave": float(player_info[7]) if player_info[7] != '-' else player_info[7],
            "BF": int(player_info[8]) if player_info[8] != '-' else player_info[8],
            "SR": float(player_info[9]) if player_info[9] != '-' else player_info[9],
            "100": int(player_info[10]) if player_info[10] != '-' else player_info[10],
            "50": int(player_info[11]) if player_info[11] != '-' else player_info[11],
            "0": int(player_info[12]) if player_info[12] != '-' else player_info[12],
            "4s": int(player_info[13]) if player_info[13] != '-' else player_info[13],
            "6s": int(player_info[14]) if player_info[14] != '-' else player_info[14]
        }

    pprint(player_data)
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
            "Balls": int(player_info[4]) if player_info[4] != '-' else player_info[4],
            "Overs": float(player_info[5]) if player_info[5] != '-' else player_info[5],
            "Mdns": int(player_info[6]) if player_info[6] != '-' else player_info[6],
            "Runs": int(player_info[7]) if player_info[7] != '-' else player_info[7],
            "Wkts": int(player_info[8]) if player_info[8] != '-' else player_info[8],
            "BBI": player_info[9],
            "Ave": float(player_info[10]) if player_info[10] != '-' else player_info[10],
            "Econ": float(player_info[11]) if player_info[11] != '-' else player_info[11],
            "SR": float(player_info[12]) if player_info[12] != '-' else player_info[12],
            "4": int(player_info[13]) if player_info[13] != '-' else player_info[13],
            "5": int(player_info[14]) if player_info[14] != '-' else player_info[14]
        }

    return player_data

def clear():
    """
    Clears the console screen.
    """
    system('cls' if name == 'nt' else 'clear')

def create_team(batting_data, bowling_data, team_name, player_names):
    players = []
    for player in player_names:
        players.append(Player(team_name, player[0], 
            batting_data.get(player[0], {}).get("Runs", 0), 
            batting_data.get(player[0], {}).get("SR", 0), 
            batting_data.get(player[0], {}).get("4s", 0), 
            batting_data.get(player[0], {}).get("6s", 0), 
            batting_data.get(player[0], {}).get("0", 0), 
            batting_data.get(player[0], {}).get("50", 0), 
            batting_data.get(player[0], {}).get("100", 0), 
            batting_data.get(player[0], {}).get("NO", 0), 
            player[1], 
            batting_data.get(player[0], {}).get("BF", 0), 
            bowling_data.get(player[0], {}).get("Wkts", 0), 
            bowling_data.get(player[0], {}).get("4", 0), 
            bowling_data.get(player[0], {}).get("5", 0), 
            player[2], 
            bowling_data.get(player[0], {}).get("Mdns", 0), 
            bowling_data.get(player[0], {}).get("hattrick", 0), 
            bowling_data.get(player[0], {}).get("Econ", 0), 
            bowling_data.get(player[0], {}).get("Overs", 0), 
            player[3], 
            player[4], 
            player[5], 
            player[6], 
            player[7]))
    return Team(team_name, players)
