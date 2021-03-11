import logging

import discord
from discord.ext import commands

from Config import var_config
from Framework import process_practice


class Practice(commands.Cog):
    def __init__(self, client):
        self.client = client

    # placeholder command, remove after implementation and testing
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command(aliases=['practice', 'prac', 'start'])
    async def _practice(self, ctx, *args):
        await practice(ctx)

    @commands.command(aliases=['end', 'nomore', 'stop'])
    async def _end_session(self, ctx, *args):
        await end_session(ctx)

    @commands.command(aliases=['status', 'np', 'room'])
    async def _room_status(self, ctx, *args):
        await room_status(ctx)

    @commands.command(aliases=['piece', 'song', 'content'])
    async def _practice_piece(self, ctx, *, args):
        await practice_piece(ctx, args)


async def practice(ctx: discord.ext.commands.Context):
    # check if user executed this command whilst not in voice channel
    if ctx.author.voice is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    # check if someone is already practicing
    elif str(ctx.author.voice.channel.id) in var_config.practicemap.keys():
        practicing_user = ctx.guild.get_member(int(var_config.practicemap[str(ctx.author.voice.channel.id)]))
        await ctx.reply(f'{practicing_user.name}#{practicing_user.discriminator} is already practicing in this channel')
    else:
        # create the user entry for their practice session
        logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} is now practicing in voice channel {ctx.author.voice.channel.name} id:'
                                            f' {ctx.author.voice.channel.id}')
        var_config.practicemap[str(ctx.author.voice.channel.id)] = str(ctx.author.id)
        var_config.practicemap[str(ctx.author.voice.channel.id) + 'timer'] = ''  # to be implemented
        await ctx.author.edit(mute=False)
        await ctx.reply('you are now practicing')

        print(var_config.practicemap)


async def end_session(ctx: discord.ext.commands.Context):
    # check if user executed this command whilst not in voice channel
    if ctx.author.voice.channel is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    # check if user that executed this command is the one that is practicing
    elif str(ctx.author.voice.channel.id) in var_config.practicemap.keys() and var_config.practicemap[str(ctx.author.voice.channel.id)] != str(ctx.author.id):
        await ctx.reply('you are not practicing in this voice channel')
    else:
        # process their practice time and end their session
        logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has ended their session in voice channel {ctx.author.voice.channel.name} id:'
                                            f' {ctx.author.voice.channel.id}')
        await ctx.author.edit(mute=True)
        await process_practice.process_leave_end(ctx.author, ctx.author.voice)


async def room_status(ctx: discord.ext.commands.Context):
    # check if user executed this command whilst not in voice channel
    if ctx.author.voice.channel is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    # check to see if there is a user currently practicing in the voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.practicemap.keys():
        await ctx.reply('there is no one practicing in this voice channel')
    else:
        # get the current practicing user
        practicing_user = ctx.guild.get_member(int(var_config.practicemap[str(ctx.author.voice.channel.id)]))
        # get the current length of user's practice session - not implemented

        # if practicing user has indicated what piece they are currently practicing, include it in the reply
        if str(ctx.author.voice.channel.id) + 'piece' in var_config.practicemap.keys():
            await ctx.reply(f'{practicing_user.name}#{practicing_user.discriminator} has been practicing for {0} hours {0} minutes. '
                      f'User is currently practicing: {var_config.practicemap[str(ctx.author.voice.channel.id) + "piece"]}')
        else:
            await ctx.reply(f'{practicing_user.name}#{practicing_user.discriminator} has been practicing for {0} hours {0} minutes. ')


async def practice_piece(ctx: discord.ext.commands.Context, piece):
    # check if user executed this command whilst not in voice channel
    if ctx.author.voice.channel is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.practicemap.keys() or var_config.practicemap[str(ctx.author.voice.channel.id)] != str(ctx.author.id):
        await ctx.reply('you are not practicing in this voice channel')
    else:
        # create/change the entry for user's current practice piece
        logging.log(level=logging.INFO, msg=f'practicing user {ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has set their piece to {piece} in channel {ctx.author.voice.channel.name} id:'
                                            f' {ctx.author.voice.channel.id}')
        var_config.practicemap[str(ctx.author.voice.channel.id) + 'piece'] = str(piece)
        await ctx.reply(f'set the piece {ctx.author.name}#{ctx.author.discriminator} is practicing to {piece}')


def setup(client):
    client.add_cog(Practice(client))
