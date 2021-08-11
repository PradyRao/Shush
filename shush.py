import sys
import os
import logging
import typing
import importlib

import discord
from discord.ext import commands

import bot_client

env = importlib.__import__("Config.env_" + sys.argv[1], fromlist=("env_" + sys.argv[1]))

logging.basicConfig(level=logging.INFO)


def main():
    @bot_client.client.command(aliases=['hi'])
    async def _hi(ctx, voice_channels: commands.Greedy[discord.VoiceChannel], *,
                  text_channel: typing.Optional[discord.TextChannel]):
        name_lis = []
        for vc in voice_channels:
            name_lis.append(vc.name)
        await ctx.reply(f"configured voice channels {str(name_lis).strip('[]')} to {text_channel.name}")

    '''@client.command(aliases=['purge'])
    async def _purge(ctx, amount = 10):
        await ctx.channel.purge(limit=amount)'''

    @bot_client.client.command()
    @commands.has_permissions(administrator=True)
    async def load(ctx, extension):
        bot_client.client.load_extension(f'Commands.{extension}')
        logging.log(level=logging.INFO, msg=f'loaded commands from {extension}')

    @bot_client.client.command()
    @commands.has_permissions(administrator=True)
    async def unload(ctx, extension):
        bot_client.client.unload_extension(f'Commands.{extension}')
        logging.log(level=logging.INFO, msg=f'unloaded commands from {extension}')
        await ctx.send(f'unloaded commands from {extension}')

    @bot_client.client.command()
    @commands.has_permissions(administrator=True)
    async def reload(ctx, extension):
        bot_client.client.unload_extension(f'Commands.{extension}')
        bot_client.client.load_extension(f'Commands.{extension}')
        logging.log(level=logging.INFO, msg=f'reloaded commands from {extension}')
        await ctx.send(f'{extension} reloaded')

    @bot_client.client.command(aliases=["__quit"])
    @commands.has_permissions(administrator=True)
    async def _close(ctx):
        await bot_client.client.close()

    for filename in os.listdir('./Commands'):
        if filename.endswith('.py'):
            bot_client.client.load_extension(f'Commands.{filename[:-3]}')

    for filename in os.listdir('./Events'):
        if filename.endswith('.py'):
            bot_client.client.load_extension(f'Events.{filename[:-3]}')

    for filename in os.listdir('./Tasks'):
        if filename.endswith('.py') and not filename.startswith('reset_stats'):
            bot_client.client.load_extension(f'Tasks.{filename[:-3]}')

    bot_client.client.run(env.token)


if __name__ == '__main__':
    main()
