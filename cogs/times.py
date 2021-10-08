from datetime import timedelta, timezone as tz, datetime as dt
from functools import partial

from utils import paginate_embed

import discord
from discord.ext import commands
import requests
from datetime import datetime, timedelta
from dateutil import parser
from operator import itemgetter

"""
customise these initial few variables according to
your hackathon timezone and start/end times
"""

# hackathon time zone
cst = tz(timedelta(hours=-5))  # cst is 5h behind utc

# hackathon start and end times
start = dt.fromtimestamp(1633744800, tz=cst)  # 9pm cst oct 8 2021
end = dt.fromtimestamp(1633874400, tz=cst)  # 9am cst oct 4 2020

nash = partial(dt.now, tz=cst)  # gives current time in nashville, use instead of dt.now() for uniformity

# Oct 8-10, 2021
# event format is (event name, duration, formatted time, time (raw for sorting))

url = "https://apply.vandyhacks.org/api/manage/events/pull"

response = requests.request("GET", url)

data = response.json()


friday = []
saturday = []
sunday = []
for x in data:
    event = []
    event.append(x['name'])
    event.append("Duration: " + str(x['duration']) + " Minutes")
    today = parser.parse(x['startTimestamp'])
    today = (today - timedelta(hours=5))
    time = today.time().strftime("%I:%M %p") 
    event.append("Time: " + time + " CST")
    if (today.weekday() == 4):
        event.append(today)
        friday.append(event)
    elif (today.weekday() == 5):
        event.append(today)
        saturday.append(event)
    else:
        event.append(today)
        sunday.append(event)
        

friday = sorted(friday, key=itemgetter(3))
saturday = sorted(saturday, key=itemgetter(3))
sunday = sorted(sunday, key=itemgetter(3))


def time_left(event):
    # returns string with duration composed
    diff = event - nash()
    d = diff.days
    h, m = divmod(diff.seconds, 3600)  # 3600 seconds in an hour
    m, s = divmod(m, 60)

    return (
        (f"{d} day{'s' * bool(d - 1)}, " if d else "")
        + (f"{h} hour{'s' * bool(h - 1)}, " if h else "")
        + (f"{m} minute{'s' * bool(m - 1)} and " if m else "")
        + f"{s} second{'s' * bool(s - 1)}"
    )


class Times(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="when")
    async def hack_times(self, ctx):
        if start > nash():
            event = start  # hackathon yet to start
        else:
            event = end  # hackathon started so give time till end

        if nash() > end:
            breakdown = "hackathon over come back next year :))"
        else:
            # compose string accordingly
            breakdown = (
                "VandyHacks VIII " + ("begins " if start > nash() else "ends ") + "in " + time_left(event) + " bb"
            )

        await ctx.send(breakdown)

    @commands.command(name="schedule")
    async def schedule(self, ctx):
        embed=discord.Embed(title="Vandy Hacks VIII", description="Hackathon Schedule", color=0x566f8f)
        embed.set_thumbnail(url="https://vandyhacks.org/assets/logo.png")
        
        
        embed.add_field(name="> Friday", value="Event List", inline=False)
        for event in friday:
            embed.add_field(name=event[0], value=event[1] + " | " + event[2], inline=False)

        
        embed.add_field(name="> Saturday", value="Event List", inline=False)
        for event in saturday:
            embed.add_field(name=event[0], value=event[1] + " | " + event[2], inline=False)

        

        embed2=discord.Embed(color=0x566f8f)
        embed2.add_field(name="> Sunday", value="Event List", inline=False)
        for event in sunday:
            embed2.add_field(name=event[0], value=event[1] + " | " + event[2], inline=False)
        embed2.set_footer(text="fun fact: disneyland wait times are shorter than the randwich line")
        await ctx.send(embed=embed)
        await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Times(bot))
