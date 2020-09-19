import os
from asyncio import TimeoutError
from datetime import datetime as dt

from database import get_quest_level, update_quest_level, make_hacker_profile

import discord
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

bot = commands.Bot(command_prefix="vh ", help_command=None)

VHVII = 755112297772351499  # vh vii server guild id

start = dt.fromtimestamp(1601690400)  # 9pm vandy time oct 2 2020
end = dt.fromtimestamp(1601906400)  # 9am vandy time oct 4 2020


# list of pairwise challenge-flags
ques = [("```bf\n"
         "----[-->+++++<]>.++[->+++<]>.-[----->+<]>.[->+++++<]>+.+++++++.+++.----.[--->+<]>-.[->+++++<]>++.+++++++++++."
         "---------.+[-->+<]>.+++++[->++<]>.-------------.+++.+++++++++++++.-.---.>--[-->+++<]>.\n"
         "```", "vh{horny_ja1l_bonk}"),
        ("This is off the *record*, but we're really **digging** the website this year. Are you? ;)", "vh{<tbd>}")]


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


@bot.event
async def on_member_join(member):
    # create entries as people join to stagger load
    await make_hacker_profile([member])


@bot.event
async def on_guild_join(guild):
    await make_hacker_profile(guild.members)


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
                    + (f"{d} day{'s' * bool(d - 1)}, " if d else "") \
                    + (f"{h} hour{'s' * bool(h - 1)}, " if h else "") \
                    + (f"{m} minute{'s' * bool(m - 1)} and " if m else "") \
                    + f"{s} second{'s' * bool(s - 1)} bb"

    await ctx.send(breakdown)


@bot.command()
async def quest(ctx):

    def check(m):  # check if author same and in DMs
        return m.author == ctx.author and m.channel.type == discord.ChannelType.private

    # check if DMs
    if ctx.guild:
        return await ctx.send('quests in DMs only 👀')

    # swapped out to the official server
    if ctx.author in bot.get_guild(VHVII).members:
        print(f"{ctx.author} embarked on the quest")
        try:
            chall, flag = ques[await get_quest_level(ctx.author)]
            await ctx.send(chall)
            await ctx.send("send your answer in the next line")
            try:
                answer = await bot.wait_for('message', check=check, timeout=60)
                if answer.content == flag:
                    await ctx.send("ggwp bb")
                    print("someone answered correctly")
                    await update_quest_level(ctx.author)
                    await quest(ctx)  # send next level
                else:
                    await ctx.send("nah, try harder")
            except TimeoutError:
                print("someone did not reply")
                await ctx.author.send("feel free to come back anytime lolz")
        except IndexError:
            await ctx.send("congratulations you completed our quest ez")
    else:
        print(f"{ctx.author} failed the vibe check")
        await ctx.send("you failed the vibe check, no quest for you")


@bot.command()
async def feedback(ctx):
    """
    anonymous feedback command, shares stuff to pvt channel
    """
    feedback_channel = bot.get_channel(755968512362676284)  # anon-feedback in official vh discord

    def check(m):  # check if author same and in DMs
        return m.author == ctx.author and m.channel.type == discord.ChannelType.private

    if ctx.author in bot.get_guild(VHVII).members:
        print("someone is giving feedback")
        await ctx.author.send("please send your anonymous feedback in the next message, "
                              "it will be directly shared with the organizers! :yellow_heart:")
        try:
            feedback_resp = await bot.wait_for('message', check=check, timeout=60)
            await feedback_channel.send(f"there's new feedback!\n>>> {feedback_resp.content}")
            print("someone successfully gave feedback")
        except TimeoutError:
            print("someone did not reply")
            await ctx.author.send("oh well good talk nonetheless :)")

    else:
        print(f"{ctx.author} failed the vibe check")
        await ctx.send("you failed the vibe check, no quest for you")


@bot.command(name="yeet", aliases=["y"])
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


@bot.command(name="help")
async def help_message(ctx):
    """
    Sends help message
    """

    embed = discord.Embed(title="the squirrel from VandyHacks", description="Here are the commands you can use:",
                          color=16761095)

    embed.add_field(name="`vh when` or `vh time`", value='Time until VH VII begins!', inline=False)
    embed.add_field(name="`vh quest`", value="slide into DMs with this :eyes:", inline=False)
    embed.add_field(name="`vh feedback`", value="send anonymous feedback", inline=False)
    embed.add_field(name="`vh help`", value="Show this message", inline=False)
    embed.add_field(name="`vh github` or `vh gh`", value="Link to the bot's source code", inline=False)
    embed.add_field(name="`vh ping`", value="Check bot latency", inline=False)
    embed.set_footer(text="think of something fun to put here")

    await ctx.send(embed=embed)


bot.run(os.environ["DISCORD"])
