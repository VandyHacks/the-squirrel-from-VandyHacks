import os
from datetime import datetime as dt

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="vh ")

start = dt.fromtimestamp(1601690400)  # 9pm vandy time oct 2 2020
end = dt.fromtimestamp(1601906400)  # 9am vandy time oct 4 2020


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(name="you succeed uwu", type=3),
    )
    print(f"{bot.user.name} is running...")


@bot.command(name="time", aliases=["when"])
async def hack_times(ctx):
    if start > dt.now():
        diff = start - dt.now()  # hackathon yet to start
    else:
        diff = end - dt.now()  # hackathon started so give time till end

    d = diff.days
    h, m = divmod(diff.seconds, 3600)  # 3600 seconds in an hour
    m, s = divmod(m, 60)

    if dt.now() > end:
        breakdown = "bruh hackathon over what are you doing here"
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
        print(f"ctx.author embarked on the quest")
        await ctx.send("This is off the *record*, but we're really **digging** the website this year, are you? ;)")
    else:
        await ctx.send('quests in DMs only 👀')


@bot.command()
@commands.has_permissions(manage_messages=True)
async def yeet(ctx, amount=1):
    await ctx.channel.purge(limit=amount, before=ctx.message)
    await ctx.message.delete()

    
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {bot.latency * 1000:.03f}ms")


@bot.command()
async def github(ctx):
    await ctx.send("closed source for now bb")
    # await ctx.send("Catch! https://github.com/aadibajpai/vh-discord-bot")


bot.run(os.environ["DISCORD"])
