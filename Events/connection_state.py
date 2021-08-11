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
        # set the bot's profile picture
        with open("./Resources/IMG_1553.jpg", "rb") as image_file:  # rb = read bytes I believe
            image = image_file.read()  # get bytes from file-like object
        await self.client.user.edit(avatar=image)
        # set the bot visibility status and add in a game-status
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(name=f'{self.client.command_prefix}help for more info'))

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.log(level=logging.INFO, msg=f'BOT HAS DISCONNECTED')

    @commands.Cog.listener()
    async def on_resumed(self):
        logging.log(level=logging.INFO, msg=f'BOT SUCCESSFULLY RESUMED')


def setup(client):
    client.add_cog(Startup(client))
