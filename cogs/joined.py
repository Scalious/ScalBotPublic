from discord.ext import commands

import discord

import settings

logger = settings.logging.getLogger("bot")

class Joined(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()     
    async def joined(self, ctx, who : discord.Member ):
        """ The date the specified user has joined this Discord """
        joined_date = who.joined_at.strftime("%Y-%m-%d %H:%M") if who.joined_at else "Unknown"
        await ctx.send(f"{who.display_name} joined the Discord on {joined_date}")

async def setup(bot):
    await bot.add_cog(Joined(bot))