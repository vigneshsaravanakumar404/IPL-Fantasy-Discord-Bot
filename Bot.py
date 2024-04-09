from discord.ext import commands
from discord.ext import commands
from datetime import datetime
from colorama import Fore, Back, Style
from Constants import IPL_FANTASY_SERVER, LOGS_CHANNEL
from Private import TOKEN
from DataHandler import DataHandler
import discord


if __name__ == "__main__":

    # Initialize
    client = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    current_time = datetime.now()
    time_string = current_time.strftime("%H:%M:%S EST")
    prfx = (
        Back.LIGHTBLACK_EX
        + Fore.GREEN
        + time_string
        + Back.RESET
        + Fore.WHITE
        + Style.BRIGHT
        + " "
    )
    print(prfx + "Data loaded successfully!" + Fore.WHITE)

    # Events
    @client.event
    async def on_ready():

        # Pre Initialize
        print(prfx + "Initializing bot..." + Fore.WHITE)
        await client.change_presence(
            activity=discord.Game(f"Latency: {(client.latency * 1000):.3f} ms")
        )
        print(
            prfx
            + "Status set to: "
            + Fore.YELLOW
            + f"Latency: {(client.latency * 1000):.3f} ms"
            + Fore.WHITE
        )

        # Load Slash Command Extensions
        await client.load_extension("slashcmds.SlashPing")
        await client.load_extension("slashcmds.SlashSquad")

        # Initilalize Slash Commands
        await client.tree.sync(guild=client.get_guild(IPL_FANTASY_SERVER))
        await client.tree.sync()

        # Post Initialize
        print(
            prfx
            + "Bot initialized "
            + Fore.YELLOW
            + client.user.name
            + Fore.WHITE
            + " is ready!"
        )
        print(prfx + f"Latency: {(client.latency * 1000):.3f} ms")

        embed = discord.Embed(
            title=f"{client.user.name} is ready!", color=discord.Color.gold()
        )
        embed.set_author(name=client.user.display_name, icon_url=client.user.avatar.url)
        embed.add_field(
            name="Latency", value=f"{(client.latency * 1000):.3f} ms", inline=False
        )

        await client.get_guild(IPL_FANTASY_SERVER).get_channel(LOGS_CHANNEL).send(
            embed=embed
        )

    client.run(TOKEN)
