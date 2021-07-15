import discord
import random
import os
from keep_alive import keep_alive
from discord.ext import commands
import praw
import youtube_dl
import pytz

import asyncio
import time
import platform
from collections import Counter

intents = discord.Intents.all()
intents.members = True
intents.typing = True
intents.presences = True

client = commands.Bot(command_prefix="#", intents=intents)

# Bot Status


def local_datetime(datetime_obj):
    utcdatetime = datetime_obj.replace(tzinfo=pytz.utc)
    tz = "Africa/Nairobi"
    return utcdatetime.astimezone(pytz.timezone(tz))


__games__ = [
    (discord.ActivityType.playing, "with DisordAPI"),
    (discord.ActivityType.playing, "with PyCharm"),
    (discord.ActivityType.playing, "with Python"),
    (discord.ActivityType.playing, "Repl.it"),
    (discord.ActivityType.watching, "over {guilds} Server"),
    (discord.ActivityType.watching, "over {members} Members"),
    (discord.ActivityType.playing, "IntelliJ"),
    (discord.ActivityType.listening, "# commands"),
]
__gamesTimer__ = 60 * 60  # 60 minutes


@client.event
async def on_ready():
    print("Bot's Ready")
    while True:
        guildCount = len(client.guilds)
        memberCount = len(list(client.get_all_members()))
        randomGame = random.choice(__games__)
        await client.change_presence(
            activity=discord.Activity(
                type=randomGame[0],
                name=randomGame[1].format(guilds=guildCount, members=memberCount),
            )
        )
        await asyncio.sleep(__gamesTimer__)


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=10):
    await ctx.channel.purge(limit=amount)


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Members")
    await member.add_roles(role)


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 802462953319956480:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == "python":
            role = discord.utils.get(guild.roles, name="Python")

        elif payload.emoji.name == "cpp":
            role = discord.utils.get(guild.roles, name="C++")

        elif payload.emoji.name == "java":
            role = discord.utils.get(guild.roles, name="Java")

        elif payload.emoji.name == "js":
            role = discord.utils.get(guild.roles, name="js")

        elif payload.emoji.name == "rust":
            role = discord.utils.get(guild.roles, name="Rust")

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = guild.get_member(payload.user_id)
            if member:
                await member.add_roles(role)
                print("done")
            else:
                print("Member Not found.")
        else:
            print("Role not found.")


@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 802462953319956480:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == "python":
            role = discord.utils.get(guild.roles, name="Python")

        elif payload.emoji.name == "cpp":
            role = discord.utils.get(guild.roles, name="C++")

        elif payload.emoji.name == "java":
            role = discord.utils.get(guild.roles, name="Java")

        elif payload.emoji.name == "js":
            role = discord.utils.get(guild.roles, name="js")

        elif payload.emoji.name == "rust":
            role = discord.utils.get(guild.roles, name="Rust")

        else:
            role = discord.utils.get(guild.roles, name=payload.emoji.name)

        if role is not None:
            member = guild.get_member(payload.user_id)

            if member:
                await member.remove_roles(role)
                print("done")
            else:
                print("Member Not found.")
        else:
            print("Role not found.")


# Mod-Mail Functionality


@client.event
async def on_message(message):
    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(), name="mod-mail")

    if message.author == client.user:
        return
    if str(message.channel.type) == "private":
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send("[" + message.author.display_name + "]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            await modmail_channel.send(
                "[" + message.author.display_name + "] " + message.content
            )

    elif str(message.channel) == "mod-mail" and message.content.startswith("<"):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments
            await member_object.send("[" + message.author.display_name + "]")

            for file in files:
                await member_object.send(file.url)
        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]
            await member_object.send(
                "[" + message.author.display_name + "]" + mod_message
            )
    await client.process_commands(message)


# Hello Command


@client.command()
async def hello(ctx):
    async with ctx.typing():
        await ctx.send("Hello " + str(ctx.author.display_name) + ", What's up?")


# Who is Command
@client.command()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(
        title=member.name, description=member.mention, color=discord.Color.blue()
    )
    embed.add_field(
        name="Name and Tag",
        value="{}#{}".format(member.name, member.discriminator),
        inline=True,
    )
    embed.add_field(name="User ID", value=member.id, inline=True)
    embed.add_field(
        name="Account Creation Date",
        value=local_datetime(member.created_at).strftime(
            "%A, %B %d %Y @ %H:%M:%S %p %Z"
        ),
        inline=False,
    )
    embed.add_field(
        name="Joined Server On",
        value=local_datetime(member.joined_at).strftime(
            "%A, %B %d %Y @ %H:%M:%S %p %Z"
        ),
        inline=False,
    )
    embed.add_field(name="Are you Friends?", value=member.is_friend(), inline=True)

    all_activities = []
    spotify = None
    for activity in member.activities:
        activity_name = activity.name
        if "spotify" in activity_name.lower():
            spotify = activity
        all_activities.append(activity_name)
    activities = "\n".join(all_activities) if all_activities else None
    embed.add_field(name="Activities", value=activities, inline=True)

    if spotify:
        embed.add_field(
            name="Spotify", value=f"{spotify.artist} - {spotify.title}", inline=True
        )

    roles = sorted([role for role in member.roles], reverse=True)
    mentions = [str(role.mention) for role in roles]
    del roles
    embed.add_field(name="Top Role", value=member.top_role, inline=False)
    embed.add_field(name="Roles", value=" , ".join(mentions), inline=False)

    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}"
    )

    await ctx.send(embed=embed)


