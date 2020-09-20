from datetime import datetime as dt
from discord.ext import commands


start = dt.fromtimestamp(1601690400)  # 9pm vandy time oct 2 2020
end = dt.fromtimestamp(1601906400)  # 9am vandy time oct 4 2020


class Times(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="when", aliases=["time"])
    async def hack_times(self, ctx):
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
                        + (f"{d} day{'s' * bool(d - 1)}, " if d else "") \
                        + (f"{h} hour{'s' * bool(h - 1)}, " if h else "") \
                        + (f"{m} minute{'s' * bool(m - 1)} and " if m else "") \
                        + f"{s} second{'s' * bool(s - 1)} bb"

        await ctx.send(breakdown)

    @commands.command(name="schedule")
    async def schedule(self, ctx):
        # TODO
        pass
