import logging

import discord
from discord.ext import commands

from Config import var_config


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
    # check if user executed this command whilst not in voice channel
    if ctx.author.voice is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel, or a moderator
    elif (not ismod) and ((str(ctx.author.voice.channel.id) not in var_config.practicemap.keys()) or (var_config.practicemap[str(ctx.author.voice.channel.id)] != str(
            ctx.author.id))):
        await ctx.reply('you are not practicing in this voice channel')
    else:
        if not args:
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


async def unexcuse(ctx: discord.ext.commands.Context, args):
    ismod = ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_roles or ctx.author.guild_permissions.manage_guild
    # check if user executed this command whilst not in voice channel
    if ctx.author.voice is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel, or a moderator
    elif (not ismod) and ((str(ctx.author.voice.channel.id) not in var_config.practicemap.keys()) or (var_config.practicemap[str(ctx.author.voice.channel.id)] != str(
            ctx.author.id))):
        await ctx.reply('you are not practicing in this voice channel')
    else:
        if not args:
            await ctx.reply("you haven't specified anyone to excuse")
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


def setup(client):
    client.add_cog(Excuse(client))
