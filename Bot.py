from Constants import IPL_FANTASY_SERVER, LOGS_CHANNEL
from discord import Intents, Game, Embed, Color
from colorama import Fore, Back, Style
from discord.ext import commands, tasks
from datetime import datetime, time
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
        now = datetime.now()
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
        now = datetime.now()
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
        now = datetime.now()
        if time(18, 0) <= now.time() < time(19, 0):
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
        """
        Event handler for when a message is received.

        Parameters:
        - message (discord.Message): The message object received.

        Returns:
        - None
        """
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
        """
        Event handler for when a message is edited.

        Parameters:
        - before (discord.Message): The message before it was edited.
        - after (discord.Message): The message after it was edited.

        Returns:
        - None

        This function creates an embed with information about the edited message and sends it to a specified channel.
        It includes the author's display name, the content of the message before and after the edit, and the timestamps.
        If any attachments were edited, it also includes a list of the attachments.

        """
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
        """
        Event handler for when a message is deleted.

        Args:
            message (discord.Message): The deleted message object.

        Returns:
            None

        Raises:
            None
        """
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
        """
        Event handler for when a reaction is added to a message.

        Parameters:
        - reaction: The reaction that was added.
        - user: The user who added the reaction.

        Returns:
        - None

        Description:
        This function is called whenever a reaction is added to a message. It checks if the user who added the reaction is not the bot itself. If the reaction is the RCB emoji, it adds two more reactions to the message: 🟰 and 🗑️.
        """
        if user == client.user:
            return
        if reaction.emoji == "<:RCB:1228474812100513792>":
            await reaction.message.add_reaction("🟰")
            await reaction.message.add_reaction("🗑️")

    @client.event
    async def on_reaction_remove(reaction, user):
        """
        Event handler for when a reaction is removed from a message.

        Parameters:
        - reaction: The Reaction object representing the removed reaction.
        - user: The User object representing the user who removed the reaction.

        Returns:
        None

        """
        if user == client.user:
            return
        if reaction.emoji == "<:RCB:1228474812100513792>":
            await reaction.message.remove_reaction("🟰", client.user)
            await reaction.message.remove_reaction("🗑️", client.user)
        else:
            embed = Embed(title="Reaction Removed", color=Color.gold())
            embed.set_author(name=user.display_name, icon_url=user.avatar.url)
            embed.add_field(name="Emoji", value=reaction.emoji, inline=False)
            embed.add_field(
                name="Message", value=reaction.message.content, inline=False
            )

            await client.get_channel(LOGS_CHANNEL).send(embed=embed)

    @client.event
    async def on_error(event, *args, **kwargs):
        """
        Event handler for handling errors that occur in the client.

        Parameters:
        - event: The event where the error occurred.
        - args: Additional arguments passed to the event.
        - kwargs: Additional keyword arguments passed to the event.

        Prints the error details and sends an error message to a designated channel.

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

        embed = Embed(
            title="An error occurred",
            color=Color.red(),
            timestamp=datetime.now(),
        )
        embed.set_author(name="IPL Fantasy")
        embed.add_field(name="Event", value=event, inline=False)
        embed.add_field(name="Args", value=str(args), inline=False)
        embed.add_field(name="Kwargs", value=str(kwargs), inline=False)
        embed.add_field(name="Error", value=str(exc_info()), inline=False)
        embed.set_thumbnail(url=client.user.avatar.url)

        await client.get_guild(IPL_FANTASY_SERVER).get_channel(LOGS_CHANNEL).send(
            embed=embed
        )

    client.run(TOKEN)
