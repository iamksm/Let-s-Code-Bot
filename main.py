import discord
import random
import os
from keep_alive import keep_alive
from discord.ext import commands
import praw

client = commands.Bot(command_prefix="#")

#Bot Status

@client.event
async def on_ready():
    # game = discord.Game("#HELP")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening, name="#HELP"))
    print("Bot's Ready")

    #Loads the Music Commands from the cog directory
    client.load_extension('cogs.music')

#Mod-Mail Functionality

@client.event
async def on_message(message):
    empty_array = []
    modmail_channel = discord.utils.get(
        client.get_all_channels(), name="mod-mail")

    if message.author == client.user:
        return
    if str(message.channel.type) == "private":
        if message.attachments != empty_array:
            files = message.attachments
            await modmail_channel.send("[" + message.author.display_name + "]")

            for file in files:
                await modmail_channel.send(file.url)
        else:
            await modmail_channel.send("[" + message.author.display_name +
                                       "] " + message.content)

    elif str(
            message.channel) == "mod-mail" and message.content.startswith("<"):
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
            await member_object.send("[" + message.author.display_name + "]" +
                                     mod_message)
    await client.process_commands(message)

#Hello Command

@client.command()
async def hello(ctx):
    await ctx.send("Hello " + str(ctx.author.display_name) + ", What's up?")


@client.command()
async def ping(ctx):
    if str(ctx.author) != "iamksm#8749":
        await ctx.send("Pong!")
    else:
        await ctx.send("Pong!")

#Who is Command

@client.command()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(
        title=member.name,
        description=member.mention,
        color=discord.Color.blue())
    embed.add_field(name="ID", value=member, inline=True)
    # embed.add_field(name = "Top Role" , value = member.roles, inline = True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(
        icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

#Help Command to list all Commands

@client.command()
async def HELP(ctx):
    embed = discord.Embed(
        title="Let's Code Bot Commands", color=discord.Color.blue())
    embed.add_field(name="hello", value="Returns Hello back", inline=False)
    embed.add_field(name="ping", value="Returns Pong", inline=False)
    embed.add_field(
        name="tictactoe @player1 @player2",
        value=
        "Starts a game of TicTacToe, For the player argument be sure to @ the players eg. @iamksm @kyande. This starts the game with the two people chosen",
        inline=False)
    embed.add_field(
        name="place no. 1 - 9",
        value=
        "On start of the TicTacToe game type place then no. between 1 to 9 to choose the box to place your mark. be sure to place on an empty space (Boxes are counted Horizontally 1 - 9)",
        inline=False)
    embed.add_field(name="memes", value="Returns a Pic Meme", inline=False)
    embed.add_field(
        name="play",
        value=
        "Plays a song from YouTube in the Lounge Channel, Takes abit of time to play so be patient",
        inline=False)
    embed.add_field(
        name="stop", value="Stops the Currently playing song", inline=False)
    embed.add_field(
        name="whois", value="Returns details of a person", inline=False)
    embed.add_field(
        name="'leave' or 'dc'",
        value="Disconnects the bot from the channel",
        inline=False)
    embed.add_field(
        name="server", value="Returns a description of the Server", inline=False)
    await ctx.send(embed=embed)


#Displays Server Info

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
        title=name + " Server Info",
        description=description,
        color=discord.Color.blue())
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=member_count, inline=True)
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
    [2, 4, 6]
]


@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
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
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

#placing No.s in the TicTacToe game

@client.command()
async def place(ctx, pos: int):
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
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the #tictactoe command.")

#Check Winner
def check_winner(winning_conditions, mark):
    global gameOver
    for condition in winning_conditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

#Error Handling
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


#MEMES Commnds

reddit = praw.Reddit(
    client_id="fZ54pZawusMgtw",
    client_secret="fuil2JVHGGnjvMIqNDlhpufc6JSi_w",
    username="imkossam",
    password="r1r2l1l2",
    user_agent="letscodebot")


@client.command()
async def memes(ctx):
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


  

keep_alive()
client.run(os.getenv('TOKEN'))
