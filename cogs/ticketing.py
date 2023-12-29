import discord, os, settings
from discord.ext import commands
#from discord.ui import Button, View
from discord import InteractionType, utils
from datetime import datetime

from discord.utils import get

logger = settings.logging.getLogger("bot")
# the listener for rules should be setup in its own Rules class eventually

class Ticketing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Alernative method to call the command using .ticket as a command

    # @commands.command()
    # @commands.has_permissions(manage_channels=True)
    # async def ticket(self, ctx):
    #     admin_id = settings.Admin_ID.id
    #     admin_role = discord.utils.get(ctx.guild.roles, id=admin_id)
    #     overwrites = {
    #         ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    #         ctx.author: discord.PermissionOverwrite(read_messages=True),
    #         self.bot.user: discord.PermissionOverwrite(read_messages=True),
    #         admin_role: discord.PermissionOverwrite(read_messages=True)
    #     }
    #     channel = await ctx.guild.create_text_channel(name=f'ticket-{ctx.author.name}', overwrites=overwrites)
    #     view = View()
    #     view.add_item(Button(style=discord.ButtonStyle.danger, label="Close Ticket", custom_id="close_ticket"))
    #     view.add_item(Button(style=discord.ButtonStyle.primary, label="Transcript", custom_id="transcript"))
    #     await channel.send(f'Ticket channel created for {ctx.author.mention}.', view=view)

    # Listener to control button interactions
    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == InteractionType.component:
            # Rules acceptance
            if interaction.data["custom_id"] == "accept_rules":
                await interaction.response.defer()
                member = interaction.user
                new_member_role = get(interaction.guild.roles, id=settings.New_Member_ID.id)  # New Member role ID
                guest_role = get(interaction.guild.roles, id=settings.Guest_ID.id)  # Guest role ID
                await member.add_roles(new_member_role)
                await member.remove_roles(guest_role)
            if interaction.data["custom_id"] == "decline_rules":
                await interaction.response.defer()
                member = interaction.user
                guest_role = get(interaction.guild.roles, id=settings.Guest_ID.id)  # Guest role ID
                new_member_role = get(interaction.guild.roles, id=settings.New_Member_ID.id)  # New Member role ID
                await member.add_roles(guest_role)
                await member.remove_roles(new_member_role)
            # Ticketing
            if interaction.data["custom_id"] == "close_ticket":
                if 'ticket-' in interaction.channel.name and interaction.user.guild_permissions.manage_channels:
                    await interaction.channel.delete()
                    await interaction.response.send_message('Ticket channel closed.')
            elif interaction.data["custom_id"] == "transcript":
                if 'ticket-' in interaction.channel.name:
                    await interaction.response.defer()
                    if os.path.exists(f"{interaction.channel.id}.md"):
                        return await interaction.followup.send(f"A transcript is already being generated!", ephemeral = True)
                    with open(f"{interaction.channel.id}.md", 'a') as f:
                        f.write(f"# Transcript of {interaction.channel.name}:\n\n")
                        async for message in interaction.channel.history(limit = None, oldest_first = True):
                            created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                            if message.edited_at:
                                edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                                f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                            else:
                                f.write(f"{message.author} on {created}: {message.clean_content}\n")
                        generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                        f.write(f"\n*Generated at {generated} by {self.bot.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
                    with open(f"{interaction.channel.id}.md", 'rb') as f:
                        await interaction.followup.send(file = discord.File(f, f"{interaction.channel.name}.md"))
                    os.remove(f"{interaction.channel.id}.md")
                else: 
                    await interaction.response.send_message("This isn't a ticket!", ephemeral = True)

async def setup(bot):
    await bot.add_cog(Ticketing(bot))