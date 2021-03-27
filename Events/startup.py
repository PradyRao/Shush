import logging

import discord
from discord.ext import commands


class Startup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.log(level=logging.INFO, msg=f'logged in as {self.client.user.name}#{self.client.user.discriminator}')
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{self.client.command_prefix}help for more info'))
        # load and sync store here and then start the crons (unless using the given tasks functionality)


def setup(client):
    client.add_cog(Startup(client))
