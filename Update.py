from Constants import MATCHES_URL, SERIES_HEADER
from requests import get
from json import dump, load
from datetime import datetime as Datetime
import datetime



def getMatchIDs(update=False):
    """
    Retrieves the series IDs of matches from the given API endpoint.

    Args:
        update (bool, optional): Flag indicating whether to update the series data from the API.
                                Defaults to False.

    Returns:
        dict: A dictionary containing match IDs as keys and a list of start and end timestamps as values.
    """

    matchIDS = {}

    if update:
        series_data = get(MATCHES_URL, headers=SERIES_HEADER).json()

        directory_path = "Data"
        with open(f"{directory_path}/series.json", "w") as f:
            dump(series_data, f)
        print("Series Data Updated")

    else:
        with open("Data/series.json", "r") as f:
            series_data = load(f)
        print("Series Data Loaded")

    for match in series_data["matchDetails"]:
        try:
            matchIDS[match["matchDetailsMap"]["match"][0]["matchInfo"]["matchId"]] = [
                int(match["matchDetailsMap"]["match"][0]["matchInfo"]["startDate"]),
                int(match["matchDetailsMap"]["match"][0]["matchInfo"]["endDate"])
                + 3600000,
            ]
        except:
            pass

    return matchIDS


# TODO
def getMatchData(matchID):
    """
    Retrieves match data for a given match ID.

    Args:
        matchID (str): The ID of the match.

    Returns:
        dict: The match data in JSON format.
    """

    match_data = get(
        f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{matchID}/hscard",
        headers=SERIES_HEADER,
    )
    match_data = match_data.json()

    return match_data


# Call This Function Every 5 Minutes
def UpdateData():
    """
    Updates the data for IPL matches.

    This function retrieves the match IDs for IPL matches and checks if the current time falls within the match start and end time.
    If the current time is within the match time range, it fetches the match data and saves it as a JSON file.

    Returns:
        bool: True if any data was updated, False otherwise.
    """
    directory_path = "Data"
    updated = 0

    if Datetime.now().hour == 23 and Datetime.now().minute >= 55:
        matchIDS = getMatchIDs(update=True)
    else:
        matchIDS = getMatchIDs()

    closest_game = 0
    for matchID in matchIDS:
        print(datetime.datetime.fromtimestamp(matchIDS[matchID][0]/1000).strftime('%Y-%m-%d %H:%M:%S') + " to " + datetime.datetime.fromtimestamp(matchIDS[matchID][1]/1000).strftime('%Y-%m-%d %H:%M:%S'))

        if (int(Datetime.now().timestamp()) >= matchIDS[matchID][0] and int(Datetime.now().timestamp()) <= matchIDS[matchID][1]):

            match_data = getMatchData(matchID)
            with open(f"{directory_path}/{matchID}.json", "w") as f:
                dump(match_data, f)
            updated += 1

        if matchIDS[matchID][0] - int(Datetime.now().timestamp()) < closest_game:
            closest_game = matchIDS[matchID][0] - int(Datetime.now().timestamp())

    print(f"Closest Game in {closest_game} Seconds")
    return updated > 0


print(UpdateData())
