from Constants import IPL_FANTASY_SERVER, LOGS_CHANNEL
from discord import Intents, Game, Embed, Color
from colorama import Fore, Back, Style
from discord.ext import commands, tasks
from datetime import datetime
from os import system, name
from Private import TOKEN
from Update import Update
from sys import exc_info

if __name__ == "__main__":

    # Initialize
    system("cls" if name == "nt" else "clear")
    client = commands.Bot(command_prefix="!", intents=Intents.all())
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

    # Async Tasks
    @tasks.loop(seconds=60)
    async def update_ping():
        """
        A task that updates the bot's presence with the current latency.

        This task runs every 60 seconds and updates the bot's presence with the current latency.
        The latency is displayed in milliseconds and rounded to 3 decimal places.

        Parameters:
            None

        Returns:
            None
        """
        await client.change_presence(
            activity=Game(f"Latency: {(client.latency * 1000):.3f} ms")
        )

    @tasks.loop(minutes=10)
    async def update_live_match():
        """
        A task that runs every 10 minutes to check if it's a weekday between 10:10 AM and 2:00 PM.
        If the conditions are met, it calls the Update() function.
        """
        now = datetime.datetime.now()
        if (
            now.weekday() < 5
            and now.time() >= datetime.time(10, 10)
            and now.time() <= datetime.time(14, 0)
        ):

            await client.get_guild(IPL_FANTASY_SERVER).get_channel(LOGS_CHANNEL).send(
                embed=Update()
            )

    @tasks.loop(minutes=20)
    async def update__live_match_sunday():
        """
        A task that runs every 20 minutes to check if it's a Sunday between 6:00 AM and 2:00 PM.
        If the conditions are met, it calls the Update() function.
        """
        now = datetime.datetime.now()
        if (
            now.weekday() == 6  # Sunday
            and now.time() >= datetime.time(6, 0)
            and now.time() <= datetime.time(14, 0)
        ):
            await client.get_guild(IPL_FANTASY_SERVER).get_channel(LOGS_CHANNEL).send(
                embed=Update()
            )

    @tasks.loop(hours=1)
    async def update_series():
        """
        A task that runs every hour and checks if it's between 6 PM and 7 PM.
        If it is, it calls the Update function with the updateSeries parameter set to True.
        """
        now = datetime.datetime.now()
        if datetime.time(18, 0) <= now.time() < datetime.time(19, 0):
            await client.get_guild(IPL_FANTASY_SERVER).get_channel(LOGS_CHANNEL).send(
                embed=Update()
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
            activity=Game(f"Latency: {(client.latency * 1000):.3f} ms")
        )
        print(
            prfx
            + "Status set to: "
            + Fore.YELLOW
            + f"Latency: {(client.latency * 1000):.3f} ms"
            + Fore.WHITE
        )

        # Load Async Tasks
        update_ping.start()
        update_live_match.start()
        update_series.start()
        update__live_match_sunday.start()

        # Load Slash Commands
        # await client.load_extension("slashcmds.Scorecard")
        await client.load_extension("slashcmds.Leaderboard")
        await client.load_extension("slashcmds.UtilityGroup")
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

        embed = Embed(title=f"{client.user.name} is ready!", color=Color.gold())
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

    @client.event
    async def on_message_edit(before, after):

        embed = Embed(title="Message Edited", color=Color.gold())
        embed.set_author(
            name=after.author.display_name, icon_url=after.author.avatar.url
        )
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)
        embed.set_footer(
            text=f"Edited at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            icon_url=client.user.avatar.url,
        )

        before_attachments = [attachment.url for attachment in before.attachments]
        after_attachments = [attachment.url for attachment in after.attachments]
        if before_attachments != after_attachments:
            embed.add_field(
                name="Attachments Edited",
                value="\n".join(
                    [f"- {attachment}" for attachment in before_attachments]
                ),
                inline=False,
            )

        await client.get_channel(LOGS_CHANNEL).send(embed=embed)

    @client.event
    async def on_message_delete(message):

        embed = Embed(title="Message Deleted", color=Color.gold())
        embed.set_author(
            name=message.author.display_name, icon_url=message.author.avatar.url
        )
        embed.add_field(name="Content", value=message.content, inline=False)
        embed.set_footer(
            text=f"Deleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            icon_url=client.user.avatar.url,
        )

        attachments = [attachment.url for attachment in message.attachments]
        if attachments:
            embed.add_field(
                name="Attachments Deleted",
                value="\n".join([f"- {attachment}" for attachment in attachments]),
                inline=False,
            )

        await client.get_channel(LOGS_CHANNEL).send(embed=embed)

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
        print(prfx + f"Error: {exc_info()}")
        # TODO: Test + logging

    client.run(TOKEN)
