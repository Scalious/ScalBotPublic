import discord, settings
from discord.ext import commands
from cogs.greetings import Greetings
from cogs.ping import Ping
from cogs.roll import Roll
from cogs.joined import Joined
from cogs.slap import Slap
from cogs.math import Math
from cogs.antispam import Antispam
from cogs.ticketing import Ticketing
from cogs.leveling import LevelingCog

from discord.ui import Button, View
from discord import app_commands

from datetime import timedelta

logger = settings.logging.getLogger("bot")
  
def run(): # Define a function to run the bot
    intents = discord.Intents.default() # Temporary Enables default Intents
    intents = discord.Intents.all() # Temporary Enables all Intents
    intents.message_content = True # Temporary Enables message_content Intents
    intents.members = True # Temporary Enables members Intents

    bot = commands.Bot(command_prefix=".", intents=intents)    # Create a new bot instance 

    @bot.tree.context_menu(name = "Open a Ticket", guild = settings.GUILDS_ID)
    @app_commands.checks.cooldown(2, 3600, key = lambda i: (i.guild_id, i.user.id))
    async def open_ticket(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.defer()
        admin_role = discord.utils.get(message.guild.roles, id=787747360398770176)
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True),
            bot.user: discord.PermissionOverwrite(read_messages=True),
            admin_role: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await message.guild.create_text_channel(name=f'ticket-{message.author.name}', overwrites=overwrites)
        view = View()
        view.add_item(Button(style=discord.ButtonStyle.danger, label="Close Ticket", custom_id="close_ticket"))
        view.add_item(Button(style=discord.ButtonStyle.primary, label="Transcript", custom_id="transcript"))
        await channel.send(f'Ticket channel created for {message.author.mention}.', view=view)
        await interaction.followup.send('Ticket created.')
  
    @bot.event # Event to run when the bot is ready
    async def on_ready(): # Define a function to run when the bot is ready
        
        logger.info(f"User: {bot.user} (ID: {bot.user.id})") # Logs the bot's username and ID

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)  # Copy global commands to guild
        await bot.tree.sync(guild=settings.GUILDS_ID) # Sync commands to guild
               
        # for cmd_file in settings.CMDS_DIR.glob("*.py"): # Load all commands in the commands folder
        #     if cmd_file.name != "__init__.py":
        #         await bot.load_extension(f"commands.{cmd_file.name[:-3]}")
        
        # await bot.add_cog(Greetings(bot))   
        # await bot.add_cog(Ping(bot))
        # await bot.add_cog(Roll(bot))
        # await bot.add_cog(Joined(bot))
        # await bot.add_cog(Slap(bot))
        # await bot.add_cog(Math(bot))
        # await bot.add_cog(Antispam(bot))
        # await bot.add_cog(Ticketing(bot))

        for cog_file in settings.COGS_DIR.glob("*.py"): # Load all cogs in the cogs folder
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.stem}")       
                                        
        print(f'We have logged in as {bot.user}')   # Prints the bot's username and identifier

    # Custom Check for Admin Commands
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
        return commands.check(predicate) 

    # Admin Commands 

    @bot.command(hidden=True)
    @is_owner()
    async def load(ctx, cog:str):
        logger.info(f"Loading {cog}...")
        await bot.load_extension(f"cogs.{cog.lower()}") # Load a cog

    @bot.command(hidden=True)
    @is_owner()
    async def unload(ctx, cog:str):
        logger.info(f"Unloading {cog}...")
        await bot.unload_extension(f"cogs.{cog.lower()}") # Unload a cog

    @bot.command(hidden=True)
    @is_owner()
    async def reload(ctx, cog:str):
        logger.info(f"Reloading {cog}...")
        await bot.reload_extension(f"cogs.{cog.lower()}") # Reload a cog

    # Error Handling     
        # This could be a listener instead of an event, but I'm not sure how to do that yet.
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error. Try ***.help {command}*** if are having issues.") #await ctx.send("Handled Error Globally")  
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_time = timedelta(seconds=int(error.retry_after))
            logger.warning(f'CommandOnCooldown for command {ctx.command}: retry after {cooldown_time} seconds')
            await ctx.send(f'You are on cooldown. Try again in {cooldown_time} seconds.')
        elif isinstance(error, commands.CommandError):
            logger.error(f'CommandError in command {ctx.command}: {error}')
            await ctx.send(f'Error: {error}')
    
    bot.run(settings.TOKEN)  # Run the bot with your token

if __name__ == "__main__":
    run() # Run our function to start bot