import logging
import typing

import discord
from discord.ext import commands

from Config import var_config
from Framework import time_utils, process_practice


class Force(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['fpractice', 'forcepractice', 'forceprac', 'fprac'])
    @commands.has_permissions(manage_roles=True)
    async def _force_practice(self, ctx, args: typing.Optional[discord.Member] = None):
        await force_practice(ctx, args)

    @commands.command(aliases=['fstop', 'forcestop'])
    @commands.has_permissions(manage_roles=True)
    async def _force_stop(self, ctx, args: typing.Optional[discord.Member] = None):
        await force_stop(ctx, args)


async def force_practice(ctx: discord.ext.commands.Context, user):
    if ctx.author.voice is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    elif not user:
        await ctx.reply('you have not provided a user to force-practice')
    elif user not in ctx.author.voice.channel.members:
        await ctx.reply(f'{user.name}#{user.discriminator} is not in your voice channel')
    else:
        # no one is practicing in this voice channel
        if str(ctx.author.voice.channel.id) not in var_config.practicemap.keys():
            logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has requested force-practice member {user.name}#'
                                                f'{user.discriminator} id: {user.id} in '
                                                f'practice room'
                                                f' {ctx.author.voice.channel.name} id:'
                                                f' {ctx.author.voice.channel.id}')
            var_config.practicemap[str(ctx.author.voice.channel.id)] = str(user.id)
            var_config.practicemap[str(ctx.author.voice.channel.id) + 'start_time'] = time_utils.now_time()
            await user.edit(mute=False)
            await ctx.send(f'{user.name}#{user.discriminator} is now practicing by {ctx.author.name}#{ctx.author.discriminator}\'s request')
        # check if mentioned user is already the one practicing
        elif var_config.practicemap[str(ctx.author.voice.channel.id)] == str(user.id):
            await ctx.reply(f'{user.name}#{user.discriminator} is already the user practicing in this channel')
        # someone else is practicing, end their practice session and start a new practice session for user
        else:
            logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has requested force-practice member {user.name}#'
                                                f'{user.discriminator} id: {user.id} in '
                                                f'practice room'
                                                f' {ctx.author.voice.channel.name} id:'
                                                f' {ctx.author.voice.channel.id}')
            # find out who is practicing
            practicing_user = ctx.guild.get_member(int(var_config.practicemap[str(ctx.author.voice.channel.id)]))
            await process_practice.process_leave_end(practicing_user, practicing_user.voice)
            # forced user's entry is now created in practicemap and user is un-muted
            var_config.practicemap[str(ctx.author.voice.channel.id)] = str(user.id)
            var_config.practicemap[str(ctx.author.voice.channel.id) + 'start_time'] = time_utils.now_time()
            await user.edit(mute=False)
            await ctx.send(f'{user.name}#{user.discriminator} is now practicing by {ctx.author.name}#{ctx.author.discriminator}\'s request')


async def force_stop(ctx: discord.ext.commands.Context, user):
    if ctx.author.voice is None:
        await ctx.reply('you are not currently in a voice channel')
    # check if user executed this command while being in an un-configured voice channel
    elif str(ctx.author.voice.channel.id) not in var_config.appliedchs:
        await ctx.reply('you are not in a configured voice channel')
    # check the voice channel is configured and
    # if the voice channel is corresponding to the text channel that the command was executed
    elif str(ctx.author.voice.channel.id) in var_config.appliedchs and var_config.broadcastchs[str(ctx.author.voice.channel.id)] != str(ctx.channel.id):
        await ctx.reply('this text channel does not correspond with your current voice channel')
    elif not user:
        await ctx.reply('you have not provided a user to force-stop')
    elif user not in ctx.author.voice.channel.members:
        await ctx.reply(f'{user.name}#{user.discriminator} is not in your voice channel')
    elif str(ctx.author.voice.channel.id) not in var_config.practicemap.keys() or var_config.practicemap[str(ctx.author.voice.channel.id)] != str(user.id):
        await ctx.reply(f'{user.name}#{user.discriminator} is not practicing in this voice channel')
    else:
        logging.log(level=logging.INFO, msg=f'{ctx.author.name}#{ctx.author.discriminator} id: {ctx.author.id} has requested force-stop member {user.name}#'
                                            f'{user.discriminator} id: {user.id} in '
                                            f'practice room'
                                            f' {ctx.author.voice.channel.name} id:'
                                            f' {ctx.author.voice.channel.id}')
        await process_practice.process_leave_end(user, user.voice)
        await ctx.send(f'{user.name}#{user.discriminator} has stopped practicing by {ctx.author.name}#{ctx.author.discriminator}\'s request')


def setup(client):
    client.add_cog(Force(client))
