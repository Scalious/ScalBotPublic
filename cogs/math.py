import discord
from discord.ext import commands
import math

import settings
logger = settings.logging.getLogger("bot")

class Math(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.group() #Creates a group call math
    async def math(self, ctx):
        """ Math Functions """
        if ctx.invoked_subcommand is None:
            await ctx.send(f"No, {ctx.subcommand_passed} does not belong to math")

    @math.command() #In the group math - this command exists - .math add number number2
    async def add(self, ctx, number : int, number2 : int):
        """ Add two numbers. """
        await ctx.send(number + number2)

    @math.command() #In the group math - this command exists - .math subtract number number2
    async def subtract(self, ctx, number : int, number2 : int):
        """ Subtract two numbers. """
        await ctx.send(number - number2)
    
    @math.command() #In the group math - this command exists - .math multiply number number2
    async def multiply(self, ctx, number : int, number2 : int):
        """ Multiply two numbers. """
        await ctx.send(number * number2)

    @math.command() #In the group math - this command exists - .math divide number number2
    async def divide(self, ctx, number : int, number2 : int):
        """ Divide two numbers. """
        await ctx.send(number / number2)
    
    """pie to the x digit capped at 100"""
    @math.command()
    async def pie(self, ctx, number : int):
        """ Pie. """
        if number > 48:
            await ctx.send("The number is too large. Please try again.")
        else:
            await ctx.send(f"{math.pi:.{number+1}}")

async def setup(bot):
    await bot.add_cog(Math(bot))