# import discord
from discord import app_commands, Embed
from datetime import datetime
from json import load

limit = 10

# TODO: Make stat leaderboards be the color of the leader's team
# TODO: add logging


# Batting: 6s, 0s, 50s, 100s, SR, battingAverage, NOs, HS
# Bowling: wickets, dots, 4H, 5H, 6H, maiden, economy, bowlingAverage, bSR, overs
# Fielding: playerOfTheMatch
class LeaderboardGroup(app_commands.Group):

    @app_commands.command(name="runs", description="displays the runs leaderboard")
    async def runs(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["runs"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Runs Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["runs"][:limit]]
        )
        player_runs = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["runs"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Runs", value=player_runs, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="4s", description="displays the 4s leaderboard")
    async def fours(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["4s"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="4s Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["4s"][:limit]]
        )
        player_fours = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["4s"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Fours", value=player_fours, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="6s", description="displays the 6s leaderboard")
    async def sixes(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["6s"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="6s Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["6s"][:limit]]
        )
        player_sixes = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["6s"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Sixes", value=player_sixes, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="50s", description="displays the 50s leaderboard")
    async def fifties(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["50s"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="50s Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["50s"][:limit]]
        )
        player_fifties = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["50s"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="50s", value=player_fifties, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="100s", description="displays the 100s leaderboard")
    async def hundreds(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["100s"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="100s Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["100s"][:limit]]
        )
        player_hundreds = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["100s"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="100s", value=player_hundreds, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sr", description="displays the strike rate leaderboard")
    async def strike_rate(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["SR"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Strike Rate Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["SR"][:limit]]
        )
        player_sr = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["SR"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Strike Rate", value=player_sr, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="batting-average", description="displays the batting average leaderboard"
    )
    async def batting_average(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["battingAverage"][0][1].replace(
            " ", "%20"
        )
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Batting Average Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [
                player[::-1][0]
                for player in leaderboard_data["batting"]["battingAverage"][:limit]
            ]
        )
        player_avg = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["battingAverage"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Batting Average", value=player_avg, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="not-outs", description="displays the not outs leaderboard"
    )
    async def not_outs(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["NOs"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Not Outs Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["NOs"][:limit]]
        )
        player_nos = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["NOs"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Not Outs", value=player_nos, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="high-score", description="displays the highest score leaderboard"
    )
    async def highest_score(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["batting"]["HS"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Highest Score Leaderboard",
            colour=0xEC1C24,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["batting"]["HS"][:limit]]
        )
        player_hs = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["batting"]["HS"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Highest Score", value=player_hs, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="wickets", description="displays the wickets leaderboard"
    )
    async def wickets(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["wickets"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Wickets Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [
                player[::-1][0]
                for player in leaderboard_data["bowling"]["wickets"][:limit]
            ]
        )
        player_wickets = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["wickets"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Wickets", value=player_wickets, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dots", description="displays the dots leaderboard")
    async def dots(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["dots"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Dots Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["bowling"]["dots"][:limit]]
        )
        player_dots = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["dots"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Dots", value=player_dots, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="4-wicket-haul", description="displays the 4 wickets leaderboard"
    )
    async def four_hauls(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["4H"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="4 Wickets Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["bowling"]["4H"][:limit]]
        )
        player_4h = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["4H"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="4 Wickets", value=player_4h, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="5-wicket-haul", description="displays the 5 wickets leaderboard"
    )
    async def five_hauls(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["5H"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="5 Wickets Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["bowling"]["5H"][:limit]]
        )
        player_5h = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["5H"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="5 Wickets", value=player_5h, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="6-wicket-haul", description="displays the 6 wickets leaderboard"
    )
    async def six_hauls(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["6H"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="6 Wickets Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["bowling"]["6H"][:limit]]
        )
        player_6h = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["6H"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="6 Wickets", value=player_6h, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="maiden", description="displays the maidens leaderboard")
    async def maidens(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["maiden"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Maidens Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [
                player[::-1][0]
                for player in leaderboard_data["bowling"]["maiden"][:limit]
            ]
        )
        player_maidens = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["maiden"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Maidens", value=player_maidens, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="economy", description="displays the economy leaderboard"
    )
    async def economy(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["economy"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Economy Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [
                player[::-1][0]
                for player in leaderboard_data["bowling"]["economy"][:limit]
            ]
        )
        player_economy = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["economy"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Economy", value=player_economy, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="bowling-average", description="displays the bowling average leaderboard"
    )
    async def bowling_average(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["bowlingAverage"][0][1].replace(
            " ", "%20"
        )
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Bowling Average Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [
                player[::-1][0]
                for player in leaderboard_data["bowling"]["bowlingAverage"][:limit]
            ]
        )
        player_avg = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["bowlingAverage"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Bowling Average", value=player_avg, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="bowling-strike-rate",
        description="displays the bowling strike rate leaderboard",
    )
    async def bowling_strike_rate(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["bSR"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Bowling Strike Rate Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["bowling"]["bSR"][:limit]]
        )
        player_bsr = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["bSR"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Bowling Strike Rate", value=player_bsr, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="overs", description="displays the overs leaderboard")
    async def overs(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["bowling"]["overs"][0][1].replace(" ", "%20")
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Overs Leaderboard",
            colour=0x004BA0,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [player[::-1][0] for player in leaderboard_data["bowling"]["overs"][:limit]]
        )
        player_overs = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["bowling"]["overs"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Overs", value=player_overs, inline=True)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(
        name="player-of-the-match",
        description="displays the player of the match leaderboard",
    )
    async def player_of_the_match(self, interaction):
        with open("Final Data\Leaderboard.json", "r") as f:
            leaderboard_data = load(f)

        leader_name = leaderboard_data["fielding"]["playerOfTheMatch"][0][1].replace(
            " ", "%20"
        )
        icon = f"https://scores.iplt20.com/ipl/playerimages/{leader_name}.png?v=4"

        embed = Embed(
            title="Player of the Match Leaderboard",
            colour=0x009688,
            timestamp=datetime.now(),
        )
        embed.set_author(
            name="IPLFantasy",
            icon_url="https://www.iplfantasycricket.com/static/media/Logo.72a128e06e97279fce9e.png",
        )
        embed.set_thumbnail(url=icon)
        embed.set_footer(
            text="Card Contents Refreshed",
            icon_url="https://assets-v2.lottiefiles.com/a/b60eaa18-118b-11ee-a837-7f9ff7261f26/PoxLPX9DzF.gif",
        )

        player_names = "\n".join(
            [
                player[::-1][0]
                for player in leaderboard_data["fielding"]["playerOfTheMatch"][:limit]
            ]
        )
        player_pom = "\n".join(
            [
                str(player[::-1][1])
                for player in leaderboard_data["fielding"]["playerOfTheMatch"][:limit]
            ]
        )

        embed.add_field(name="Player", value=player_names, inline=True)
        embed.add_field(name="Player of the Match", value=player_pom, inline=True)

        await interaction.response.send_message(embed=embed)


async def setup(client):
    client.tree.add_command(
        LeaderboardGroup(
            name="leaderboard", description="player, statistic, and team leaderboards"
        )
    )
