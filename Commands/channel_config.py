import sys
import logging
import typing
import importlib

import discord
from discord.ext import commands

from Framework import mongo_utils

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class AddRemoveChannels(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['enablechs', 'echs'])
    @commands.has_permissions(administrator=True)
    async def _enable_channels(self, ctx, voice_channels: commands.Greedy[discord.VoiceChannel], *, text_channel: typing.Optional[discord.TextChannel]):
        await enable_channels(ctx, voice_channels, text_channel)

    @commands.command(aliases=['disablechs', 'dchs'])
    @commands.has_permissions(administrator=True)
    async def _disable_channels(self, ctx, *voice_channels: commands.Greedy[discord.VoiceChannel]):
        await disable_channels(ctx, voice_channels)


async def enable_channels(ctx, voice_channels, text_channel):
    name_lis = []
    # if args wasn't the intended type or no args was provided
    if not (voice_channels or text_channel):
        await ctx.reply(f'invalid command use, please include at least one voice channel and text channel')
        return
    # for each voice channels that was provided, add that to applied channels cache and from mongo
    # and map each voice channel to the text channel that was provided in broadcast channels cache and from mongo
    for vc in voice_channels:
        var_config.appliedchs[str(ctx.guild.id)].append(str(vc.id))
        var_config.broadcastchs[str(ctx.guild.id)][str(vc.id)] = str(text_channel.id)
        name_lis.append(vc.name)

    # update configuration in mongo
    mongo_utils.update_channel_configurations(str(ctx.guild.id), var_config.appliedchs[str(ctx.guild.id)], var_config.broadcastchs[str(ctx.guild.id)])

    logging.log(level=logging.INFO, msg=f"configured voice channels {str(name_lis).strip('[]')} to text channel {text_channel.name} in guild: {ctx.guild.id}")

    await ctx.reply(f"configured voice channels {str(name_lis).strip('[]')} to text channel {text_channel.name}")
    return


async def disable_channels(ctx, voice_channels):
    name_lis = []
    # if there was no voice channels given as argument
    if not voice_channels:
        await ctx.reply(f'invalid command use, please include at least one voice channel')
        return

    # for each voice channels that was provided, remove it from applied channels cache and from mongo
    # and remove each map entry that contains the channels to be removed as key in broadcast channels cache and from mongo
    for vc in voice_channels:
        if str(vc.id) in (var_config.appliedchs[str(ctx.guild.id)] and var_config.broadcastchs[str(ctx.guild.id)].keys()):
            var_config.appliedchs[str(ctx.guild.id)].remove(str(vc.id))
            del var_config.broadcastchs[str(ctx.guild.id)][str(vc.id)]
            name_lis.append(vc.name)

    # update configuration in mongo
    mongo_utils.update_channel_configurations(str(ctx.guild.id), var_config.appliedchs[str(ctx.guild.id)], var_config.broadcastchs[str(ctx.guild.id)])

    logging.log(level=logging.INFO, msg=f"removed voice channels {str(name_lis).strip('[]')} from configuration, they can no longer be used as practice rooms in guild: {ctx.guild.id}")

    await ctx.reply(f"removed voice channels {str(name_lis).strip('[]')} from configuration, they can no longer be used as practice rooms ")
    return


def setup(client):
    client.add_cog(AddRemoveChannels(client))
