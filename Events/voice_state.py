import logging

import discord
from discord.ext import commands

from Config import var_config

class VoiceStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #instance when user joins, user leaves, user moves
        if(before.voice.channel is None and after.voice.channel is not None):
            userjoin(member, before, after)
        if (before.voice.channel is not None and after.voice.channel is not None):
            usermove(member, before, after)
        if (before.voice.channel is not None and after.voice.channel is None):
            userleave(member, before, after)



def userjoin(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if(member.channel.id not in var_config.appliedchs):
        member.edit(mute=False)
        logging.log(msg=f'{member.name}#{member.discriminator} unmuted: user is in an unconfigured channel')
        return
    else:
        member.edit(mute=True)
        logging.log(msg=f'{member.name}#{member.discriminator} muted: user is not practicing or excused')

def userleave(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
def usermove(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):


def setup(client):
    client.add_cog(VoiceStateUpdate(client))