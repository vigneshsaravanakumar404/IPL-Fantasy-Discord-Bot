# TODO: Update series ID each day at 12:00 AM
# TODO: Update day's match at 11:59 PM
# TODO: Update each match 90 times evenly throughout match start to end + 1 hour (for two game days spread out further)
# TODO: Store data in each game's file

from Constants import MATCHES_URL, SERIES_HEADER
from requests import get


def getSeriesIDs():
    """
    Retrieves the series IDs of matches from the given API endpoint.

    Returns:
        list: A list of match IDs.
    """
    series_data = get(MATCHES_URL, headers=SERIES_HEADER)
    series_data = series_data.json()

    matchIDS = []
    for match in series_data["matchDetails"]:
        try:
            matchIDS.append(
                match["matchDetailsMap"]["match"][0]["matchInfo"]["matchId"]
            )
        except:
            pass

    return matchIDS


# TODO
def getMatchData(matchID):

    match_data = get(
        f"https://cricbuzz-cricket.p.rapidapi.com/match/v1/{matchID}",
        headers=SERIES_HEADER,
    )
    match_data = match_data.json()

    return match_data
