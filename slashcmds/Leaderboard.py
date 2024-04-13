# import discord
from discord import app_commands, Embed
from datetime import datetime
from json import load


# TODO: add logging
# TODO: Deal with ties
# TODO: correct last updated time
# TODO: Add owner


class LeaderboardGroup(app_commands.Group):

    @app_commands.command(name="runs", description="Displays the runs leaderboard")
    async def runs(self, interaction, limit: int = 100):

        # Parse Variables
        leaderboard_data = load(open("Final Data\Leaderboard.json", "r"))
        lenght = len(leaderboard_data["batting"]["runs"])

        if limit < 0:
            start = lenght + limit
            end = lenght
        else:
            start = 0
            end = limit

        leader_name = leaderboard_data["batting"]["runs"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"
        max_name_length = max(
            len(player[::-1][0].split()[0][0] + player[::-1][0].split()[-1])
            for player in leaderboard_data["batting"]["runs"][start:end]
        )
        count = start + 1
        leaderboard_list = []

        for player in leaderboard_data["batting"]["runs"][start:end]:

            # Parse Variables
            initial = player[::-1][0].split()[0][0]
            lastName = player[::-1][0].split()[-1]
            player_name = initial + ". " + lastName
            player_runs = str(player[::-1][1])
            player_rank = str(count) + ")" + ((3 - len(str(count))) * " ")
            extra_spaces = " " * (max_name_length - len(player_name) + 2)

            leaderboard_list.append(
                f"{player_rank} {player_name}{extra_spaces}  {player_runs}\n"
            )
            count += 1

        # Create Embeds
        title_embed = Embed(
            title="Runs Leaderboard",
            colour=0xEC1C24,
            description=f"Showing top {limit} players",
        )
        title_embed.set_author(
            name="IPL Fantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        title_embed.set_thumbnail(url=icon)

        # Other Embeds
        embeds = []
        for i in range(0, len(leaderboard_list), 50):
            embed = Embed(
                colour=0xEC1C24,
                description="```" + "".join(leaderboard_list[i : i + 50]) + "```",
            )
            embeds.append(embed)

        # Send Embeds
        await interaction.response.send_message(embed=title_embed)
        for embed in embeds:
            await interaction.channel.send(embed=embed)

    @app_commands.command(name="help", description="displays the help message")
    async def help(self, interaction):
        embed = Embed(
            title="IPLFantasy Bot",
            description="A Discord bot that displays IPL statistics",
            colour=0x009688,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_footer(
            text="Vignesh Saravanakumar",
            icon_url="https://lh3.googleusercontent.com/a/ACg8ocKII8LPTqmYUAgEyzvcZCeAd1_sZKoj2giIvs8Zhw-Y9cyvolbt=s360-c-no",
        )

        embed.add_field(
            name="Commands",
            value="`/help` - displays this help message\n\n"
            "**Commands for batting statistics:**\n"
            "`/runs`\n"
            "`/0s`\n"
            "`/4s`\n"
            "`/6s`\n"
            "`/50s`\n"
            "`/100s`\n"
            "`/sr`\n"
            "`/batting-average`\n"
            "`/not-outs`\n"
            "`/high-score`\n\n"
            "**Commands for bowling statistics:**\n"
            "`/wickets`\n"
            "`/dots`\n"
            "`/4-wicket-haul`\n"
            "`/5-wicket-haul`\n"
            "`/6-wicket-haul`\n"
            "`/maiden`\n"
            "`/economy`\n"
            "`/bowling-average`\n"
            "`/bowling-strike-rate`\n"
            "`/overs`\n\n"
            "**Other commands:**\n"
            "`/player-of-the-match`",
            inline=False,
        )

        await interaction.response.send_message(embed=embed)


async def setup(client):
    client.tree.add_command(
        LeaderboardGroup(
            name="leaderboard", description="player, statistic, and team leaderboards"
        )
    )
