import logging
import typing


import discord
from discord.ext import commands

from Config import var_config


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
    if not (voice_channels or text_channel):
        await ctx.reply(f'invalid command use, please include at least one voice channel and text channel')
        return

    for vc in voice_channels:
        var_config.appliedchs.append(str(vc.id))
        var_config.broadcastchs[str(vc.id)] = str(text_channel.id)
        name_lis.append(vc.name)
    await ctx.reply(f"configured voice channels {str(name_lis).strip('[]')} to text channel {text_channel.name}")
    return


async def disable_channels(ctx, voice_channels):
    name_lis = []
    if not voice_channels:
        await ctx.reply(f'invalid command use, please include at least one voice channel')
        return

    for vc in voice_channels:
        if str(vc.id) in (var_config.appliedchs and var_config.broadcastchs.keys()):
            var_config.appliedchs.remove(str(vc.id))
            del var_config.broadcastchs[str(vc.id)]
            name_lis.append(vc.name)
    await ctx.reply(f"removed voice channels {str(name_lis).strip('[]')} from configuration, they can no longer be used as practice rooms ")
    return


def setup(client):
    client.add_cog(AddRemoveChannels(client))
