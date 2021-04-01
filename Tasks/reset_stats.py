import logging

import discord
from discord.ext import commands#, tasks

class ResetStats(commands.Cog):
    def __init__(self, client):
        self.client = client

    #@tasks.loop(seconds=0, minutes=0, hours=0)
    async def reset_daily(self):
        #instance when user joins, user leaves, user moves
        print('lul 4head')



def setup(client):
    client.add_cog(ResetStats(client))