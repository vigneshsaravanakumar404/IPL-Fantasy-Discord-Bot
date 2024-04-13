from discord.ext import commands
from discord.ext import commands
from datetime import datetime
from colorama import Fore, Back, Style
from Constants import IPL_FANTASY_SERVER, LOGS_CHANNEL
from Private import TOKEN
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

    # Events
    @client.event
    async def on_ready():
        """
        Event handler function that is called when the bot is ready to start receiving events.
        It initializes the bot, sets its status, loads slash command extensions, initializes slash commands,
        and sends a notification to the logs channel indicating that the bot is ready.

        Parameters:
        None

        Returns:
        None
        """
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
        # await client.load_extension("slashcmds.Scorecard")
        await client.load_extension("slashcmds.Leaderboard")
        await client.load_extension("slashcmds.UtilityGroup")

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

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        elif "RCB" in message.content:
            await message.add_reaction("<:RCB:1228474812100513792>")
            await message.add_reaction("🟰")
            await message.add_reaction("🗑️")
        elif "MI" in message.content:
            await message.add_reaction("<:MI:1228474810292502609>")
        elif "CSK" in message.content:
            await message.add_reaction("<:CSK:1228474780047507496>")
        elif "KKR" in message.content:
            await message.add_reaction("<:KKR:1228474808438751312>")
        elif "DC" in message.content:
            await message.add_reaction("<:DC:1228474806752776223>")
        elif "GT" in message.content:
            await message.add_reaction("<:GT:1228474807532654712>")
        elif "LSG" in message.content:
            await message.add_reaction("<:LSG:1228474809424281661>")
        elif "PBKS" in message.content:
            await message.add_reaction("<:PBKS:1228474811232293067>")
        elif "RR" in message.content:
            await message.add_reaction("<:RR:1228474852181016648>")
        elif "SRH" in message.content:
            await message.add_reaction("<:SRH:1228474814407114854>")

    # TODO: add on_message_edit, on_message_delete,

    @client.event
    async def on_reaction_add(reaction, user):
        if user == client.user:
            return
        if reaction.emoji == "<:RCB:1228474812100513792>":
            await reaction.message.add_reaction("🟰")
            await reaction.message.add_reaction("🗑️")

    # TODO: add logging
    @client.event
    async def on_reaction_remove(reaction, user):
        if user == client.user:
            return
        if reaction.emoji == "<:RCB:1228474812100513792>":
            await reaction.message.remove_reaction("🟰", client.user)
            await reaction.message.remove_reaction("🗑️", client.user)

    @client.event
    async def on_error(event, *args, **kwargs):
        """
        Event handler function that is called when an error occurs during an event.

        Parameters:
        event (str): The event that caused the error.
        *args: The arguments passed to the event.
        **kwargs: The keyword arguments passed to the event.

        Returns:
        None
        """
        current_time = datetime.now()
        time_string = current_time.strftime("%H:%M:%S EST")
        prfx = (
            Back.LIGHTBLACK_EX
            + Fore.RED
            + time_string
            + Back.RESET
            + Fore.WHITE
            + Style.BRIGHT
            + " "
        )

        print(prfx + f"An error occurred in event {event}:")
        print(prfx + f"Args: {args}")
        print(prfx + f"Kwargs: {kwargs}")
        # TODO: Test + logging

    client.run(TOKEN)
