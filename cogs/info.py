import time
from datetime import timedelta

import discord
import psutil
from discord.ext import commands

process = psutil.Process()
init_cpu_time = process.cpu_percent()


class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats")
    async def view_stats(self, ctx):
        """
        Returns bot statistics and technical data.
        """
        app_info = await self.bot.application_info()
        total_ram = (psutil.virtual_memory().total >> 30) + 1
        embed = discord.Embed(
            title="the squirrel from VandyHacks Bot Stats",
            description=f"Running on a dedicated server with {total_ram}GB RAM.",
            color=16761095)

        embed.add_field(name="Latency", value=f"{self.bot.latency*1000:.03f}ms", inline=False)

        embed.add_field(name='"technical" info', value="random values or something idk I'm not DevOps", inline=False)
        embed.add_field(name="System CPU Usage", value=f"{psutil.cpu_percent():.02f}%")
        embed.add_field(name="System RAM Usage",
                        value=f"{psutil.virtual_memory().used/1048576:.02f} MB")
        embed.add_field(name="System Uptime",
                        value=f'{timedelta(seconds=int(time.time() - psutil.boot_time()))}')
        embed.add_field(name="Bot CPU Usage", value=f"{process.cpu_percent():.02f}%")
        embed.add_field(name="Bot RAM Usage", value=f"{process.memory_info().rss / 1048576:.02f} MB")
        embed.add_field(name="Bot Uptime",
                        value=f'{timedelta(seconds=int(time.time() - process.create_time()))}')

        embed.add_field(name=":bulb::link:", value="now some thought provoking links", inline=False)
        embed.add_field(name="Cool Website", value="vandyhacks.org](https://vandyhacks.org)")
        embed.add_field(name="Another Cool Website", value="[apply.vandyhacks.org]"
                                                           "(https://apply.vandyhacks.org)")
        embed.add_field(name="Source of Cool Websites", value="[github.com/VandyHacks]"
                                                              "(https://github.com/VandyHacks)")

        embed.set_footer(text="think of something cool to write here")

        await ctx.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, ctx):
        """
        Checks bot latency.
        """
        await ctx.send(f"Pong! {self.bot.latency * 1000:.03f}ms")

    @commands.command(name="github", aliases=["gh"])
    async def github(self, ctx):
        await ctx.send("closed source for now bb")  # potentially abstract stuff away and make this open sourceable?
        # await ctx.send("Catch! https://github.com/VandyHacks/the-squirrel-from-VandyHacks")
