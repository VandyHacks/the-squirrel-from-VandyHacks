from datetime import datetime as dt

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='vh ')

start = dt.fromtimestamp(1601614800)  # 12am vandy time oct 2 2020

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="you hack", type=3))
    print(f'{bot.user.name} is running...')


@bot.command(name="time", aliases=["start"])
async def hack_times(ctx):
    diff = start - dt.now()
    d = diff.days
    h, m = divmod(diff.seconds, 3600)  # 3600 seconds in an hour
    m, s = divmod(m, 60)
    # TODO: make it not add a part if it's 0
    ctx.send("VandyHacks VII begins in {f"{d} days, " if d else ''}{h} hours, {m} minutes and {s} seconds bb")


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {bot.latency * 1000:.03f}ms")


@bot.command()
async def github(ctx):
    await ctx.send("closed source for now bb")
    # await ctx.send("Catch! https://github.com/aadibajpai/vh-discord-bot")


bot.run(os.environ["DISCORD"])
