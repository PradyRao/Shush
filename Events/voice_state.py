import logging

import discord
from discord.ext import commands

from Config import var_config
from Framework import process_practice


class VoiceStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # if user was previously not in a voice channel and they joined into a voice channel
        if before.voice.channel is None and after.voice.channel is not None:
            user_join(member, before, after)
        # if the user was previously in a voice channel and they joined another voice channel
        if before.voice.channel is not None and after.voice.channel is not None:
            user_move(member, before, after)
        # if the user was previously in a voice channel and they leave
        if before.voice.channel is not None and after.voice.channel is None:
            user_leave(member, before, after)


# we just have to check whether they're in a configued channel or not
def user_join(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # if the channel which the user joined is NOT part of the channels that are handled by the bot
    if str(after.channel.id) not in var_config.appliedchs:
        # we don't mute them
        member.edit(mute=False)
        logging.log(msg=f'{member.name}#{member.discriminator} unmuted: user is in an unconfigured channel')
        return
    else:
        # if channel is handled by the bot, the user gets initially muted
        member.edit(mute=True)
        logging.log(msg=f'{member.name}#{member.discriminator} muted: user is not practicing or excused')


# if they leave, all that matters is whether the channel they were in previously was a configured channel
def user_leave(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if str(before.channel.id) in var_config.appliedchs:
        process_practice.process_leave_end(member, before, "leave")


# this is a bit more complicated
def user_move(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # if the user moves from a configured channel to another configured channel
    # we need to process whether user was registered within practicemap and then mute
    if str(before.channel.id) in var_config.appliedchs and str(after.channel.id) in var_config.appliedchs:
        process_practice.process_leave_end(member, before, "move")
    # if the user moves from an unconfigured channel to a configured channel
    # user would previously not be using the bot functions anyways so we just directly mute
    elif str(before.channel.id) not in var_config.appliedchs and str(after.channel.id) in var_config.appliedchs:
        member.edit(mute=True)
    # if the user moves from a configured channel to an unconfigured channel
    # we need to process whether they were registered within practicemap and then un-mute
    # same as user_leave
    elif str(before.channel.id) in var_config.appliedchs and str(after.channel.id) not in var_config.appliedchs:
        process_practice.process_leave_end(member, before, "leave")


def setup(client):
    client.add_cog(VoiceStateUpdate(client))
