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
        if before.voice.channel is None and after.voice.channel is not None:
            user_join(member, before, after)
        if before.voice.channel is not None and after.voice.channel is not None:
            user_move(member, before, after)
        if before.voice.channel is not None and after.voice.channel is None:
            user_leave(member, before, after)


def user_join(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member.channel.id not in var_config.appliedchs:
        member.edit(mute=False)
        logging.log(msg=f'{member.name}#{member.discriminator} unmuted: user is in an unconfigured channel')
        return
    else:
        member.edit(mute=True)
        logging.log(msg=f'{member.name}#{member.discriminator} muted: user is not practicing or excused')


def user_leave(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member.channel.id in var_config.appliedchs:
        process_practice.process_leave_end(member, before)


def user_move(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if member.channel.id in var_config.appliedchs:
        process_practice.process_leave_end(member, before)


def setup(client):
    client.add_cog(VoiceStateUpdate(client))
