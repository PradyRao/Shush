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

    @commands.command(aliases=['serverstats', 'svst'])
    @commands.has_permissions(manage_roles=True)
    async def _get_server_stats(self, ctx, type: typing.Optional[str] = None):
        await get_server_stats(ctx, type)

    @commands.command(aliases=['leaderboard', 'leader'])
    @commands.has_permissions(manage_roles=True)
    async def _get_leaderboard(self, ctx):
        await get_leaderboard(ctx)


async def get_user_stats(ctx: discord.ext.commands.Context, user: discord.Member):
    if user is None:
        user = ctx.author

    stats = mongo_utils.find_user_record(str(user.id), str(ctx.guild.id))

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
    embed.add_field(name='Last Repertoire Practice Time', value=f'You practiced your last rep for: {last_readable[1]}h {last_readable[2]}m {last_readable[3]}s', inline=False)
    embed.add_field(name='Total Practice Time', value=f'Total Time Practiced: {total_readable[1]}h {total_readable[2]}m {total_readable[3]}s', inline=False)

    await(await ctx.reply(embed=embed)).delete(delay=20)
    return


async def get_server_stats(ctx: discord.ext.commands.Context, type):
    stats = mongo_utils.find_server_record(str(ctx.guild.id))

    if stats is None:
        await ctx.reply(f'This server\'s record does not exist')
        return

    daily = time_utils.time_readable(stats['practiceStats']['dailyTotal'])
    weekly = time_utils.time_readable(stats['practiceStats']['weeklyTotal'])
    monthly = time_utils.time_readable(stats['practiceStats']['monthlyTotal'])
    yearly = time_utils.time_readable(stats['practiceStats']['yearlyTotal'])
    grand_total = time_utils.time_readable(stats['practiceStats']['grandTotal'])

    embed = discord.Embed()
    embed.colour = 16357382
    embed.timestamp = time_utils.now_date()
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/693257204819689483/822353418839916544/IMG_1553.jpg')

    if type == 'daily':
        embed.title = 'Daily Server Practice Time'
        embed.add_field(name='Daily Total', value=f'{daily[1]}h {daily[2]}m {daily[3]}s', inline=False)
    elif type == 'weekly':
        embed.title = 'Weekly Server Practice Time'
        embed.add_field(name='Weekly Total', value=f'{weekly[0]}d {weekly[1]}h {weekly[2]}m {weekly[3]}s', inline=False)
    elif type == 'monthly':
        embed.title = 'Monthly Server Practice Time'
        embed.add_field(name='Monthly Total', value=f'{monthly[0]}d {monthly[1]}h {monthly[2]}m {monthly[3]}s', inline=False)
    elif type == 'yearly':
        embed.title = 'Yearly Practice Time'
        embed.add_field(name='Yearly Total', value=f'{yearly[0]}d {yearly[1]}h {yearly[2]}m {yearly[3]}s', inline=False)
    else:
        embed.title = 'Server Practice Time Totals'
        embed.add_field(name='Daily Total', value=f'{daily[1]}h {daily[2]}m {daily[3]}s', inline=False)
        embed.add_field(name='Weekly Total', value=f'{weekly[0]}d {weekly[1]}h {weekly[2]}m {weekly[3]}s', inline=False)
        embed.add_field(name='Monthly Total', value=f'{monthly[0]}d {monthly[1]}h {monthly[2]}m {monthly[3]}s', inline=False)
        embed.add_field(name='Yearly Total', value=f'{yearly[0]}d {yearly[1]}h {yearly[2]}m {yearly[3]}s', inline=False)
        embed.add_field(name='Grand Total', value=f'{grand_total[0]}d {grand_total[1]}h {grand_total[2]}m {grand_total[3]}s', inline=False)

    await(await ctx.reply(embed=embed)).delete(delay=20)
    return


async def get_leaderboard(ctx: discord.ext.commands.Context):
    stat_list = mongo_utils.leaderboard(str(ctx.guild.id))

    if stat_list is None:
        await ctx.reply(f'Could not retrieve this server\'s leaderboard')
        return

    embed = discord.Embed()
    embed.colour = 16357382
    embed.title = 'Practice Time Leaderboard'
    embed.timestamp = time_utils.now_date()
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/693257204819689483/822353418839916544/IMG_1553.jpg')

    index = 0
    for stats in stat_list:
        user = ctx.guild.get_member(int(stats["userId"]))

        if user is None:
            continue

        total_readable = time_utils.time_readable(stats['info']['practiceStats']['totalTime'])
        total_str = f'{total_readable[0]}d {total_readable[1]}h {total_readable[2]}m {total_readable[3]}s'

        if index == 0:
            embed.add_field(name=f'{index+1}. {user.name}#{user.discriminator} ♕', value=f'Total time practiced: ' + total_str, inline=False)
        else:
            embed.add_field(name=f'{index+1}. {user.name}#{user.discriminator}', value=f'Total time practiced: ' + total_str, inline=False)

        index += 1

    await(await ctx.reply(embed=embed)).delete(delay=20)
    return


def setup(client):
    client.add_cog(Scales(client))
