import sys
import logging
import importlib

import discord
from discord.ext import commands

from Framework import process_practice

var_config = importlib.__import__("Config.var_config_" + sys.argv[1], fromlist=("var_config_" + sys.argv[1]))


class Disconnect(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['__dcmembers', '__emptyvcs'])
    @commands.has_permissions(administrator=True)
    async def _empty_vc(self, ctx):
        await empty_vc(ctx)


async def empty_vc(ctx: discord.ext.commands.Context):
    server = ctx.guild
    vcs = var_config.appliedchs[str(server.id)]

    for channel_id in vcs:
        channel = server.get_channel(channel_id)
        logging.log(level=logging.INFO,
                    msg=f'disconnecting members from voice channel {channel.name} id: {channel_id} in guild {server.name} id: {server.id}')
        for member in channel.members:
            logging.log(level=logging.INFO,
                        msg=f'disconnecting member {member.name}#{member.discriminator} id:{member.id}')
            await process_practice.process_leave_end(member, member.voice)
            await member.move_to(None)
    return


def setup(client):
    client.add_cog(Disconnect(client))