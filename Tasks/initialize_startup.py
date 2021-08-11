import sys
import importlib
import logging

from discord.ext import commands

from Framework import mongo_utils

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class Initialize(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.loop.create_task(self._initialize_startup())

    async def _initialize_startup(self):
        await self.client.wait_until_ready()
        await initialize_cache(self.client)


async def initialize_cache(client):
    for guild in client.guilds:
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

    logging.log(level=logging.INFO, msg=f'Initial loading of appliedchs, broadcastchs, practicemap finished for all '
                                        f'guilds')


def setup(client):
    client.add_cog(Initialize(client))
