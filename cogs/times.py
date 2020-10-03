from datetime import timedelta, timezone as tz, datetime as dt
from functools import partial

from utils import paginate_embed

import discord
from discord.ext import commands

cst = tz(timedelta(hours=-5))  # cst is 5h behind utc

start = dt.fromtimestamp(1601690400, tz=cst)  # 9pm vandy time oct 2 2020
end = dt.fromtimestamp(1601906400, tz=cst)  # 9am vandy time oct 4 2020

nash = partial(dt.now, tz=cst)  # gives current time in nashville, use instead of dt.now() for uniformity

# Oct 2-4, 2020
sched = {
    2: [
        ('4:30 pm', 'Team Matching - Glimpse Session', ''),
        ('6:00 pm', 'Opening Ceremony', 'https://www.twitch.tv/vandyhacks'),
        ('7:00 pm', 'Keynote Speaker - Authors of Swipe to Unlock: Business Strategy for Technologists',
         'https://vanderbilt.zoom.us/j/99212620856'),
        ('7:50 pm', 'Keynote Speaker - Jeffrey Rothschild', 'https://www.twitch.tv/vandyhacks'),
        ('8:30 pm', 'Team Matching - Glimpse Session', 'https://app.joinglimpse.com/room?key=FDC34E'),
        ('9:00 pm', 'Hacking begins', ''),
        ('9:00 pm', 'Full-Stack Workshop w/ Angular', 'https://youtu.be/peKt6tRog60'),
        ('9:00 pm', 'Google Cloud Tech Talk - Cloud Hero Workshop', 'https://youtu.be/lrEYwt9ZpyQ'),
        ('10:00 pm', 'Intro to Open Source Workshop', 'https://youtu.be/0fkE7Awceig'),
        ('11:00 pm', 'SlackBot Workshop', 'https://youtu.be/12lSoyqgSxw')
    ],
    3: [
        ('8:00 am', 'Neural Networks Workshop', 'https://youtu.be/Yue_yX5k-Hc'),
        ('9:00 am', 'React Native Workshop', 'https://youtu.be/e2JHoda3RZU'),
        ('10:00 am', 'Big Data Workshop', 'https://youtu.be/txRjZvOAMnc'),
        ('11:00 am', 'Google Cloud Workshop', 'https://youtu.be/D_H4vchrSn8'),
        ('1:00 pm', 'Sponsor Career Fair', ''),
        ('3:30 pm', 'Zoomba', 'https://vanderbilt.zoom.us/j/96037192950?pwd=RjhmUDVwTEV5QUNCbUc2SXZtZFlaQT09'),
        ('4:00 pm', 'Exploring Data-Driven Advocacy - The % Project', ''),
        ('4:30 pm', 'MLH Werewolf', ''),
        ('5:00 pm', 'Let\'s Bake Together!', ''),
        ('6:00 pm', 'MLH Capture The Flag', ''),
        ('6:30 pm', 'Keynote Speaker - Karl Mehta', 'https://www.twitch.tv/vandyhacks'),
        ('7:20 pm', 'Skribbl.io', ''),
        ('8:00 pm', 'Keynote Speaker - Shauna McIntyre', 'https://www.twitch.tv/vandyhacks'),
        ('9:00 pm', 'Typing Competition!', ''),
        ('10:30 pm', 'Guided meditation and mindfulness', ''),
        ('11:30 pm', 'How to solve a Rubik\'s cube?', ''),
    ],
    4: [
        ('8:30 am', 'Hacking Ends', ''),
        ('8:30 am', 'Make your Demo!', ''),
        ('8:30 am', 'How To Demo Workshop', ''),
        ('9:30 am', 'Finish your Demo!', ''),
        ('9:45 am', 'Skribbl.io', ''),
        ('10:30 am', 'Keynote Speaker - Thiago Olson', ''),
        ('10:30 am', 'Judging', ''),
        ('1:20 pm', 'Keynote Speaker - Jennison Asuncion', ''),
        ('3:00 pm', 'Closing Ceremony', ''),
    ]
}


def time_left(event):
    # returns string with duration composed
    diff = event - nash()
    d = diff.days
    h, m = divmod(diff.seconds, 3600)  # 3600 seconds in an hour
    m, s = divmod(m, 60)

    return (f"{d} day{'s' * bool(d - 1)}, " if d else "") \
           + (f"{h} hour{'s' * bool(h - 1)}, " if h else "") \
           + (f"{m} minute{'s' * bool(m - 1)} and " if m else "") \
           + f"{s} second{'s' * bool(s - 1)}"


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
            breakdown = "VandyHacks VII " \
                        + ("begins " if start > nash() else "ends ") \
                        + "in " + time_left(event) + " bb"

        await ctx.send(breakdown)

    @commands.command(name="schedule")
    async def schedule(self, ctx):
        embeds = []
        for day, events in sched.items():
            full_day = ["Friday", "Saturday", "Sunday"][day - 2]
            embed = discord.Embed(title="VandyHacks VII Schedule :scroll:",
                                  description=f"**{full_day}, Oct {day}** \nso much fun to be had :')",
                                  color=16761095)
            for num, event in enumerate(events):
                event_time, event_name, link = event
                # unapologetically use walrus operator
                if ((left := dt.strptime(f"2020 Oct {day} {event_time}", "%Y %b %d %I:%M %p").
                        replace(tzinfo=cst)) > nash()):
                    embed.add_field(name=f"{num + 1}. {event_name}",
                                    value=(f"in {time_left(left)}" + (f", [**link**]({link})" if link else '')),
                                    inline=False)

            embeds.append(embed)

        # TODO: split saturday into two embeds
        await paginate_embed(self.bot, ctx.channel, embeds)
