import os
import logging

from discord.ext import commands

from Config import envdev

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix=envdev.botprefix)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'Commands.{extension}')
    logging.log(level=logging.INFO, msg=f'loaded commands from {extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'Commands.{extension}')
    logging.log(level=logging.INFO, msg=f'unloaded commands from {extension}')
    await ctx.send(f'unloaded commands from {extension}')

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f'Commands.{extension}')
    client.load_extension(f'Commands.{extension}')
    logging.log(level=logging.INFO, msg=f'reloaded commands from {extension}')
    await ctx.send(f'{extension} reloaded')

for filename in os.listdir('./Commands'):
    if filename.endswith('.py'):
        client.load_extension(f'Commands.{filename[:-3]}')

for filename in os.listdir('./Events'):
    if filename.endswith('.py'):
        client.load_extension(f'Events.{filename[:-3]}')

client.run(envdev.token)
