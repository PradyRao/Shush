import sys
import typing
import importlib

import discord
from discord.ext import commands

from Framework import mongo_utils, time_utils

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class Scales(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['stats', 'stat'])
    async def _get_user_stats(self, ctx, *, args: typing.Optional[discord.Member] = None):
        await get_user_stats(ctx, args)


async def get_user_stats(ctx: discord.ext.commands.Context, user: discord.Member):
    if user is None:
        user = ctx.author

    stats = mongo_utils.find_user_record(str(user.id))

    if stats is None:
        await ctx.reply(f'User {user.name}#{user.discriminator}\'s record does not exist')
        return

    last_rep = stats['info']['practiceStats']['lastRep']
    total_readable = time_utils.time_readable(stats['info']['practiceStats']['totalTime'])
    last_readable = time_utils.time_readable(stats['info']['practiceStats']['lastRepTime'])

    embed = discord.Embed()
    embed.colour = 16357382
    embed.timestamp = time_utils.now_date()
    embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)

    embed.add_field(name='Last Repertoire', value=last_rep, inline=False)
    embed.add_field(name='Last Repertoire Practice Time', value=f'You practiced your last rep for: {last_readable[1]}h {last_readable[0]}m {last_readable[3]}s', inline=False)
    embed.add_field(name='Total Practice Time', value=f'Total Time Practiced: {total_readable[1]}h {total_readable[0]}m {total_readable[3]}s', inline=False)

    await(await ctx.reply(embed=embed)).delete(delay=20)
    return


def setup(client):
    client.add_cog(Scales(client))
