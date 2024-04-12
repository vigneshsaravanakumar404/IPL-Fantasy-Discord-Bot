import discord
import Constants
from discord import app_commands
from datetime import datetime


class UtilityGroup(app_commands.Group):

    @app_commands.command(name="ping", description="displays the bot's latency")
    async def ping(self, interaction):
        """
        Command to display the bot's latency.

        Parameters:
        - interaction: The interaction object representing the user's interaction with the bot.

        Returns:
        - None

        Side Effects:
        - Sends a message with the bot's latency to the user.
        - Sends an embed message with the bot's latency to the logs channel.

        """
        embed = discord.Embed(
            title=f"{discord.utils.escape_markdown(interaction.user.display_name)} Used /ping",
            color=discord.Color.gold(),
        )
        embed.set_author(
            name=interaction.user.display_name, icon_url=interaction.user.avatar.url
        )
        embed.add_field(
            name="Latency",
            value=f"{round(interaction.client.latency * 1000, 2)} ms",
            inline=False,
        )

        await interaction.response.send_message(
            f"{interaction.user.mention} Latency is {round(interaction.client.latency * 1000, 2)} ms",
            ephemeral=True,
        )
        await interaction.client.get_guild(Constants.IPL_FANTASY_SERVER).get_channel(
            Constants.LOGS_CHANNEL
        ).send(embed=embed)


async def setup(client):
    client.tree.add_command(
        UtilityGroup(name="utility", description="utlity and admin commands")
    )
