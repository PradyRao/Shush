import logging
import typing

import discord
from discord.ext import commands

from Config import var_config
from Framework import general_check


class ChannelSettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['bitrate', 'setbit', 'bt'])
    async def _set_bitrate(self, ctx, bitrate: typing.Optional[int] = None):
        await set_bitrate(ctx, bitrate)

    @commands.command(aliases=['limit', 'userlimit', 'users', 'ut'])
    async def _set_user_limit(self, ctx, user_limit: typing.Optional[int] = None):
        await set_user_limit(ctx, user_limit)


async def set_bitrate(ctx, bitrate):
    ismod = ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_roles or ctx.author.guild_permissions.manage_guild
    # perform voice command general check
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel, or a moderator
    elif (not ismod) and ((str(ctx.author.voice.channel.id) not in var_config.practicemap.keys()) or (var_config.practicemap[str(ctx.author.voice.channel.id)] != str(
            ctx.author.id))):
        await ctx.reply('you are not practicing in this voice channel')
    elif not bitrate:
        await ctx.reply('incorrect command usage, you have not provided a bit rate to set for this channel')
    elif (bitrate < 8) or (bitrate > (var_config.bit_tier[ctx.author.voice.channel.guild.premium_tier]) / 1000):
        await ctx.reply(f'bitrate setting must be in between 8 and {var_config.bit_tier[ctx.author.voice.channel.guild.premium_tier] / 1000}')
    else:
        await ctx.author.voice.channel.edit(bitrate=bitrate * 1000)
        await ctx.reply(f'bitrate for this channel has been set to {bitrate}')
    return


async def set_user_limit(ctx, user_limit):
    ismod = ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.manage_roles or ctx.author.guild_permissions.manage_guild
    # perform voice command general check
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel, or a moderator
    elif (not ismod) and ((str(ctx.author.voice.channel.id) not in var_config.practicemap.keys()) or (var_config.practicemap[str(ctx.author.voice.channel.id)] != str(
            ctx.author.id))):
        await ctx.reply('you are not practicing in this voice channel')
    elif not user_limit:
        await ctx.reply('incorrect command usage, you have not provided a user limit to set for this channel')
    elif user_limit > 99 or user_limit < 0:
        await ctx.reply('incorrect input, user limit has to be between 0 (no limit) or 99')
    else:
        await ctx.author.voice.channel.edit(user_limit=user_limit)
        await ctx.reply(f'user limit for this channel has been set to {user_limit}')
    return


def setup(client):
    client.add_cog(ChannelSettings(client))
