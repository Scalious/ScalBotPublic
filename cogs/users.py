import discord
from discord.ext import commands

from member_function import add_member, users

class Users(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.users = users
        self.add_member = add_member

    @commands.Cog.listener()
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return # ignore DMs and bots
        if message.author.id not in users: # If the user is not in the dictionary
            await self.add_member(message.author.id, message.author.display_name, 0) # Add the user to the dictionary
        else: # If the user is in the dictionary
            pass # Do nothing

async def setup(bot):
    await bot.add_cog(Users(bot))


