from datetime import timedelta, timezone as tz, datetime as dt
from functools import partial

from utils import paginate_embed

import discord
from discord.ext import commands
import requests
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

response = requests.get(url)

data = response.json()

friday = []
saturday = []
sunday = []

for event in data:
    today = parser.parse(event["startTimestamp"])
    today = today - timedelta(hours=5)
    time = today.time()
    if event["location"].startswith("https"):
        eventTuple = (time, event["name"], event["location"], event["duration"])
    else:
        eventTuple = (time, event["name"], "", event["duration"])
    if today.weekday() == 4:
        friday.append(eventTuple)
    elif today.weekday() == 5:
        saturday.append(eventTuple)
    else:
        sunday.append(eventTuple)

friday = sorted(friday, key=itemgetter(0))
saturday = sorted(saturday, key=itemgetter(0))
sunday = sorted(sunday, key=itemgetter(0))
friday = [(time.strftime("%I:%M %p"), name, loc, duration) for time, name, loc, duration in friday]
saturday = [(time.strftime("%I:%M %p"), name, loc, duration) for time, name, loc, duration in saturday]
sunday = [(time.strftime("%I:%M %p"), name, loc, duration) for time, name, loc, duration in sunday]

sched = {8: friday, 9: saturday, 10: sunday}


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
                    event_time, event_name, link, duration = event
                    # unapologetically use walrus operator
                    left = dt.strptime(f"2021 Oct {day} {event_time}", "%Y %b %d %I:%M %p").replace(tzinfo=cst)
                    if (
                        left + timedelta(minutes=duration) > nash()
                    ):  # check if event hasn't already passed or is happening
                        msg = "Happening now!" if left <= nash() else f"in {time_left(left)}"
                        embed.add_field(
                            name=f"{num + 1}. {event_name}",
                            value=(msg + (f", [**link**]({link})" if link else "")),
                            inline=False,
                        )

                embeds.append(embed)

        await paginate_embed(self.bot, ctx.channel, embeds)


def setup(bot):
    bot.add_cog(Times(bot))
