import discord
from discord.ext import commands

class Ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
            aliases=['p'], #shortcut/shortforms
            enabled=True, #enableds/disables the command
            hidden=False #hides the command description
        )
    async def ping(self, ctx):
        """ Test Ping """
        await ctx.send("Pong")

async def setup(bot):
    await bot.add_cog(Ping(bot))