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
end = dt.fromtimestamp(1633874400, tz=cst)  # 9am cst oct 10 2020

nash = partial(dt.now, tz=cst)  # gives current time in nashville, use instead of dt.now() for uniformity

# Oct 8-10, 2021

url = "https://apply.vandyhacks.org/api/manage/events/pull"

response = requests.request("GET", url)

data = response.json()

sched = {}
friday = []
saturday = []
sunday = []
for x in data:
    today = parser.parse(x['startTimestamp'])
    today = (today - timedelta(hours=5))
    time = today.time().strftime("%I:%M %p") 
    if ("https" in x['location']):
        eventTuple = (time, x['name'], x['location'])
    else:
        eventTuple = (time, x['name'], "")
    if (today.weekday() == 4):
        friday.append(eventTuple)
    elif (today.weekday() == 5):
        saturday.append(eventTuple)
    else:
        sunday.append(eventTuple)

friday = sorted(friday, key=itemgetter(0))
saturday = sorted(saturday, key=itemgetter(0))
sunday = sorted(sunday, key=itemgetter(0))

sched[8] = friday
sched[9] = saturday
sched[10] = sunday


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
                "VandyHacks VII " + ("begins " if start > nash() else "ends ") + "in " + time_left(event) + " bb"
            )

        await ctx.send(breakdown)

    @commands.command(name="schedule")
    async def schedule(self, ctx):
        embeds = []

        for day, events in sched.items():
            if day >= nash().day:
                full_day = ["Friday", "Saturday", "Sunday"][day - 8]  # 2 since that was the first day

                embed = discord.Embed(
                    title="VandyHacks VIII Schedule :scroll:",
                    description=f"**{full_day}, Oct {day}** \nso much fun to be had :')",
                    color=16761095,
                )

                for num, event in enumerate(events):
                    event_time, event_name, link = event
                    # unapologetically use walrus operator
                    if (
                        left := dt.strptime(f"2021 Oct {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
                    ) > nash():  # check if event hasn't already passed

                        embed.add_field(
                            name=f"{num + 1}. {event_name}",
                            value=(f"in {time_left(left)}" + (f", [**link**]({link})" if link else "")),
                            inline=False,
                        )

                embeds.append(embed)

        await paginate_embed(self.bot, ctx.channel, embeds)


def setup(bot):
    bot.add_cog(Times(bot))
