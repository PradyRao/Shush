import logging
import typing


import discord
from discord.ext import commands

from Config import var_config

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['help'])
    async def _help(self, ctx):
        await help(ctx, self.client.command_prefix)


async def help(ctx: discord.ext.commands.Context, bot_prefix):
    ismod = ctx.author.guild_permissions.manage_roles
    isadmin = ctx.author.guild_permissions.administrator

    embed = discord.Embed()
    embed.colour = 2491526
    embed.title = 'Shushbot help page'
    embed.description = 'Documentation available [here](https://shush-bot.firebaseapp.com/) \n Report bugs [here](https://forms.gle/A4mA6AYJQFdDm62N9) \n Click [here](' \
                        'https://discordapp.com/channels/690354771189825547/705344913319133184/705354040778948669) for optimal Discord audio settings '
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/438392276981645325/822349903169716224/IMG_1553.jpg')
    embed.add_field(name=bot_prefix + 'practice', value=f'If your channel has no one practicing, this command will set you into practice mode')
    embed.add_field(name=bot_prefix + 'nomore', value='If you don\'t want to practice anymore, this command can be used to end your practice session')
    embed.add_field(name=bot_prefix + 'np', value=f'This command will make the bot tell you who is practicing.')
    embed.add_field(name=bot_prefix + 'piece', value=f'If user is practicing, this command will set the piece you are practicing. Usage: {bot_prefix}piece <piece name>')
    embed.add_field(name=bot_prefix + 'excuse', value=f'Unmutes a non-practicing user so they can talk. Usage: {bot_prefix}excuse <user>')
    embed.add_field(name=bot_prefix + 'unexcuse', value=f'Mutes a user once they are done giving you feedback. Usage: {bot_prefix}unexcuse <user>')
    embed.add_field(name=bot_prefix + 'bitrate', value=f'Only users currently practicing can use this command, it will alter the bitrate of your practice room to your preference. Usage: '
                                                       f'{bot_prefix}setbit <value>')
    embed.add_field(name=bot_prefix + 'userlimit', value=f'Only users currently practicing can use this command, it will alter the user limit of your practice room to your preference. Usage: '
                                                         f'{bot_prefix}userlimit <value>')
    embed.add_field(name=bot_prefix + 'scale', value=f'Gives you a random scale to practice. Usage: {bot_prefix}scale')
    embed.add_field(name=bot_prefix + 'stats', value=f'Gets statistics of a user. Usage: {bot_prefix}stats or {bot_prefix}stats <user>')
    if(ismod):
        embed.add_field(name=bot_prefix + 'forcepractice', value=f'For case by case scenarios when a mod wants to override someone to practice.')
        embed.add_field(name=bot_prefix + 'forcestop', value=f'For case by case scenarios when a mod wants to override and end a practice session.')
        embed.add_field(name=bot_prefix + 'serverstats', value=f'Gets the server total statistics, accumulation of everyone\'s practice time for certain time intervals. Usage: {bot_prefix}serverStats')
        embed.add_field(name=bot_prefix + 'leaderboard', value=f'Get the overall leaderboard of individual practice times. Use with great caution, do not use it in public channels. Usage: {bot_prefix}leaderboard')
    if(isadmin):
        embed.add_field(name=bot_prefix + 'enablechs', value=f'To enable new voicechats to the bot, or update existing voice chats with a new text chat. Usage: {bot_prefix}enablechs vcId1, vcId2, ..., '
                                                             f'vcIdn, txtChId (Assigns vcId1 - vcIdn to txtChId).')
        embed.add_field(name=bot_prefix + 'disablechs', value=f'To disable existing voicechats from the bot. Usage: {bot_prefix}disablechs vcId1, vcId2, ..., vcIdn')
        embed.add_field(name=bot_prefix + 'dcmembers', value=f'Disconnect all members in that channel category in which the bot is enabled')

    await(await ctx.reply(embed=embed)).delete(delay=20)


def setup(client):
    client.add_cog(Help(client))