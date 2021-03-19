import logging

import discord
from discord.ext import commands

from Config import var_config
from Framework import general_check


class Excuse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['excuse', 'ex'])
    async def _excuse(self, ctx, *args: commands.Greedy[discord.Member]):
        await excuse(ctx, args)

    @commands.command(aliases=['unexcuse', 'unex', 'ux'])
    async def _unexcuse(self, ctx, *args: commands.Greedy[discord.Member]):
        await unexcuse(ctx, args)


async def excuse(ctx: discord.ext.commands.Context, args):
    ismod = ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_roles or ctx.author.guild_permissions.manage_guild
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel, or a moderator
    elif (not ismod) and ((str(ctx.author.voice.channel.id) not in var_config.practicemap.keys()) or (var_config.practicemap[str(ctx.author.voice.channel.id)] != str(
            ctx.author.id))):
        await ctx.reply('you are not practicing in this voice channel')
    elif not args:
        await ctx.reply("you haven't specified anyone to excuse")
    else:
        for member in args:
            # check if mentioned user is a valid member of the guild and if they're in the voice chat
            if (member.id != ctx.author.id) and (member in ctx.author.voice.channel.members):
                logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has requested to excuse member {member.name}#'
                                                    f'{member.discriminator} id: {member.id} in '
                                                    f'practice room'
                                                    f' {ctx.author.voice.channel.name} id:'
                                                    f' {ctx.author.voice.channel.id}')
                # add their entry into excused key of the practice map
                if str(ctx.author.voice.channel) + 'excused' not in var_config.practicemap.keys():
                    var_config.practicemap[str(ctx.author.voice.channel.id) + 'excused'] = [member.id]
                else:
                    var_config.practicemap[str(ctx.author.voice.channel.id) + 'excused'].append(member.id)
                # un-mute them
                await member.edit(mute=False)
        await ctx.reply('valid mentioned members have been excused')
    return


async def unexcuse(ctx: discord.ext.commands.Context, args):
    ismod = ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_roles or ctx.author.guild_permissions.manage_guild
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel, or a moderator
    elif (not ismod) and ((str(ctx.author.voice.channel.id) not in var_config.practicemap.keys()) or (var_config.practicemap[str(ctx.author.voice.channel.id)] != str(
            ctx.author.id))):
        await ctx.reply('you are not practicing in this voice channel')
    elif not args:
        await ctx.reply("you haven't specified anyone to un-excuse")
    else:
        for member in args:
            # check if mentioned user is a valid member of the guild and if they're in the voice chat and if they're currently excused
            if (member.id != ctx.author.id) \
                    and (member in ctx.author.voice.channel.members) \
                    and (str(ctx.author.voice.channel.id) + 'excused' in var_config.practicemap.keys()) \
                    and (member.id in var_config.practicemap[str(ctx.author.voice.channel.id) + 'excused']):
                logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has requested to un-excuse member {member.name}#'
                                                    f'{member.discriminator} id: {member.id} in '
                                                    f'practice room'
                                                    f' {ctx.author.voice.channel.name} id:'
                                                    f' {ctx.author.voice.channel.id}')
                # remove their entry from practice map excused
                var_config.practicemap[str(ctx.author.voice.channel.id) + 'excused'].remove(member.id)
                # re-mute them
                await member.edit(mute=True)
        await ctx.reply('valid mentioned members have been un-excused')
    return


def setup(client):
    client.add_cog(Excuse(client))
