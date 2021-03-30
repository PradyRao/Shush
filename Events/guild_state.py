import sys
import logging
import importlib

import discord
from discord.ext import commands

from Framework import mongo_utils

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class GuildStateUpdate(commands.Cog):
    def __init__(self, client):
        self.client = client

    # we need some way to register new servers that invite the bot while the bot is already active
    # once bot gets invited, a record is created in cache for appliedchs, broadcastchs and practicemap
    # and a record gets created on the database as well
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        var_config.appliedchs[str(guild.id)] = []
        var_config.broadcastchs[str(guild.id)] = {}
        var_config.practicemap[str(guild.id)] = {}

        # add new document to mongo for this guild with empty values
        mongo_utils.update_channel_configurations(str(guild.id), var_config.appliedchs[str(guild.id)], var_config.broadcastchs[str(guild.id)])

        logging.log(level=logging.INFO, msg=f'{guild.name} HAS INVITED THE BOT. ID: {guild.id}')

    # same thing but this time we're removing the records from cache and database
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        del var_config.appliedchs[str(guild.id)]
        del var_config.broadcastchs[str(guild.id)]
        del var_config.practicemap[str(guild.id)]

        # remove the configuration document corresponding to this guild from mongo
        mongo_utils.delete_channel_configuration(str(guild.id))

        logging.log(level=logging.INFO, msg=f'BOT HAS LEFT GUILD {guild.name}. ID: {guild.id}')


def setup(client):
    client.add_cog(GuildStateUpdate(client))