# Help Command to list all Commands


@client.command()
async def HELP(ctx):
    async with ctx.typing():
        embed = discord.Embed(
            title="Let's Code Bot Commands", color=discord.Color.blue()
        )
        embed.add_field(name="hello", value="Returns Hello back", inline=False)
        embed.add_field(name="ping", value="Returns Pong", inline=False)
        embed.add_field(
            name="tictactoe @player1 @player2",
            value="Starts a game of TicTacToe, For the player argument be sure to @ the players eg. @iamksm @kyande. This starts the game with the two people chosen",
            inline=False,
        )
        embed.add_field(
            name="place no. 1 - 9",
            value="On start of the TicTacToe game type place then no. between 1 to 9 to choose the box to place your mark. be sure to place on an empty space (Boxes are counted Horizontally 1 - 9)",
            inline=False,
        )
        embed.add_field(name="meme", value="Returns a Pic Meme", inline=False)
        embed.add_field(
            name="play",
            value="Plays a song from YouTube in the Lounge Channel, Takes abit of time to play so be patient",
            inline=False,
        )
        embed.add_field(
            name="stop", value="Stops the Currently playing song", inline=False
        )
        embed.add_field(name="whois", value="Returns details of a person", inline=False)
        embed.add_field(
            name="'leave' or 'dc'",
            value="Disconnects the bot from the channel",
            inline=False,
        )
        embed.add_field(
            name="server", value="Returns a description of the Server", inline=False
        )
        await ctx.send(embed=embed)


# Displays Server Info


@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    member_count = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Info", description=description, color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=False)
    embed.add_field(name="Member Count", value=member_count, inline=True)

    if ctx.guild.premium_subscribers:
        names = ctx.guild.premium_subscribers
        mentions = [str(name.mention) for name in names]
        del names

        embed.add_field(
            name="Current Server Boosters", value="\n".join(mentions), inline=False
        )

    embed.add_field(
        name="Server Creation Date",
        value=local_datetime(ctx.guild.created_at).strftime(
            "%A, %B %d %Y @ %H:%M:%S %p %Z"
        ),
        inline=False,
    )

    if ctx.guild.system_channel:
        embed.add_field(
            name="Standard Channel", value=f"#{ctx.guild.system_channel}", inline=True
        )
        embed.add_field(
            name="AFK Voice Timeout",
            value=f"{int(ctx.guild.afk_timeout / 60)} min",
            inline=True,
        )
        embed.add_field(name="Guild Shard", value=ctx.guild.shard_id, inline=True)

    roles = sorted([role for role in ctx.guild.roles], reverse=True)
    mentions = [str(role.mention) for role in roles]
    del roles

    embed.add_field(name="Roles in Server", value="\n".join(mentions), inline=True)

    if ctx.guild.emojis:
        emojis = ctx.guild.emojis
        the_emojis = [str(emoji.name) for emoji in emojis]
        del emojis

        embed.add_field(name="Custom Emojis", value="\n".join(the_emojis), inline=True)

    embed.set_footer(text="Bot by iamksm#8749")
    await ctx.send(embed=embed)


# Starting the TICTACTOE game

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winning_conditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    async with ctx.typing():
        global count
        global player1
        global player2
        global turn
        global gameOver

        if gameOver:
            global board
            board = [
                ":white_large_square:",
                ":white_large_square:",
                ":white_large_square:",
                ":white_large_square:",
                ":white_large_square:",
                ":white_large_square:",
                ":white_large_square:",
                ":white_large_square:",
                ":white_large_square:",
            ]
            turn = ""
            gameOver = False
            count = 0

            player1 = p1
            player2 = p2

            # print the board
            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x == 8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]

            # determine who goes first
            num = random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
            elif num == 2:
                turn = player2
                await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
        else:
            await ctx.send(
                "A game is already in progress! Finish it before starting a new one."
            )


# placing No.s in the TicTacToe game


@client.command()
async def place(ctx, pos: int):
    async with ctx.typing():
        global turn
        global player1
        global player2
        global board
        global count
        global gameOver

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":regional_indicator_x:"
                elif turn == player2:
                    mark = ":o2:"
                if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                    board[pos - 1] = mark
                    count += 1

                    # print the board
                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x == 8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    check_winner(winning_conditions, mark)
                    print(count)
                    if gameOver:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        gameOver = True
                        await ctx.send("It's a tie!")

                    # switch turns
                    if turn == player1:
                        turn = player2
                    elif turn == player2:
                        turn = player1
                else:
                    await ctx.send(
                        "Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile."
                    )
            else:
                await ctx.send("It is not your turn.")
        else:
            await ctx.send("Please start a new game using the #tictactoe command.")


