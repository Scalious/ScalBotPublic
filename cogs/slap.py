from discord.ext import commands
import random

class Slap(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    class Slapper(commands.Converter):

        def __init__(self, *, use_nicknames) -> None:
            self.use_nicknames = use_nicknames

        async def convert(self, ctx, argument):
            members = ctx.guild.members
            if argument.lower() == "dildo" or argument == "🍆":
                return f"**{ctx.author.display_name}** slapped **{ctx.author.display_name}** with *{argument}*"
            else:
                return f"**{ctx.author.display_name}** slapped **{random.choice(members).display_name}** with *{argument}*"

    @commands.command()
    async def slap(self, ctx, reason : Slapper(use_nicknames=True) ):
        """ Slaps a random Member with whatever you say"""
        await ctx.send(reason)  

async def setup(bot):
    await bot.add_cog(Slap(bot))