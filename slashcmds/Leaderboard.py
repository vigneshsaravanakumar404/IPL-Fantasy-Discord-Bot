# import discord
from Pagination import Pagination
from discord import app_commands, Embed
from datetime import datetime
from json import load


# TODO: add logging
# TODO: Deal with ties
# TODO: correct last updated time
# TODO: Add owner


class LeaderboardGroup(app_commands.Group):

    @app_commands.command(name="runs", description="Displays the runs leaderboard")
    async def runs(self, interaction):
        # Parse Variables
        leaderboard_data = load(open("Final Data\Leaderboard.json", "r"))
        length = len(leaderboard_data["batting"]["runs"])

        group = 10
        total_pages = (length + group - 1) // group
        leader_name = leaderboard_data["batting"]["runs"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        # Function to generate embeds for pagination
        async def get_page(page: int):
            emb = Embed(
                title="Runs Leaderboard",
                colour=0xEC1C24,
                description=f"Page {page} of {total_pages}",
            )

            start_index = (page - 1) * group
            end_index = min(start_index + group, length)

            emb.add_field(
                name="Rank",
                value="\n".join(str(i + 1) for i in range(start_index, end_index)),
                inline=True,
            )
            emb.add_field(
                name="Player",
                value="\n".join(
                    leaderboard_data["batting"]["runs"][i][1]
                    for i in range(start_index, end_index)
                ),
                inline=True,
            )
            emb.add_field(
                name="Runs",
                value="\n".join(
                    str(leaderboard_data["batting"]["runs"][i][0])
                    for i in range(start_index, end_index)
                ),
            )

            emb.set_author(
                name="IPL Fantasy",
                icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
            )
            # emb.set_thumbnail(url=icon)
            emb.set_footer(text="Last Updated")
            with open("Final Data\LastRefresedh.json", "r") as f:
                emb.timestamp = datetime.fromtimestamp(load(f)["time"])

            return emb, total_pages

        # Create Pagination view and navigate
        await Pagination(interaction, get_page).navegate()

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
