import discord
from discord.ext import commands

class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #     await message.add_reaction("👋")

    @commands.command(
        enabled=True, #enableds/disables the command
        hidden=False #hides the command description
    )
    async def hello(self, ctx):
        author = ctx.author
        await ctx.send(f"Happy Holidays! {author.mention}")
        
    @commands.command(
        aliases=['heyo','sup','yo','howdy','heeey','heey','hey'], #shortcut/shortforms
        enabled=True, #enableds/disables the command
        hidden=True #hides the command description
    )
    async def hi(self, ctx):
        author = ctx.author
        await ctx.send(f"Whats gucci {author.mention}")

async def setup(bot):
    await bot.add_cog(Greetings(bot))