import logging
import typing

import discord
from discord.ext import commands

from Config import var_config
from Framework import process_practice, time_utils, general_check


class Practice(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['practice', 'prac', 'start'])
    async def _practice(self, ctx):
        await practice(ctx)

    @commands.command(aliases=['end', 'nomore', 'stop'])
    async def _end_session(self, ctx):
        await end_session(ctx)

    @commands.command(aliases=['status', 'np', 'room'])
    async def _room_status(self, ctx):
        await room_status(ctx)

    @commands.command(aliases=['piece', 'song', 'content'])
    async def _practice_piece(self, ctx, *, args: typing.Optional[str] = None):
        await practice_piece(ctx, args)


async def practice(ctx: discord.ext.commands.Context):
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check if someone is already practicing
    elif str(ctx.author.voice.channel.id) in var_config.practicemap.keys():
        practicing_user = ctx.guild.get_member(int(var_config.practicemap[str(ctx.author.voice.channel.id)]))
        await ctx.reply(f'{practicing_user.name}#{practicing_user.discriminator} is already practicing in this channel')
    else:
        # create the user entry for their practice session
        logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} is now practicing in voice channel {ctx.author.voice.channel.name} id:'
                                            f' {ctx.author.voice.channel.id}')
        var_config.practicemap[str(ctx.author.voice.channel.id)] = str(ctx.author.id)
        var_config.practicemap[str(ctx.author.voice.channel.id) + 'start_time'] = time_utils.now_time()
        await ctx.author.edit(mute=False)
        await ctx.reply('you are now practicing')
        print(var_config.practicemap)
    return


async def end_session(ctx: discord.ext.commands.Context):
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check if user that executed this command is the one that is practicing
    elif str(ctx.author.voice.channel.id) in var_config.practicemap.keys() and var_config.practicemap[str(ctx.author.voice.channel.id)] != str(ctx.author.id):
        await ctx.reply('you are not practicing in this voice channel')
    else:
        # process their practice time and end their session
        logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has ended their session in voice channel {ctx.author.voice.channel.name} id:'
                                            f' {ctx.author.voice.channel.id}')
        await ctx.author.edit(mute=True)
        await process_practice.process_leave_end(ctx.author, ctx.author.voice)
    return


async def room_status(ctx: discord.ext.commands.Context):
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check to see if there is a user currently practicing in the voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.practicemap.keys():
        await ctx.reply('there is no one practicing in this voice channel')
    else:
        # get the current practicing user
        practicing_user = ctx.guild.get_member(int(var_config.practicemap[str(ctx.author.voice.channel.id)]))
        # get the current length of user's practice session
        time_practiced_seconds = time_utils.time_practiced_seconds(ctx.author.voice.channel.id)
        time_practiced = time_utils.time_readable(time_practiced_seconds)
        # if practicing user has indicated what piece they are currently practicing, include it in the reply
        if str(ctx.author.voice.channel.id) + 'piece' in var_config.practicemap.keys():
            await ctx.reply(f'{practicing_user.name}#{practicing_user.discriminator} has been practicing for {time_practiced[1]} hours {time_practiced[2]} minutes {time_practiced[3]} seconds. '
                      f'User is currently practicing: {var_config.practicemap[str(ctx.author.voice.channel.id) + "piece"]}')
        else:
            await ctx.reply(f'{practicing_user.name}#{practicing_user.discriminator} has been practicing for {time_practiced[1]} hours {time_practiced[2]} minutes {time_practiced[3]} seconds.')
    return


async def practice_piece(ctx: discord.ext.commands.Context, piece):
    if not await general_check.voice_channel_command_check(ctx):
        return
    # check if a user is practicing in the voice channel and if the user that executed the command is currently the one practicing in this voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.practicemap.keys() or var_config.practicemap[str(ctx.author.voice.channel.id)] != str(ctx.author.id):
        await ctx.reply('you are not practicing in this voice channel')
    elif not piece:
        await ctx.reply('invaid command usage, you have not specified a piece')
    else:
        # create/change the entry for user's current practice piece
        logging.log(level=logging.INFO, msg=f'practicing user {ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has set their piece to {piece} in channel {ctx.author.voice.channel.name} id:'
                                            f' {ctx.author.voice.channel.id}')
        var_config.practicemap[str(ctx.author.voice.channel.id) + 'piece'] = str(piece)
        await ctx.reply(f'set the piece {ctx.author.name}#{ctx.author.discriminator} is practicing to {piece}')
    return


def setup(client):
    client.add_cog(Practice(client))
