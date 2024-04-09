from Constants import MATCHES_URL, SERIES_HEADER
from requests import get


def getSeriesIDs():

    series_data = get(MATCHES_URL, headers=SERIES_HEADER)
    series_data = series_data.json()

    matchIDS = []
    for match in series_data["matchDetails"]:
        try:
            matchIDS.append(match["matchDetailsMap"]["match"][0]["matchInfo"]["matchId"])
        except:
            pass    
    
    return matchIDS

def getMatchData(matchID):

    match_data = get(f"https://cricbuzz-cricket.p.rapidapi.com/match/v1/{matchID}", headers=SERIES_HEADER)
    match_data = match_data.json()

    return match_data
