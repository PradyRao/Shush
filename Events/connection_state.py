import sys
import logging
import importlib

import discord
from discord.ext import commands

from Framework import mongo_utils

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class Startup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.log(level=logging.INFO, msg=f'logged in as {self.client.user.name}#{self.client.user.discriminator}')
        # set the bot visibility status and add in a game-status
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{self.client.command_prefix}help for more info'))
        # for all servers that the bot is in
        for guild in self.client.guilds:
            # get the applied and broadcast channel configurations for that guild
            channel_configs = mongo_utils.get_channel_configurations(str(guild.id))
            # if that configuration exists in the database - add the configuration to the cache
            if channel_configs is not None:
                var_config.appliedchs[str(guild.id)] = channel_configs['applied_channels']
                var_config.broadcastchs[str(guild.id)] = channel_configs['broadcast_channels']
            else:
                var_config.appliedchs[str(guild.id)] = []
                var_config.broadcastchs[str(guild.id)] = {}
            var_config.practicemap[str(guild.id)] = {}

        logging.log(level=logging.INFO, msg=f'Initial loading of appliedchs, broadcastchs, practicemap finished for all guilds')
        # start the crons here (unless using the given tasks functionality)

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.log(level=logging.INFO, msg=f'BOT HAS DISCONNECTED')

    @commands.Cog.listener()
    async def on_resumed(self):
        logging.log(level=logging.INFO, msg=f'BOT SUCCESSFULLY RESUMED')


def setup(client):
    client.add_cog(Startup(client))
