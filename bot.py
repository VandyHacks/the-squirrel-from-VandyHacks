import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='vh ')


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name="you hack", type=3))
    print(f'{bot.user.name} is running...')


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {bot.latency * 1000:.03f}ms")


@bot.command()
async def github(ctx):
    await ctx.send("closed source for now bb")
    # await ctx.send("Catch! https://github.com/aadibajpai/vh-discord-bot")


bot.run(os.environ["DISCORD_TOKEN"])