# Check Winner
def check_winner(winning_conditions, mark):
    global gameOver
    for condition in winning_conditions:
        if (
            board[condition[0]] == mark
            and board[condition[1]] == mark
            and board[condition[2]] == mark
        ):
            gameOver = True


# Error Handling
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Please make sure to mention/ping players (ie. <@688534433879556134>)."
        )


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


# MEMES Commnds

reddit = praw.Reddit(
    client_id="fZ54pZawusMgtw",
    client_secret="fuil2JVHGGnjvMIqNDlhpufc6JSi_w",
    username="imkossam",
    password="r1r2l1l2",
    user_agent="letscodebot",
)


@client.command()
async def meme(ctx):
    async with ctx.typing():
        subreddit = reddit.subreddit("memes")
        all_subs = []
        top = subreddit.top(limit=50)

        for submission in top:
            all_subs.append(submission)
        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(title=name)
        embed.set_image(url=url)
        await ctx.send(embed=embed)


@client.command(aliases=["uptime", "up"])
async def status(ctx):
    """Info about the bot"""
    client.startTime = time.time()
    timeUp = time.time() - client.startTime
    hours = timeUp / 3600
    minutes = (timeUp / 60) % 60
    seconds = timeUp % 60

    client.commands_used = Counter()

    __version__ = "1.6.1"
    client.botVersion = __version__

    client.AppInfo = await client.application_info()
    admin = client.AppInfo.owner

    users = 0
    channel = 0
    if len(client.commands_used.items()):
        commandsChart = sorted(
            client.commands_used.items(), key=lambda t: t[1], reverse=False
        )
        topCommand = commandsChart.pop()
        commandsInfo = "{} (Top-Command: {} x {})".format(
            sum(client.commands_used.values()), topCommand[1], topCommand[0]
        )
    else:
        commandsInfo = str(sum(client.commands_used.values()))
    for guild in client.guilds:
        users += len(guild.members)
        channel += len(guild.channels)

    embed = discord.Embed(color=ctx.me.top_role.colour)
    embed.set_footer(text="Bot Created by iamksm#8749")
    embed.set_thumbnail(url=ctx.me.avatar_url)
    embed.add_field(name="Bot Admin", value=admin, inline=False)
    embed.add_field(
        name="Uptime",
        value="{0:.0f} Hours, {1:.0f} Minutes and {2:.0f} Seconds\n".format(
            hours, minutes, seconds
        ),
        inline=False,
    )
    embed.add_field(name="Observed users", value=users, inline=True)
    embed.add_field(name="Observed servers", value=len(client.guilds), inline=True)
    embed.add_field(name="Watched channel", value=channel, inline=True)
    embed.add_field(name="Commands executed", value=commandsInfo, inline=True)
    embed.add_field(name="Bot Version", value=client.botVersion, inline=True)
    embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
    embed.add_field(name="Python Version", value=platform.python_version(), inline=True)

    embed.add_field(
        name="Operating system",
        value=f"{platform.system()} {platform.release()} {platform.version()}",
        inline=False,
    )
    await ctx.send("**:information_source:** Information about this bot:", embed=embed)


@client.command()
async def ping(ctx):
    """Measure the Response Time"""
    ping = ctx.message
    pong = await ctx.send("**:ping_pong:** Pong!")
    delta = pong.created_at - ping.created_at
    delta = int(delta.total_seconds() * 1000)
    await pong.edit(
        content=f":ping_pong: Pong! ({delta} ms)\n*Discord WebSocket latency: {round(client.latency, 5)} ms*"
    )


@client.command(aliases=["activities"])
async def games(ctx, *scope):
    """Shows which games and how often are currently being played on the server"""
    games = Counter()
    for member in ctx.guild.members:
        for activity in member.activities:
            if not member.bot:
                if isinstance(activity, discord.Game):
                    games[str(activity)] += 1
                elif isinstance(activity, discord.Activity):
                    games[activity.name] += 1
    msg = ":chart: Games currently being played on this server\n"
    msg += "```js\n"
    msg += "{!s:40s}: {!s:>3s}\n".format("Name", "Number")
    chart = sorted(games.items(), key=lambda t: t[1], reverse=True)
    for index, (name, amount) in enumerate(chart):
        if len(msg) < 1950:
            msg += "{!s:40s}: {!s:>3s}\n".format(name, amount)
        else:
            amount = len(chart) - index
            msg += f"+ {amount} Others"
            break
    msg += "```"
    await ctx.send(msg)


keep_alive()
client.run(os.getenv("TOKEN"))
