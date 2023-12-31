import discord, settings
from discord.ext import commands

import apps_menu

from cogs.member_function import UserHandler

logger = settings.logging.getLogger("bot")

def run(): # Define a function to run the bot
    intents = discord.Intents.default() # Temporary Enables default Intents
    intents = discord.Intents.all() # Temporary Enables all Intents
    intents.message_content = True # Temporary Enables message_content Intents
    intents.members = True # Temporary Enables members Intents

    bot = commands.Bot(command_prefix=".", intents=intents)    # Create a new bot instance

    apps_menu.setup(bot) # Setup the apps menu
  
    @bot.event # Event to run when the bot is ready
    async def on_ready(): # Define a function to run when the bot is ready
        
        logger.info(f"User: {bot.user} (ID: {bot.user.id})") # Logs the bot's username and ID

        bot.user_handler = UserHandler(bot)  # Create a new UserHandler instance and add it as an attribute to the bot
        await bot.user_handler.load_users()  # Load users from file  
        #print(bot.user_handler.get_users()) # Print users to console
        
        for cmd_file in settings.CMDS_DIR.glob("*.py"): # Load all commands in the commands folder
            if cmd_file.name != "__init__.py":
                await bot.load_extension(f"commands.{cmd_file.name[:-3]}")

        for cog_file in settings.COGS_DIR.glob("*.py"): # Load all cogs in the cogs folder
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.stem}")  

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)  # Copy global commands to guild
        await bot.tree.sync(guild=settings.GUILDS_ID) # Sync commands to guild          
                                        
        print(f'We have logged in as {bot.user}')   # Prints the bot's username and identifier
    
    bot.run(settings.TOKEN)  # Run the bot with your token

if __name__ == "__main__":
    run() # Run our function to start bot