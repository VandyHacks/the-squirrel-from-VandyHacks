import os
from datetime import datetime as dt

import discord
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

bot = commands.Bot(command_prefix="vh ", help_command=None)

start = dt.fromtimestamp(1601690400)  # 9pm vandy time oct 2 2020
end = dt.fromtimestamp(1601906400)  # 9am vandy time oct 4 2020

ques = ["```bf\n"
        "----[-->+++++<]>.++[->+++<]>.-[----->+<]>.--[->+++<]>+.[-->+<]>---.+[--->++<]>-.[->+++<]>-.-----.+++++++++++++"
        ".-------.[--->+<]>-.+[->+++<]>.+++++++.-------------.+++++++++++++.+.------------.++++++++++++++.+[----->++<]>"
        "-.[--->+<]>--.----.+++..+++++++.[->+++++<]>++.[--->+<]>--.++++[->+++<]>.+++++++++.++.[----->++<]>+.++++++++.>-"
        "-[-->+++<]>.\n```",
        "This is off the *record*, but we're really **digging** the website this year. Are you? ;)"]


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("missing perms, get gud kid")


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(name="you succeed uwu", type=3),
    )
    print(f"{bot.user.name} is running...")


@bot.command(name="when", aliases=["time"])
async def hack_times(ctx):
    if start > dt.now():
        diff = start - dt.now()  # hackathon yet to start
    else:
        diff = end - dt.now()  # hackathon started so give time till end

    d = diff.days
    h, m = divmod(diff.seconds, 3600)  # 3600 seconds in an hour
    m, s = divmod(m, 60)

    if dt.now() > end:
        breakdown = "hackathon over come back next year :))"
    else:
        # compose string accordingly
        breakdown = "VandyHacks VII " \
                    + ("begins " if start > dt.now() else "ends ") + "in " \
                    + (f"{d} day{'s' * bool(d-1)}, " if d else "") \
                    + (f"{h} hour{'s' * bool(h-1)}, " if h else "") \
                    + (f"{m} minute{'s' * bool(m-1)} and " if m else "") \
                    + f"{s} second{'s' * bool(s-1)} bb"

    await ctx.send(breakdown)


@bot.command()
async def quest(ctx):
    # check if DMs
    if not ctx.guild:
        # remove this later when going to prod or swap out to the official server
        if ctx.author in bot.get_guild(424321814152347679).members:  # vandyhaxxx
            print(f"{ctx.author} embarked on the quest")
            await ctx.send(ques[0])
        else:
            print(f"{ctx.author} failed the vibe check")
            await ctx.send("you failed the vibe check, no quest for you")
    else:
        await ctx.send('quests in DMs only 👀')


@bot.command()
async def feedback(ctx):
    """
    anonymous feedback command, shares stuff to pvt channel
    """
    feedback_channel = bot.get_channel(752297941468708946)  # appropriate

    def check(m):  # check if author same and in DMs
        return m.author == ctx.author and m.channel.type == discord.ChannelType.private

    if ctx.author in bot.get_guild(424321814152347679).members:  # vandyhaxxx
        print(f"{ctx.author} is giving feedback")
        await ctx.author.send("please send you anonymous feedback bb, it will be directly shared with the organizers!")
        feedback = await bot.wait_for('message', check=check)
        await feedback_channel.send(f"there's new feedback\n> {feedback}")
    else:
        print(f"{ctx.author} failed the vibe check")
        await ctx.send("you failed the vibe check, no quest for you")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def yeet(ctx, amount=1):
    await ctx.channel.purge(limit=amount, before=ctx.message)
    await ctx.message.delete()

    
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {bot.latency * 1000:.03f}ms")


@bot.command(name="github", aliases=["gh"])
async def github(ctx):
    await ctx.send("closed source for now bb")  # potentially abstract stuff away and make this open sourceable?
    # await ctx.send("Catch! https://github.com/aadibajpai/vh-discord-bot")


@bot.command()
async def lewd(ctx):
    await ctx.send("<:lewd:748915128824627340>")  # easter egg?
    await ctx.message.delete()


@bot.command(name="help")
async def help_message(ctx):
    """
    Sends help message
    """

    embed = discord.Embed(title="the squirrel from VandyHacks", description="Here are the commands you can use:",
                          color=16761095)

    embed.add_field(name="`vh when` or `vh time`", value='Time until VH VII begins!', inline=False)
    embed.add_field(name="`vh quest`", value="slide into DMs with this :eyes:", inline=False)
    embed.add_field(name="`vh feedback`", value="send anonymous feedback :wink:", inline=False)
    embed.add_field(name="`vh help`", value="Show this message", inline=False)
    embed.add_field(name="`vh github` or `vh gh`", value="Link to the bot's source code", inline=False)
    embed.add_field(name="`vh ping`", value="Check bot latency", inline=False)
    embed.set_footer(text="think of something fun to put here")

    await ctx.send(embed=embed)


bot.run(os.environ["DISCORD"])
