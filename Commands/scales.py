import random

import discord
from discord.ext import commands

scaleList = [
    "G major",
    "G minor",
    "Ab major",
    "Ab minor",
    "A major",
    "A minor",
    "Bb major",
    "Bb minor",
    "B major",
    "B minor",
    "C major",
    "C minor",
    "Db major",
    "Db minor",
    "D major",
    "D minor",
    "Eb major",
    "Eb minor",
    "E major",
    "E minor",
    "F major",
    "F minor",
    "Gb major",
    "Gb minor"
]


class Scales(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['scales', 'scale'])
    async def _get_random_scale(self, ctx):
        await get_random_scale(ctx)


async def get_random_scale(ctx):
    await ctx.reply(f'{random.choice(scaleList)}')
    return


def setup(client):
    client.add_cog(Scales(client))
