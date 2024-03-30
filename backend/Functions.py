from bs4 import BeautifulSoup
from os import system, name
from json import loads
from requests import get
from sys import maxsize


CATEGORY_MAXES = {
    "yellow_batting": [0, ""],
    "green_batting": [0, ""],
    "cyan_batting": [0, ""],
    "yellow_bowling": [0, ""],
    "purple_bowling": [0, ""],
    "green_bowling": [0, ""],
}
GLOBAL_MAXES = {
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
    "Econ": [0, []],
    "Ave": [0, []],
}


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
            "Mat": int(player_info[1].replace("*", "")) if player_info[1] != "-" else 0,
            "Inns": int(player_info[2].replace("*", "")) if player_info[2] != "-" else 0,
            "NO": int(player_info[3].replace("*", "")) if player_info[3] != "-" else 0,
            "Runs": int(player_info[4].replace("*", "")) if player_info[4] != "-" else 0,
            "BF": int(player_info[5].replace("*", "")) if player_info[5] != "-" else 0,
            "HS": int(player_info[6].replace("*", "")) if player_info[6] != "-" else 0,
            "Ave": float(player_info[7].replace("*", "")) if player_info[7] != "-" else 0,
            "SR": float(player_info[8].replace("*", "")) if player_info[8] != "-" else 0,
            "100": int(player_info[9].replace("*", "")) if player_info[9] != "-" else 0,
            "50": int(player_info[10].replace("*", "")) if player_info[10] != "-" else 0,
            "0": int(player_info[11].replace("*", "")) if player_info[11] != "-" else 0,
            "4s": int(player_info[12].replace("*", "")) if player_info[12] != "-" else 0,
            "6s": int(player_info[13].replace("*", "")) if player_info[13] != "-" else 0,
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
        player_info = [cell.text.strip().replace("*", "")
                       for cell in row.find_all("td")]
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
    """
    Retrieves the data for players who have taken 4 or 5 wickets in a match from a given URL.

    Args:
        url (str): The URL of the webpage containing the data.

    Returns:
        dict: A dictionary containing the player names as keys and their wicket data as values.
              The wicket data includes the player name, number of 4-wicket hauls, and number of 5-wicket hauls.
    """

    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table_body = soup.find("tbody")

    # Extract table rows
    wicket_data = {}
    if str(table_body.find_all("tr")).find("No records found") != -1:
        return wicket_data

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
    data = loads(json_data)
    additional_stats = loads(additional_data)

    for team in data:

        # Batting
        for player, batting_stats in team["batting"].items():
            if player not in combined_stats:
                combined_stats[player] = {"batting": {}, "bowling": {}}

            combined_stats[player]["batting"] = batting_stats
            combined_stats[player]["batting"]["boundaries"] = batting_stats["4s"]

            combined_stats[player]["points"] = 0
            combined_stats[player]["position"] = ""

        # Bowling
        for player, bowling_stats in team["bowling"].items():
            if player not in combined_stats:
                combined_stats[player] = {
                    "batting": {},
                    "bowling": {},
                    "4": 0,
                    "5": 0,
                    "6": 0,
                    "dots": 0,
                    "Hat-Tricks": 0,
                }

            combined_stats[player]["bowling"] = bowling_stats
            combined_stats[player]["bowling"]["4"] = 0
            combined_stats[player]["bowling"]["5"] = 0

            combined_stats[player]["bowling"]["6"] = 0
            combined_stats[player]["bowling"]["Hat-Tricks"] = 0

    # Process additional data
    for player, stats in additional_stats.items():
        player_name = player.split(" (")[0]

        # If the player is not already in the combined stats, add them
        if player_name not in combined_stats:
            combined_stats[player_name] = {
                "batting": {},
                "bowling": {},
                "4": 0,
                "5": 0,
                "6": 0,
                "dots": 0,
                "Hat-Tricks": 0,
            }

        # Update 4 and 5 wicket hauls
        combined_stats[player_name]["bowling"]["4"] = stats.get("4", 0)
        combined_stats[player_name]["bowling"]["5"] = stats.get("5", 0)

    return combined_stats


