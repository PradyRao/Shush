import sys
import importlib

import discord

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


# to eliminate code repetition, this check basically happens with most commands of this bot
async def voice_channel_command_check(ctx: discord.ext.commands.Context) -> bool:
    # check if user executed this command whilst not in voice channel
    if ctx.author.voice is None:
        await ctx.reply('you are not currently in a voice channel')
        return False
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
        return False
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
        return False
    else:
        return True
