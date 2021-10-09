from asyncio import TimeoutError

from database import get_quest_level, update_quest_level

# from cogs.times import nash, end

import discord
from discord.ext import commands

VHVIII = [755112297772351499, 891807649656602675]  # vh viii server guild id
FIREHOSE_CHANNEL = 896499321749504020


class Quest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.firehose = bot.get_channel(FIREHOSE_CHANNEL)

    # list of pairwise challenge-flags
    ques = [
        (
            "welcome to vh quest! this is a ctf-style, fun treasure hunt where you look for flags like "
            "`vh{hi_im_a_flag}` hidden in places with cryptic clues to advance to the next level. "
            "Flags are always in the vh{} format. Feel free to reach out for hints and good luck on your quest! "
            "<:vh_heart:757444914983207002>",
            "vh{hi_im_a_flag}",
        ),
        (
            "I have a notion that there might be some sort of guide for this level...",
            "vh{thanks_4_read1ng}",
        ),
        (
            "Not sure *where* to look? Try asking the bot nicely :)",
            "vh{th4nks_br0th3r}",
        ),
        (
            "Honestly, f*** this: https://hastebin.com/usawoxitoc.md",
            "vh{factual}",
        ),
        (
            "If you *analyzed* those little links floating aroud, you might find a colorful flag.",
            "vh{blue_flag}",
        ),
        (
            "Don't you love our discord server? Shoutout to our designers for making some awesome assets.",
            "vh{imagine_using_discord}",
        ),
        (
            "Here at VandyHacks we love our open source projects, even if they sometimes have a lot of issues.",
            "vh{vaken_more_like_vâken}",
        ),
        (
            "Even though we're blasting off into space, we're still feeling a bit artsy. "
            "As we come to the end of our vh quest journey, let's take a trip down memory lane.",
            "vh{what_is_p0pping}",
        ),
    ]

    @commands.command()
    async def quest(self, ctx):
        def check(m):  # check if author same and in DMs
            return m.author == ctx.author and m.channel.type == discord.ChannelType.private

        # check if DMs
        if ctx.guild:
            await ctx.send("quests in my DMs only 👀")
            return await ctx.author.send("send `vh quest` :sweat_drops: :sweat_drops:")

        #        if nash() > end:
        #            return await ctx.author.send("quest is over i cri :(")

        print(f"{ctx.author} embarked on the quest")
        try:
            level = await get_quest_level(ctx.author)
            chall, flag = self.ques[level]
            await ctx.send(f"Level {level}: {chall}")
            await ctx.send("send your answer in the next line")
            try:
                answer = await self.bot.wait_for("message", check=check, timeout=60)
                print(answer.content)
                if answer.content == flag:
                    await ctx.send(":sparkles: Correct! :sparkles:")
                    await self.firehose.send(f"{ctx.author.name} with id {ctx.author.id} has reached level {level+1}.")
                    print(f"{ctx.author} answered level {level} correctly")
                    await update_quest_level(ctx.author)
                    await self.quest(ctx)  # send next level
                else:
                    await ctx.send("nah, try harder")
            except TimeoutError:
                print(f"{ctx.author} did not reply")
                await ctx.author.send("feel free to come back anytime :))")
        except IndexError:
            await ctx.send("congratulations you completed our quest ez")


def setup(bot):
    bot.add_cog(Quest(bot))
