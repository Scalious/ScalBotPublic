import discord, settings
from discord.ui import Button, View
from discord import app_commands

logger = settings.logging.getLogger("bot")

def is_owner():
    async def predicate(interaction : discord.Interaction):
        admin_role_id = settings.Admin_ID.id
        if admin_role_id in [role.id for role in interaction.user.roles]:
                return True
    return app_commands.check(predicate)

def setup(bot):

    def __init__(self, bot):
        self.bot = bot
        self.unmute_tasks = {}

    # Creates the Open a Ticket button
    @bot.tree.context_menu(name = "Open a Ticket", guild = settings.GUILDS_ID)
    @app_commands.checks.cooldown(2, 3600, key = lambda i: (i.guild_id, i.user.id)) # 2 uses per hour per user
    async def open_ticket(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer()
        admin_role = discord.utils.get(message.guild.roles, id=settings.Admin_ID.id)
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False), # Deny everyone to see the channel
            interaction.user: discord.PermissionOverwrite(read_messages=True), # Allow the user to see the channel
            #message.author: discord.PermissionOverwrite(read_messages=True), # Allow the target message author to see the channel
            bot.user: discord.PermissionOverwrite(read_messages=True), # Allow the bot to see the channel
            admin_role: discord.PermissionOverwrite(read_messages=True) # Allow the admin role to see the channel
        }
        member = await message.guild.fetch_member(interaction.user.id)
        nickname = member.nick if member.nick else member.display_name
        channel = await message.guild.create_text_channel(name=f'ticket-{message.author.name}', overwrites=overwrites)
        view = View()
        view.add_item(Button(style=discord.ButtonStyle.danger, label="Close Ticket", custom_id="close_ticket"))
        view.add_item(Button(style=discord.ButtonStyle.primary, label="Transcript", custom_id="transcript"))
        await channel.send(f'Ticket channel created by {nickname}.', view=view)
        await channel.send(f'Target message: {message.content}')
        await interaction.followup.send('Ticket created.')  

    # Mutes a user
    @bot.tree.context_menu(name = "Mute", guild = settings.GUILDS_ID)
    @is_owner()
    async def mute(interaction: discord.Interaction, message: discord.Message):
        """Timeout a user for an hour."""
        await interaction.response.defer()
        muted_role = discord.utils.get(interaction.guild.roles, id=settings.Muted_ID.id)
        await message.author.add_roles(muted_role)
        await interaction.followup.send(f'{message.author.mention} has been muted.')

    @mute.error
    async def mute_error(interaction: discord.Interaction, error):
        await interaction.response.send_message(f"Permission Denied.", ephemeral=True)
        

    #this needs to cancel the await_unmute task
    @bot.tree.context_menu(name = "UnMute", guild = settings.GUILDS_ID)
    @is_owner()
    async def unmute(interaction: discord.Interaction, message: discord.Message):
        """Umutes a user immediately."""
        await interaction.response.defer()
        muted_role = discord.utils.get(interaction.guild.roles, id=settings.Muted_ID.id)
        await message.author.remove_roles(muted_role)
        await interaction.followup.send(f'{message.author.mention} has been unmuted.')

    @unmute.error
    async def mute_error(interaction: discord.Interaction, error):
        await interaction.response.send_message(f"Permission Denied.", ephemeral=True)



