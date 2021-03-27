import sys
import os
import logging
import typing
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


@client.command(aliases=['hi'])
async def _hi(ctx, voice_channels: commands.Greedy[discord.VoiceChannel], *, text_channel: typing.Optional[discord.TextChannel]):
    name_lis = []
    for vc in voice_channels:
        name_lis.append(vc.name)
    await ctx.reply(f"configured voice channels {str(name_lis).strip('[]')} to {text_channel.name}")


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'Commands.{extension}')
    logging.log(level=logging.INFO, msg=f'loaded commands from {extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'Commands.{extension}')
    logging.log(level=logging.INFO, msg=f'unloaded commands from {extension}')
    await ctx.send(f'unloaded commands from {extension}')


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'Commands.{extension}')
    client.load_extension(f'Commands.{extension}')
    logging.log(level=logging.INFO, msg=f'reloaded commands from {extension}')
    await ctx.send(f'{extension} reloaded')


@client.command(aliases=["quit"])
@commands.has_permissions(administrator=True)
async def _close(ctx):
    await client.close()


for filename in os.listdir('./Commands'):
    if filename.endswith('.py'):
        client.load_extension(f'Commands.{filename[:-3]}')

for filename in os.listdir('./Events'):
    if filename.endswith('.py'):
        client.load_extension(f'Events.{filename[:-3]}')

for filename in os.listdir('./Tasks'):
    if filename.endswith('.py'):
        client.load_extension(f'Tasks.{filename[:-3]}')

client.run(env.token)
