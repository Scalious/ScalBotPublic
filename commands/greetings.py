import discord
from discord.ext import commands

from discord import ui, Member, Role

from discord.utils import get

import settings

logger = settings.logging.getLogger("bot")

class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Replace 'your-channel-id' with the ID of your channel
        if message.channel.id == settings.welcome_ID.id:
            await message.add_reaction("👋")
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(settings.welcome_ID.id)
        await channel.send(f"Welcome to the server, {member.mention}!\n\n"
                           "Please read the rules in #rules and assign yourself a role in #self-assign-roles.\n",
                           )

    @commands.command(
        enabled=True, #enableds/disables the command
        hidden=False #hides the command description
    )
    async def hello(self, ctx):
        """Try saying howdy!"""
        author = ctx.author
        await ctx.send(f"Hello! {author.mention}")
        
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