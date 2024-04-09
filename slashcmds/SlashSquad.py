import discord
from discord import app_commands
from Constants import USER
from DataHandler import DataHandler
from pprint import pprint


class SquadGroup(app_commands.Group):
    """
    Represents a group of slash commands related to squads.

    Attributes:
        app_commands.Group: The base class for slash command groups.

    Methods:
        me: Displays the squad with points per player for the user.
    """

    @app_commands.command(
        name="me", description="displays your squad with points per player"
    )
    async def me(self, interaction):
        data = DataHandler.get_data()[0]

        embed = discord.Embed(
            title="Your Squad Leaderboard", color=discord.Color.green()
        )
        user_id = interaction.user.id
        user_name = USER.get(user_id, "Unknown User")

        squad_points = 0
        player_list = []

        for player, player_data in data.items():
            if "Owner" in player_data and player_data["Owner"] == user_name:
                squad_points += player_data["points"]
                player_list.append(player)

        player_list.sort(key=lambda x: data[x]["points"], reverse=True)

        if player_list:
            squad_info = "\n".join(
                [
                    f"{index + 1}. {data[player]['old_name']} - {data[player]['points']} points"
                    for index, player in enumerate(player_list)
                ]
            )
            embed.add_field(
                name=f"{user_name}'s Squad ({squad_points} points)",
                value=squad_info,
                inline=False,
            )
        else:
            embed.add_field(
                name="Your Squad",
                value="You don't have any players in your squad yet.",
                inline=False,
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(client):
    client.tree.add_command(SquadGroup(name="squad", description="squad commands"))
