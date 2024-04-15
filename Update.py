from Constants import MATCHES_URL, SERIES_HEADER
from Compute import updateComputation
from datetime import datetime
from json import dump, load
from discord import Embed
from requests import get
from os import path


def updateSeries():
    """
    Updates the series data by making an API request to the MATCHES_URL and saving the response to a JSON file.
    """
    series_data = get(MATCHES_URL, headers=SERIES_HEADER).json()
    script_dir = "/root/IPL-Fantasy-Discord-Bot"
    data_dir = path.join(script_dir, "Data")
    file_path = path.join(data_dir, "series.json")
    with open(file_path, "w") as f:
        dump(series_data, f)


def updateMatch(matchID):
    """
    Updates the match data by making an API request to the MATCHES_URL and saving the response to a JSON file.
    """
    match_data = get(
        f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{matchID}/hscard",
        headers=SERIES_HEADER,
    ).json()
    script_dir = "/root/IPL-Fantasy-Discord-Bot"
    data_dir = path.join(script_dir, "Data")
    file_path = path.join(data_dir, f"{matchID}.json")
    with open(file_path, "w") as f:
        dump(match_data, f)


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


def Update(updateSeries=False):
    """
    Updates the series data, computed data, and last refreshed time.

    Args:
        updateSeries (bool, optional): Whether to update the series data. Defaults to False.

    Returns:
        discord.Embed: An embed object containing information about the updated matches and series data.
    """

    # Update the Series Data
    if updateSeries:
        updated = UpdateData(updateSeries=True)
    else:
        updated = UpdateData()
    print(f"Updated {updated} matches")

    # Update the Computed Data
    updateComputation()

    # Update the Last Refreshed Time
    script_dir = "/root/IPL-Fantasy-Discord-Bot"
    data_dir = path.join(script_dir, "Final Data")
    file_path = path.join(data_dir, "LastRefresedh.json")
    with open(file_path, "w") as f:
        dump({"time": datetime.now().timestamp()}, f)

    embed = Embed(
        title="Updated Series & Live Matches",
        colour=0x00B0F4,
        timestamp=datetime.now(),
    )
    embed.set_author(name="IPL Fantasy")
    embed.add_field(name="Updated Matches", value=updated, inline=False)
    embed.add_field(name="Series Data", value=updateSeries, inline=False)
    embed.set_thumbnail(
        url="https://lh3.googleusercontent.com/a/ACg8ocKII8LPTqmYUAgEyzvcZCeAd1_sZKoj2giIvs8Zhw-Y9cyvolbt=s96-c-rg-br100"
    )
    embed.set_footer(text="Updated")

    return embed