def compute_points(player):
    """
    Compute the total points for a given player based on their performance in batting and bowling.

    Args:
        player (dict): A dictionary containing the player's information, including their batting and bowling stats.

    Returns:
        int: The total points earned by the player.

    """
    # Variables
    total = 0
    name = player.get("old_name")
    isBowler = player.get("isBowler")
    isBatsman = player.get("isBatsman")
    team = player.get("Team")
    report = f"Player: {name}, Team: {team}, isBowler: {isBowler}, isBatsman: {isBatsman}\n"

    # Bowling Points
    bowling = 0
    report += "Bowling Points:\n"

    # Yellow
    yellow_bowling = 0
    yellow_wkts = player.get("bowling", {}).get("Wkts", 0)
    yellow_dots = player.get("bowling", {}).get("dots", 0)
    yellow_4s = player.get("bowling", {}).get("4", 0)
    yellow_5s = player.get("bowling", {}).get("5", 0)
    yellow_6s = player.get("6+", 0)
    yellow_HT = player.get("HT", 0)
    yellow_mdns = player.get("bowling", {}).get("Mdns", 0)
    yellow_ave = player.get("bowling", {}).get("Ave", 0)

    yellow_bowling += yellow_wkts * 50
    yellow_bowling += yellow_dots * 5
    yellow_bowling += yellow_4s * 250
    yellow_bowling += yellow_5s * 500
    yellow_bowling += yellow_6s * 1000
    yellow_bowling += yellow_HT * 2000
    yellow_bowling += yellow_mdns * 150

    # TODO: Adjust formula
    yellow_bowling += yellow_ave * 100
    report += f"  - Average: {yellow_ave:.2f}\n"

    report += f"  - Wickets: {yellow_wkts} x 50 = {yellow_wkts * 50}\n"
    report += f"  - Dots: {yellow_dots} x 5 = {yellow_dots * 5}\n"
    report += f"  - 4s: {yellow_4s} x 250 = {yellow_4s * 250}\n"
    report += f"  - 5s: {yellow_5s} x 500 = {yellow_5s * 500}\n"
    report += f"  - 6s: {yellow_6s} x 1000 = {yellow_6s * 1000}\n"
    report += f"  - Maidens: {yellow_mdns} x 150 = {yellow_mdns * 150}\n"
    report += f"  - Hat-Tricks: {yellow_HT} x 2000 = {yellow_HT * 2000}\n"
    update_max_category("yellow_bowling", yellow_bowling, player)

    # Purple
    purple_bowling = 0
    econ = player.get("bowling", {}).get("Econ", float('inf'))
    overs = player.get("bowling", {}).get("Overs", 0)
    if overs > 5:
        if econ > 11:
            purple_bowling -= 500
            report += f"  - Economy: {econ:.2f} -> -500\n"
        elif econ > 10:
            purple_bowling -= 400
            report += f"  - Economy: {econ:.2f} -> -400\n"
        elif econ > 9:
            purple_bowling -= 200
            report += f"  - Economy: {econ:.2f} -> -200\n"
        elif econ > 8:
            purple_bowling -= 100
            report += f"  - Economy: {econ:.2f} -> -100\n"
        elif econ > 6:
            purple_bowling += 100
            report += f"  - Economy: {econ:.2f} -> 100\n"
        elif econ > 5:
            purple_bowling += 250
            report += f"  - Economy: {econ:.2f} -> 250\n"
        elif econ > 4:
            purple_bowling += 500
            report += f"  - Economy: {econ:.2f} -> 500\n"
        elif econ > 3:
            purple_bowling += 800
            report += f"  - Economy: {econ:.2f} -> 800\n"
        elif econ > 2:
            purple_bowling += 1200
            report += f"  - Economy: {econ:.2f} -> 1200\n"
        elif econ > 1:
            purple_bowling += 1500
            report += f"  - Economy: {econ:.2f} -> 1500\n"
        else:
            purple_bowling += 2000
            report += f"  - Economy: {econ:.2f} -> 2000\n"
        update_max_category("purple_bowling", purple_bowling, player)

    # Green
    green_bowling = 0
    wkts = player.get("bowling", {}).get("Wkts", 0)
    if wkts > 35:
        green_bowling += 5000
    elif wkts > 30:
        green_bowling += 4000
    elif wkts > 25:
        green_bowling += 3000
    elif wkts > 20:
        green_bowling += 2000
    elif wkts > 15:
        green_bowling += 1000
    report += f"  - Wickets: {wkts}\n"
    update_max_category("green_bowling", green_bowling, player)

    # Batting Points
    batting = 0
    report += "Batting Points:\n"

    # Yellow
    yellow_batting = 0
    runs = player.get("batting", {}).get("Runs", 0)
    boundaries = player.get("batting", {}).get("boundaries", 0)
    sixes = player.get("batting", {}).get("6s", 0)
    zeros = player.get("batting", {}).get("0", 0)
    fifties = player.get("batting", {}).get("50", 0)
    centuries = player.get("batting", {}).get("100", 0)
    ave = player.get("batting", {}).get("Ave", 0)

    yellow_batting += runs * 2
    yellow_batting += boundaries * 4
    yellow_batting += sixes * 8
    yellow_batting += zeros * -6
    yellow_batting += fifties * 50
    yellow_batting += centuries * 100

    # TODO: Adjust formula
    yellow_batting += ave * 100
    report += f"  - Average: {ave:.2f}\n"

    report += f"  - Runs: {runs} x 2 = {runs * 2}\n"
    report += f"  - Boundaries: {boundaries} x 4 = {boundaries * 4}\n"
    report += f"  - Sixes: {sixes} x 8 = {sixes * 8}\n"
    report += f"  - Zeros: {zeros} x -6 = {zeros * -6}\n"
    report += f"  - Fifties: {fifties} x 50 = {fifties * 50}\n"
    report += f"  - Centuries: {centuries} x 100 = {centuries * 100}\n"
    update_max_category("yellow_batting", yellow_batting, player)

    # Green
    green_batting = 0
    bf = player.get("batting", {}).get("BF", 0)
    sr = player.get("batting", {}).get("SR", 0)
    if bf > 15:
        if sr > 200:
            green_batting += 1000
            report += f"  - Strike Rate: {sr:.2f} -> 1000\n"
        elif sr > 175:
            green_batting += 800
            report += f"  - Strike Rate: {sr:.2f} -> 800\n"
        elif sr > 150:
            green_batting += 600
            report += f"  - Strike Rate: {sr:.2f} -> 600\n"
        elif sr > 125:
            green_batting += 400
            report += f"  - Strike Rate: {sr:.2f} -> 400\n"
        elif sr > 100:
            green_batting += 200
            report += f"  - Strike Rate: {sr:.2f} -> 200\n"
        elif sr < 75:
            green_batting -= 200
            report += f"  - Strike Rate: {sr:.2f} -> -200\n"
        elif sr < 50:
            green_batting -= 300
            report += f"  - Strike Rate: {sr:.2f} -> -300\n"
        elif sr < 25:
            green_batting -= 500
            report += f"  - Strike Rate: {sr:.2f} -> -500\n"
        else:
            green_batting -= 100
            report += f"  - Strike Rate: {sr:.2f} -> -100\n"
    update_max_category("green_batting", green_batting, player)

    # Cyan
    cyan_batting = 0
    if runs > 850:
        cyan_batting += 5000
    elif runs > 800:
        cyan_batting += 4500
    elif runs > 750:
        cyan_batting += 4000
    elif runs > 700:
        cyan_batting += 3500
    elif runs > 650:
        cyan_batting += 3000
    elif runs > 600:
        cyan_batting += 2500
    elif runs > 550:
        cyan_batting += 2000
    elif runs > 500:
        cyan_batting += 1500
    elif runs > 450:
        cyan_batting += 1000
    elif runs > 400:
        cyan_batting += 750
    elif runs > 350:
        cyan_batting += 500
    elif runs > 300:
        cyan_batting += 250
    update_max_category("cyan_batting", cyan_batting, player)

    # Sub Total
    update_maxes(player)
    st = player.get("bowling", {}).get("St", 0)
    ct = player.get("bowling", {}).get("Ct", 0)
    mom = player.get("MOM", 0)
    report += f"Other ({(st * 50) + (ct * 25)}):\n  - Stumpings: {st} x 50 = {st * 50}\n  - Catches: {ct} x 25 = {ct * 25}\n  - MOM: {mom} x 100 = {mom * 100}\n"
    report += f"Balls Faced: {bf}, Overs Bowled: {player.get('bowling', {}).get('Overs', 0)}\n"

    other = (st * 50) + (ct * 25) + (mom * 100)
    batting = yellow_batting + green_batting + cyan_batting
    bowling = yellow_bowling + purple_bowling + green_bowling

    # Position Points
    if player.get("isBowler") == True and batting > 0:
        batting *= 2
    elif player.get("isBatsman") == True and bowling > 0:
        bowling *= 2
    elif player.get("isBowler") == True and batting < 0:
        batting /= 2
    elif player.get("isBatsman") == True and bowling < 0:
        bowling /= 2

    # Total Points
    total = batting + bowling + other

    # C/VC Points
    if player.get("Position") == "VC":
        total *= 1.5
    elif player.get("Position") == "C":
        total *= 2

    report += f"\nTotal Points: {total}, Owner: {player.get('Owner')}\n\n\n\n"

    #! Write to file
    if player.get("Owner") == "Viggy":
        with open("backend\Reports\Viggy.txt", "a") as file:
            file.write(report)
    elif player.get("Owner") == "Kaushal":
        with open("backend\Reports\Kaushal.txt", "a") as file:
            file.write(report)

    return total


