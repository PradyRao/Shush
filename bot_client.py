import sys
import logging
import importlib

import discord
from discord.ext import commands


env = importlib.__import__("Config.env_" + sys.argv[1], fromlist=("env_" + sys.argv[1]))

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.members = True
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True

client = commands.Bot(command_prefix=env.bot_prefix, intents=intents)
client.remove_command('help')
