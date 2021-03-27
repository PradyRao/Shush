import sys
import logging
import importlib

import discord
from discord.ext import commands

from Framework import process_practice

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class VoiceStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # if not (after.self_mute or after.self_deaf or after.self_stream or after.self_video or after.deaf or after.mute or after.afk):
        # if user was previously not in a voice channel and they joined into a voice channel
        if before.channel is None and after.channel is not None:
            await user_join(member, before, after)
            return
        # if the user was previously in a voice channel and they leave
        if before.channel is not None and after.channel is None:
            await user_leave(member, before, after)
            return
        # if the user was previously in a voice channel and they joined another voice channel
        if before.channel is not None and after.channel is not None:
            await user_move(member, before, after)
            return


# we just have to check whether they're in a configured channel or not
async def user_join(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # if the channel which the user joined is NOT part of the channels that are handled by the bot
    if str(after.channel.id) not in var_config.appliedchs:
        # we don't mute them
        await member.edit(mute=False)
        logging.log(level=logging.INFO, msg=f'{member.name}#{member.discriminator} unmuted: user is in an un-configured channel')
        return
    else:
        # if channel is handled by the bot, the user gets initially muted
        await member.edit(mute=True)
        logging.log(level=logging.INFO, msg=f'{member.name}#{member.discriminator} muted: user is not practicing or excused')


# if they leave, all that matters is whether the channel they were in previously was a configured channel
async def user_leave(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if str(before.channel.id) in var_config.appliedchs:
        await process_practice.process_leave_end(member, before)


# this is a bit more complicated
async def user_move(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # if the user moves from a configured channel to another configured channel
    if (before.channel.id != after.channel.id) and (str(before.channel.id) in var_config.appliedchs) and (str(after.channel.id) in var_config.appliedchs):
        # speeds up process - this just means that if user self muted or deafened or anything other move voice channels
        await member.edit(mute=True)
        await process_practice.process_leave_end(member, before)
    # if the user moves from an un-configured channel to a configured channel
    # user would previously not be using the bot functions anyways so we just directly mute
    elif str(before.channel.id) not in var_config.appliedchs and str(after.channel.id) in var_config.appliedchs:
        await member.edit(mute=True)
    # if the user moves from a configured channel to an un-configured channel
    # we need to process whether they were registered within practicemap and then un-mute
    elif str(before.channel.id) in var_config.appliedchs and str(after.channel.id) not in var_config.appliedchs:
        await member.edit(mute=False)
        await process_practice.process_leave_end(member, before)


def setup(client):
    client.add_cog(VoiceStateUpdate(client))
