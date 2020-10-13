from asyncio import TimeoutError

from database import get_quest_level, update_quest_level
from cogs.times import nash, end

import discord
from discord.ext import commands


class Quest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    VHVII = 755112297772351499  # vh vii server guild id

    # list of pairwise challenge-flags
    ques = [
        (
            "welcome to vh quest! this is a ctf-style, fun treasure hunt where you look for flags like "
            "`vh{yes_this_is_a_flag_hehe}` hidden in places with cryptic clues to advance to the next level. "
            "Flags are always in the vh{} format. Feel free to reach out for hints and good luck on your quest! "
            "<:vh_heart:757444914983207002>",
            "vh{yes_this_is_a_flag_hehe}",
        ),
        (
            "```bf\n"
            "----[-->+++++<]>.++[->+++<]>.-[----->+<]>.-------.+[->+++<]>++.+.[--->+<]>----.--[->+++++<]>+.+[->++"
            "<]>+.+++++++.-------------.++++++++++.++++++++++.++[->+++<]>.+++++++++++++.[-->+<]>---.+[--->++<]>-."
            "[->+++<]>-.>--[-->+++<]>.\n"
            "```",
            "vh{tabr1el_is_l3wd}",
        ),
        (
            "Did you tell Tabriel Ging how much you love VandyHacks? He's asking that frequently.",
            "vh{v1rtually_the_be$t_<3}",
        ),
        ("everyone ask what is vh, why is vh, no one ask how is vh", "vh{aww_thx_4_asking_heart_emoji}"),
        ("This is off the *record*, but we're really **digging** the website this year. Are you? ;)", "vh{p/q2-q4!}"),
        (
            "this level has no answer, literally, it's an empty string. "
            "But you can still get past it, I believe in you!",
            "",
        ),  # empty message can still get past this
        (
            "you\u200b\u200b\u200b\u200b \u200b\u200bare \u200e\u200b\u200bnearing \u200e\u200b\u200bthe \u200bend. "
            "\u200e\u200bYour \u200b\u200b\u200e\u200b"
            "flag \u200b\u200e\u200b\u200bis \u200b\u200ehere, \u200e\u200e\u200bwrap \u200b\u200e\u200b\u200bit "
            "\u200b\u200b\u200b\u200e\u200ein "
            "\u200e\u200e\u200b\u200bvh{} \u200e\u200e\u200balso \u200e\u200e\u200e\u200e\u200eit's all uppercase.",
            "vh{HIDDENFLAGL3ZG0}",
        ),
        ("Dark web? More like dork web. Find the teapot, vhviippzyvdissgj :onion:", "vh{this_is_the_end_im_sad}"),
    ]

    @commands.command()
    async def quest(self, ctx):
        def check(m):  # check if author same and in DMs
            return m.author == ctx.author and m.channel.type == discord.ChannelType.private

        # check if DMs
        if ctx.guild:
            await ctx.send("quests in my DMs only 👀")
            return await ctx.author.send("send `vh quest` :sweat_drops: :sweat_drops:")

        if nash() > end:
            return await ctx.author.send("quest is over i cri :(")

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
