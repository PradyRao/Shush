import sys
import typing
import logging
import importlib

import discord
from discord.ext import commands

from Framework import mongo_utils, time_utils

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class Stats(commands.Cog):
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
    # if a mentioned user was not provided, fetches the stats of the author of the command
    if user is None:
        user = ctx.author

    # get the user's document from mongo database
    stats = mongo_utils.find_user_record(str(user.id), str(ctx.guild.id))

    # if there user has not practiced before their document will not exist in the database
    if stats is None:
        await ctx.reply(f'User {user.name}#{user.discriminator}\'s record does not exist')
        return

    # retrieve their stats and return it in embed form
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


async def get_server_stats(ctx: discord.ext.commands.Context, stat_type):
    # gets the server's stats from mongo
    stats = mongo_utils.find_server_record(str(ctx.guild.id))

    # if there is no server record (if no practice times have been recorded from any user in that server)
    if stats is None:
        await ctx.reply(f'This server\'s record does not exist')
        return

    # return the stats for the server in embed form
    daily = time_utils.time_readable(stats['practiceStats']['dailyTotal'])
    weekly = time_utils.time_readable(stats['practiceStats']['weeklyTotal'])
    monthly = time_utils.time_readable(stats['practiceStats']['monthlyTotal'])
    yearly = time_utils.time_readable(stats['practiceStats']['yearlyTotal'])
    grand_total = time_utils.time_readable(stats['practiceStats']['grandTotal'])

    embed = discord.Embed()
    embed.colour = 16357382
    embed.timestamp = time_utils.now_date()
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/693257204819689483/822353418839916544/IMG_1553.jpg')

    if stat_type == 'daily':
        embed.title = 'Daily Server Practice Time'
        embed.add_field(name='Daily Total', value=f'{daily[1]}h {daily[2]}m {daily[3]}s', inline=False)
    elif stat_type == 'weekly':
        embed.title = 'Weekly Server Practice Time'
        embed.add_field(name='Weekly Total', value=f'{weekly[0]}d {weekly[1]}h {weekly[2]}m {weekly[3]}s', inline=False)
    elif stat_type == 'monthly':
        embed.title = 'Monthly Server Practice Time'
        embed.add_field(name='Monthly Total', value=f'{monthly[0]}d {monthly[1]}h {monthly[2]}m {monthly[3]}s', inline=False)
    elif stat_type == 'yearly':
        embed.title = 'Yearly Practice Time'
        embed.add_field(name='Yearly Total', value=f'{yearly[0]}d {yearly[1]}h {yearly[2]}m {yearly[3]}s', inline=False)
    elif stat_type == 'grand':
        embed.title = 'Grand Total Practice Time'
        embed.add_field(name='Grand Total', value=f'{grand_total[0]}d {grand_total[1]}h {grand_total[2]}m {grand_total[3]}s', inline=False)
    elif stat_type == 'all' or None:
        embed.title = 'Server Practice Time Totals'
        embed.add_field(name='Daily Total', value=f'{daily[1]}h {daily[2]}m {daily[3]}s', inline=False)
        embed.add_field(name='Weekly Total', value=f'{weekly[0]}d {weekly[1]}h {weekly[2]}m {weekly[3]}s', inline=False)
        embed.add_field(name='Monthly Total', value=f'{monthly[0]}d {monthly[1]}h {monthly[2]}m {monthly[3]}s', inline=False)
        embed.add_field(name='Yearly Total', value=f'{yearly[0]}d {yearly[1]}h {yearly[2]}m {yearly[3]}s', inline=False)
        embed.add_field(name='Grand Total', value=f'{grand_total[0]}d {grand_total[1]}h {grand_total[2]}m {grand_total[3]}s', inline=False)

    await(await ctx.reply(embed=embed)).delete(delay=20)
    return


async def get_leaderboard(ctx: discord.ext.commands.Context):
    # get the server's practice leaderboard
    stat_list = mongo_utils.get_user_leaderboard(str(ctx.guild.id))

    # if there is no leaderboard (if no practice times have been recorded from any user in that server) or something else went wrong with the retrieval
    if stat_list is None:
        await ctx.reply(f'Could not retrieve this server\'s leaderboard')
        return

    # create an embed for the leaderboard
    embed = discord.Embed()
    embed.colour = 16357382
    embed.title = 'Practice Time Leaderboard'
    embed.timestamp = time_utils.now_date()
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/693257204819689483/822353418839916544/IMG_1553.jpg')

    # this will be to index the top users in each server
    # automatic indexing won't work here because if there is a null user (user document is no longer in the server)
    # leaderboard will error out and not display the embed
    index = 0
    # for each statistic on the leaderboard
    for stats in stat_list:
        # gets the user associated with the current statistic
        user = ctx.guild.get_member(int(stats["userId"]))

        # this handles the case where user is no longer in the server
        if user is None:
            # just move on to the next user without incrementing the index
            continue

        # dev note: we should probably delete records of users no longer in the server after some time

        total_readable = time_utils.time_readable(stats['info']['practiceStats']['totalTime'])
        total_str = f'{total_readable[0]}d {total_readable[1]}h {total_readable[2]}m {total_readable[3]}s'

        # if current user is the holder for most practiced in the server (excluding anyone no longer in the server)
        # give them a crown beside their name
        if index == 0:
            embed.add_field(name=f'{index+1}. {user.name}#{user.discriminator} ♕', value=f'Total time practiced: ' + total_str, inline=False)
        else:
            embed.add_field(name=f'{index+1}. {user.name}#{user.discriminator}', value=f'Total time practiced: ' + total_str, inline=False)

        # we increment the index here so when above user null case gets hit, index does not get incremented
        index += 1

    logging.log(level=logging.INFO, msg=f'Leaderboard requested by {ctx.author.name}#{ctx.author.discriminator}')

    await(await ctx.reply(embed=embed)).delete(delay=20)
    return


def setup(client):
    client.add_cog(Stats(client))
