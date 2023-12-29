import discord
from discord.ext import commands

import random

import settings
logger = settings.logging.getLogger("bot")

class Roll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        aliases=['r'], #shortcut/shortforms
        roll="Rolls a Random Number up to the given Number",
        enabled=True, #enableds/disables the command
        hidden=False #hides the command description
    )
    async def roll(self, ctx, number : int):
        """ Rolls a Random Number up to the given Number """
        await ctx.send(random.randint(1, number)) 

async def setup(bot):
    await bot.add_cog(Roll(bot))