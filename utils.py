import asyncio


async def paginate_embed(bot, channel, embeds):
    """
    async def modifier_func(type, curr_page) type: 1 for forward, -1 for backward.
    """
    total_pages = len(embeds)

    curr_page = 0

    og_msg = await channel.send(embed=embeds[curr_page].set_footer(text=f"Page {curr_page+1}/{total_pages}"))
    if total_pages <= 1:
        return

    await og_msg.add_reaction("⬅")
    await og_msg.add_reaction("➡")

    def check(reaction, user):
        return (
                not user.bot
                and reaction.message.channel == channel
                and reaction.message.id == og_msg.id
        )

    try:
        while True:
            reaction, user = await bot.wait_for(
                "reaction_add", timeout=120.0, check=check
            )
            if str(reaction.emoji) == "➡":
                if curr_page < total_pages - 1:
                    curr_page += 1
                    await og_msg.edit(
                        embed=embeds[curr_page].set_footer(text=f"Page {curr_page+1}/{total_pages}"))
                await og_msg.remove_reaction("➡", user)
            elif str(reaction.emoji) == "⬅":
                if curr_page > 0:
                    curr_page -= 1
                    await og_msg.edit(
                        embed=embeds[curr_page].set_footer(text=f"Page {curr_page+1}/{total_pages}"))
                await og_msg.remove_reaction("⬅", user)
            else:
                continue
    except asyncio.TimeoutError:
        await og_msg.remove_reaction("⬅", bot.user)
        await og_msg.remove_reaction("➡", bot.user)
        return
