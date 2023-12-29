import discord, settings
from discord.ext import commands

from discord.ui import Button, View
from discord import app_commands

from cogs.member_function import UserHandler

logger = settings.logging.getLogger("bot")

def run(): # Define a function to run the bot
    intents = discord.Intents.default() # Temporary Enables default Intents
    intents = discord.Intents.all() # Temporary Enables all Intents
    intents.message_content = True # Temporary Enables message_content Intents
    intents.members = True # Temporary Enables members Intents

    bot = commands.Bot(command_prefix=".", intents=intents)    # Create a new bot instance

    # Creates a Open a Ticket apps command - commented out the target user for now
    @bot.tree.context_menu(name = "Open a Ticket", guild = settings.GUILDS_ID)
    @app_commands.checks.cooldown(2, 3600, key = lambda i: (i.guild_id, i.user.id)) # 2 uses per hour per user
    async def open_ticket(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer()
        admin_role = discord.utils.get(message.guild.roles, id=settings.Admin_ID.id)
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False), # Deny everyone to see the channel
            #message.author: discord.PermissionOverwrite(read_messages=True), # Allow the author to see the channel
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
  
    @bot.event # Event to run when the bot is ready
    async def on_ready(): # Define a function to run when the bot is ready
        
        logger.info(f"User: {bot.user} (ID: {bot.user.id})") # Logs the bot's username and ID

        bot.user_handler = UserHandler(bot)  # Create a new UserHandler instance and add it as an attribute to the bot
        await bot.user_handler.load_users()  # Load users from file  
        print(bot.user_handler.get_users()) # Print users to console
        
        # for cmd_file in settings.CMDS_DIR.glob("*.py"): # Load all commands in the commands folder
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"commands.{cmd_file.name[:-3]}")

        for cog_file in settings.COGS_DIR.glob("*.py"): # Load all cogs in the cogs folder
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.stem}")  

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)  # Copy global commands to guild
        await bot.tree.sync(guild=settings.GUILDS_ID) # Sync commands to guild          
                                        
        print(f'We have logged in as {bot.user}')   # Prints the bot's username and identifier
    
    bot.run(settings.TOKEN)  # Run the bot with your token

if __name__ == "__main__":
    run() # Run our function to start bot