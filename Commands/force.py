import logging
import re

import discord
from discord.ext import commands

from Config import var_config


class Force(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['fpractice','forcepractice', 'forceprac', 'fprac'])
    async def _force_practice(self, ctx, user: discord.Member):
        print('hurrdurr')

    @commands.command(aliases=['fstop','forcestop'])
    async def _force_stop(self, ctx, user: discord.Member):
        print('hurrdurr')

def setup(client):
    client.add_cog(Force(client))
