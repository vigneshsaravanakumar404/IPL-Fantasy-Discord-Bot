# import discord
from Pagination import Pagination
from discord import app_commands, Embed
from datetime import datetime
from json import load
from os import path


# TODO: Add logging
# TODO: Deal with ties
# TODO: Add owner

# Variables
TRUNCATE_LIMIT = 9
GROUP = 10


def truncate_last_name(last_name: str) -> str:
    return (
        (last_name[: TRUNCATE_LIMIT - 2] + "..")
        if len(last_name) > TRUNCATE_LIMIT
        else last_name
    )


def maxNameLength(data: list) -> int:
    return min(
        TRUNCATE_LIMIT + 1,
        max(
            len(player[::-1][0].split()[0][0] + player[::-1][0].split()[-1])
            for player in data
        ),
    )


class LeaderboardGroup(app_commands.Group):

    @app_commands.command(
        name="bowling",
        description="Displays the leaderboard for a specific bowling statistic",
    )
    @app_commands.describe(stats="Statistics to choose from")
    @app_commands.choices(
        stats=[
            app_commands.Choice(name="Wickets", value="wickets"),
            app_commands.Choice(name="Dots", value="dots"),
            app_commands.Choice(name="4-Wicket Haul", value="4H"),
            app_commands.Choice(name="5-Wicket Haul", value="5H"),
            app_commands.Choice(name="6-Wicket Haul", value="6H"),
            app_commands.Choice(name="Maiden", value="maiden"),
            app_commands.Choice(name="Economy", value="economy"),
            app_commands.Choice(name="Bowling Average", value="bowlingAverage"),
            app_commands.Choice(name="Bowling Strike Rate", value="bSR"),
            app_commands.Choice(name="Overs", value="overs"),
        ]
    )
    async def bowling(self, interaction, stats: app_commands.Choice[str]):
        """
        Displays the leaderboard for a specific bowling statistic.

        Parameters:
        - interaction: The interaction object representing the user's interaction with the command.
        - stats: The chosen bowling statistic to display the leaderboard for.

        Returns:
        None
        """

        # Parse Variables
        file_path = path.join(
            path.join("/root/IPL-Fantasy-Discord-Bot", "Final Data"), "Leaderboard.json"
        )
        leaderboard_data = load(open(file_path, "r"))
        length = len(leaderboard_data["bowling"][stats.value])
        total_pages = (length + GROUP - 1) // GROUP
        leader_name = leaderboard_data["bowling"][stats.value][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        # Function to generate embeds for pagination
        async def get_page(page: int):
            """
            Generates the leaderboard embed for a specific page.

            Parameters:
            - page: The page number to generate the leaderboard for.

            Returns:
            - emb: The leaderboard embed for the specified page.
            - total_pages: The total number of pages in the leaderboard.
            """
            # Parse Variables
            start = (page - 1) * GROUP
            end = min(start + GROUP, length)
            count = start + 1
            max_name_length = maxNameLength(
                leaderboard_data["bowling"][stats.value][start:end]
            )
            leaderboard_list = []

            for player in leaderboard_data["bowling"][stats.value][start:end]:
                # Parse Variables
                initial = player[::-1][0].split()[0][0]
                lastName = truncate_last_name(player[::-1][0].split()[-1])
                player_name = initial + ". " + lastName
                player_stat = str(player[::-1][1])
                player_rank = str(count) + ((3 - len(str(count))) * " ")
                extra_spaces = " " * (max_name_length - len(player_name) + 2)

                leaderboard_list.append(
                    f"{player_rank} {player_name}{extra_spaces}  {player_stat}\n"
                )
                count += 1

            # generate embeds
            emb = Embed(
                title=f"{stats.name.capitalize()} Leaderboard",
                colour=0xEC1C24,
                description=f"Page {page} of {total_pages}\n```"
                + "".join(leaderboard_list)
                + "```",
            )
            emb.set_author(
                name="IPL Fantasy",
                icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
            )
            emb.set_image(url=icon)
            emb.set_footer(text="Last Updated")
            file_path = path.join(
                path.join("/root/IPL-Fantasy-Discord-Bot", "Final Data"),
                "LastRefresedh.json",
            )
            emb.timestamp = datetime.fromtimestamp(load(open(file_path, "r"))["time"])

            return emb, total_pages

        await Pagination(interaction, get_page).navegate()

    @app_commands.command(
        name="batting",
        description="Displays the leaderboard for a specific batting statistic",
    )
    @app_commands.describe(stats="Statistics to choose from")
    @app_commands.choices(
        stats=[
            app_commands.Choice(name="Runs", value="runs"),
            app_commands.Choice(name="4s", value="4s"),
            app_commands.Choice(name="6s", value="6s"),
            app_commands.Choice(name="50s", value="50s"),
            app_commands.Choice(name="100s", value="100s"),
            app_commands.Choice(name="Ducks", value="0s"),
            app_commands.Choice(name="Batting Average", value="battingAverage"),
            app_commands.Choice(name="Batting Strike Rate", value="SR"),
        ]
    )
    async def batting(self, interaction, stats: app_commands.Choice[str]):
        """
        Displays the leaderboard for a specific batting statistic.

        Parameters:
        - interaction: The interaction object representing the user's interaction with the command.
        - stats: The batting statistic to display the leaderboard for.

        Returns:
        None
        """

        # Parse Variables
        file_path = path.join(
            path.join("/root/IPL-Fantasy-Discord-Bot", "Final Data"), "Leaderboard.json"
        )
        leaderboard_data = load(open(file_path, "r"))
        length = len(leaderboard_data["batting"][stats.value])
        total_pages = (length + GROUP - 1) // GROUP
        leader_name = leaderboard_data["batting"][stats.value][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        # Function to generate embeds for pagination
        async def get_page(page: int):
            """
            Generates the leaderboard embed for a specific page.

            Parameters:
            - page: The page number to generate the leaderboard for.

            Returns:
            - emb: The leaderboard embed for the specified page.
            - total_pages: The total number of pages in the leaderboard.
            """

            # Parse Variables
            start = (page - 1) * GROUP
            end = min(start + GROUP, length)
            count = start + 1
            max_name_length = maxNameLength(
                leaderboard_data["batting"][stats.value][start:end]
            )
            leaderboard_list = []

            for player in leaderboard_data["batting"][stats.value][start:end]:

                # Parse Variables
                initial = player[::-1][0].split()[0][0]
                lastName = truncate_last_name(player[::-1][0].split()[-1])
                player_name = initial + ". " + lastName
                player_stat = str(player[::-1][1])
                player_rank = str(count) + ((3 - len(str(count))) * " ")
                extra_spaces = " " * (max_name_length - len(player_name) + 2)

                leaderboard_list.append(
                    f"{player_rank} {player_name}{extra_spaces}  {player_stat}\n"
                )
                count += 1

            # generate embeds
            emb = Embed(
                title=f"{stats.name.capitalize()} Leaderboard",
                colour=0xEC1C24,
                description=f"Page {page} of {total_pages}\n```"
                + "".join(leaderboard_list)
                + "```",
            )
            emb.set_author(
                name="IPL Fantasy",
                icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
            )
            emb.set_thumbnail(url=icon)
            emb.set_footer(text="Last Updated")
            file_path = path.join(
                path.join("/root/IPL-Fantasy-Discord-Bot", "Final Data"),
                "LastRefresedh.json",
            )
            emb.timestamp = datetime.fromtimestamp(load(open(file_path, "r"))["time"])

            return emb, total_pages

        await Pagination(interaction, get_page).navegate()


async def setup(client):
    client.tree.add_command(
        LeaderboardGroup(
            name="leaderboard", description="player, statistic, and team leaderboards"
        )
    )
