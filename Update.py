from Constants import MATCHES_URL, SERIES_HEADER
from requests import get
from json import dump, load
from datetime import datetime
from pprint import pprint


def updateSeries():
    """
    Updates the series data by making an API request to the MATCHES_URL and saving the response to a JSON file.
    """
    series_data = get(MATCHES_URL, headers=SERIES_HEADER).json()
    with open(f"Data/series.json", "w") as f:
        dump(series_data, f)


def updateMatch(matchID):
    """
    Updates the match data by making an API request to the MATCHES_URL and saving the response to a JSON file.
    """
    match_data = get(
        f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{matchID}/hscard",
        headers=SERIES_HEADER,
    ).json()
    with open(f"Data/{matchID}.json", "w") as f:
        dump(match_data, f)


#! Function is called every 10 minutes during match active times. Then one last time 1 hour after active times
def UpdateData(updateSeries=False):
    """
    UpdateData function updates the data for IPL matches.

    Args:
        updateSeries (bool, optional): Flag to update series data. Defaults to False.
    """

    if updateSeries:
        updateSeries(update=True)

    with open("Data/series.json", "r") as f:
        series_data = load(f)["matchDetails"]

    count_updated = 0
    for matchDetailsMap in series_data:
        if "matchDetailsMap" in matchDetailsMap:
            for match in matchDetailsMap["matchDetailsMap"]["match"]:

                start_time = int(match["matchInfo"]["startDate"]) / 1000
                state = match["matchInfo"]["state"]
                match_id = match["matchInfo"]["matchId"]

                year = datetime.fromtimestamp(start_time).year == datetime.now().year
                month = datetime.fromtimestamp(start_time).month == datetime.now().month
                day = datetime.fromtimestamp(start_time).day == datetime.now().day

                if year and month and day:
                    updateMatch(match_id)
                    print(f"Updated match {match_id}")
                    count_updated += 1

    return count_updated


if __name__ == "__main__":
    print(f"Updated {UpdateData()} games")
