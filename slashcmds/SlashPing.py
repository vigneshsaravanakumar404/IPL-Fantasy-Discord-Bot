import discord
import Constants
from discord import app_commands
from DataHandler import DataHandler
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

    @app_commands.command(name="refresh", description="refreshes the data")
    async def refresh(self, interaction):
        """
        Command to refresh the data.

        Parameters:
        - interaction: The interaction object representing the user's interaction with the bot.

        Returns:
        - None

        Side Effects:
        - Refreshes the data.
        - Sends a message to the user indicating that the data has been refreshed.
        - Sends an embed message to the logs channel indicating that the data has been refreshed.

        """
        last_refreshed_time = DataHandler.last_refreshed_time
        current_time = datetime.now()
        time_difference = current_time - last_refreshed_time

        # Check if data was refreshed less than 5 minutes ago
        if time_difference.total_seconds() < 300:
            embed = discord.Embed(
                title=f"{discord.utils.escape_markdown(interaction.user.display_name)} Used /refresh",
                color=discord.Color.red(),
            )
            embed.set_author(
                name=interaction.user.display_name, icon_url=interaction.user.avatar.url
            )
            embed.add_field(
                name="Data Refresh Failed",
                value="Data was refreshed less than 5 minutes ago!",
                inline=False,
            )

            await interaction.response.send_message(
                f"{interaction.user.mention} Data was refreshed less than 5 minutes ago!",
                ephemeral=True,
            )
            await interaction.client.get_guild(
                Constants.IPL_FANTASY_SERVER
            ).get_channel(Constants.LOGS_CHANNEL).send(embed=embed)
        else:
            DataHandler.update_data()
            embed = discord.Embed(
                title=f"{discord.utils.escape_markdown(interaction.user.display_name)} Used /refresh",
                color=discord.Color.gold(),
            )
            embed.set_author(
                name=interaction.user.display_name, icon_url=interaction.user.avatar.url
            )
            embed.add_field(
                name="Data Refreshed",
                value="Data has been refreshed successfully!",
                inline=False,
            )

            await interaction.response.send_message(
                f"{interaction.user.mention} Data has been refreshed successfully!",
                ephemeral=True,
            )
            await interaction.client.get_guild(
                Constants.IPL_FANTASY_SERVER
            ).get_channel(Constants.LOGS_CHANNEL).send(embed=embed)


async def setup(client):
    client.tree.add_command(
        UtilityGroup(name="utility", description="utlity and admin commands")
    )
