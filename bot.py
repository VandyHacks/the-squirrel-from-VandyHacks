import os
from asyncio import TimeoutError

from cogs.info import Info
from cogs.quest import Quest
from cogs.times import Times
from database import make_hacker_profile, init_pats

import discord
from discord.ext import commands
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

bot = commands.Bot(command_prefix=["vh ", "vH ", "Vh ", "VH "], case_insensitive=True, help_command=None)

VHVII = 755112297772351499  # vh vii server guild id


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("missing perms, get gud kid")


@bot.event
async def on_ready():
    # create pat counter if not already
    await init_pats()
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(name="you succeed uwu | vh help", type=3),
    )
    print(f"{bot.user.name} is running...")


@bot.event
async def on_member_join(member):
    # create entries as people join to stagger load
    await make_hacker_profile([member])


@bot.event
async def on_guild_join(guild):
    await make_hacker_profile(guild.members)


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
        await ctx.author.send(
            "please send your anonymous feedback in the next message, "
            "it will be directly shared with the organizers! :yellow_heart:"
        )
        await ctx.author.send("or send q to quit feedback submission.")
        try:
            feedback_resp = await bot.wait_for("message", check=check, timeout=60)
            if feedback_resp.content == "q":
                return await ctx.author.send("cool beans")
            await feedback_channel.send(f"there's new feedback!\n>>> {feedback_resp.content}")
            print("someone successfully gave feedback")
            await ctx.author.send("successfully sent your feedback!")
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
async def lewd(ctx):
    await ctx.send("<:lewd:748915128824627340>")  # easter egg?


@bot.command(name="help")
async def help_message(ctx):
    """
    Sends help message
    """

    embed = discord.Embed(
        title="the squirrel from VandyHacks", description="Here are the commands you can use:", color=16761095
    )

    embed.add_field(name="`vh when`", value="Time until VH VII ends!", inline=False)
    embed.add_field(name="`vh schedule`", value="interactive events schedule :calendar_spiral:", inline=False)
    embed.add_field(name="`vh quest`", value="super secret quest for you :eyes:", inline=False)
    embed.add_field(name="`vh pat`", value="pat the squirrel <:squirrelL:757097790181605416>", inline=False)
    embed.add_field(name="`vh feedback`", value="send anonymous feedback", inline=False)
    embed.add_field(name="`vh help`", value="Show this message", inline=False)
    embed.add_field(name="`vh where`", value="important hackathon links")
    embed.add_field(name="`vh how`", value="VH VII hacker guide")
    embed.add_field(name="`vh why`", value="why")
    embed.add_field(name="`vh github` or `vh gh`", value="Link to the bot's source code")
    embed.add_field(name="`vh stats`", value="Bot deployment info")
    embed.add_field(name="`vh ping`", value="Check bot latency")
    embed.set_footer(
        text="fun fact: vandy has a 3:1 squirrel to student population!",
        # squirrel emoji
        icon_url="https://cdn.discordapp.com/emojis/757098871859183687.png?v=1",
    )

    await ctx.send(embed=embed)


# add cogs
bot.add_cog(Info(bot))
bot.add_cog(Quest(bot))
bot.add_cog(Times(bot))

bot.run(os.environ["DISCORD"])
