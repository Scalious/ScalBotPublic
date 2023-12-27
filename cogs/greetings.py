import discord
from discord.ext import commands

from discord import ui, ButtonStyle, Member, Role
from discord.ui import Button, View
from discord.utils import get

import settings

class Greetings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    class RoleButtons(ui.View):
        def __init__(self, member: Member, accept_role: Role, remove_role: Role):
            super().__init__()
            self.member = member
            self.accept_role = accept_role
            self.remove_role = remove_role

    # This NotOwner class is the same in main.py, but I'm not sure how to import it yet.
        # I want to separate this into a separate file, but I'm not sure how to do that yet.
    class NotOwner(commands.CheckFailure):
        pass

    def is_owner():
        async def predicate(ctx):
            admin_role_id = 787747360398770176
            if admin_role_id in [role.id for role in ctx.author.roles]:
                return True
            else:
                raise commands.CommandError("Permission Denied.")
                print (admin_role_id)
        return commands.check(predicate) 
        # I want to separate this into a separate file, but I'm not sure how to do that yet.
    @commands.command(
        enabled=True, #enableds/disables the command
        hidden=True #hides the command description
    )
    @is_owner()
    async def rules(self, ctx):
        # Get the channel
        channel = self.bot.get_channel(959111607068274789)  # Replace with your channel ID
        # Purge the channel
        await channel.purge()
        # Get the message
        view = View()
        view.add_item(Button(style=discord.ButtonStyle.danger, label="Accept", custom_id="accept_rules"))
        view.add_item(Button(style=discord.ButtonStyle.primary, label="Decline", custom_id="decline_rules"))
        await channel.send(
            "Welcome to the server!\n\n"
            "Rules:\n\n"
            "1. No malice.\n\n"
            "Please accept the rules by clicking the button below",
            view=view
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Replace 'your-channel-id' with the ID of your channel
        if message.channel.id == 986433466650468403:
            await message.add_reaction("👋")
        
    @commands.Cog.listener()
    async def on_member_join(self, message, member):
        # Get the channel where you want to send the message
        channel = message.channel.id == 986433466650468403
        # Send a message to the channel
        await channel.send(f"Welcome to the server, {member.mention}!")

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