def update_max_category(category, value, player):
    """
    Update the maximum value for a given category and the owner of the player with that maximum value.

    Parameters:
    - category (str): The category for which the maximum value needs to be updated.
    - value (int): The new value to be compared with the current maximum value.
    - player (dict): The player object containing information about the player.

    Returns:
    None
    """
    current_max = CATEGORY_MAXES.get(category, [0, ""])[0]
    if value > current_max:
        CATEGORY_MAXES[category] = [value, player.get("Owner")]


def update_maxes(player):
    """
    Update the global maximum values for batting and bowling statistics based on the given player's stats.

    Args:
        player (dict): A dictionary containing the player's batting and bowling statistics.

    Returns:
        None
    """

    batting_stats = ["NO", "Runs", "Ave",
                     "100", "50", "0", "4s", "6s", "HS"]
    bowling_stats = ["Wkts", "dots", "Mdns", "Ave"]

    if "batting" in player:
        for stat in batting_stats:
            current_max = GLOBAL_MAXES.get(stat, [0, ""])[0]
            player_stat = player.get("batting", {}).get(stat, 0)

            if player_stat > current_max:
                GLOBAL_MAXES[stat] = [
                    player_stat,
                    player.get("Team", ""),
                    player.get("bowling", {}).get("Player", ""),
                ]

        current_max = GLOBAL_MAXES.get("SR", [0, ""])[0]
        player_sr = player.get("batting", {}).get("SR", 0)
        player_bf = player.get("batting", {}).get("BF", 0)
        if player_sr > current_max and player_bf > 15:
            GLOBAL_MAXES["SR"] = [
                player_sr,
                player.get("Team", ""),
                player.get("bowling", {}).get("Player", ""),
            ]
    if "bowling" in player:
        for stat in bowling_stats:
            current_max = GLOBAL_MAXES.get(stat, [0, ""])[0]
            player_stat = player.get("bowling", {}).get(stat, 0)

            if player_stat > current_max:
                GLOBAL_MAXES[stat] = [
                    player_stat,
                    player.get("Team", ""),
                    player.get("bowling", {}).get("Player", ""),
                ]

        current_max = GLOBAL_MAXES.get("Econ", [0, ""])[0]
        player_econ = player.get("bowling", {}).get("Econ", 0)
        player_overs = player.get("bowling", {}).get("Overs", 0)

        if player_econ < current_max and player_overs > 5:
            GLOBAL_MAXES["Econ"] = [
                player_econ,
                player.get("Team", ""),
                player.get("bowling", {}).get("Player", ""),
            ]

    # TODO: Add 1000 points to teams
