import logging

import discord
from discord.ext import commands

class VoiceStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        #instance when user joins, user leaves, user moves
        print('lul 4head')



def setup(client):
    client.add_cog(VoiceStateUpdate(client))