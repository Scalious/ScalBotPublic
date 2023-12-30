import discord, settings
from discord.ext import commands
from discord.ui import Button, View

from datetime import timedelta

logger = settings.logging.getLogger("bot")

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.leveling = self.bot.get_cog("LevelingCog")
        self.user_handler = self.bot.get_cog("UserHandler")

    @staticmethod
    def is_owner():
        async def predicate(ctx):
            admin_role_id = settings.Admin_ID.id
            if admin_role_id in [role.id for role in ctx.author.roles]:
                return True
            else:
                raise commands.CommandError("Permission Denied.")
        return commands.check(predicate) 
        
    # Test Commands

    @commands.command()
    @is_owner()
    async def print_users(self, ctx):
        """Prints the users Dictionary"""
        user_handler = self.bot.get_cog("UserHandler")
        users = user_handler.get_users()
        await ctx.send(f'Users: {users}')
 
    @commands.command()
    @is_owner()
    async def purge_channel(self, ctx):
        """Purges the channel of 100 messages"""
        channel = ctx.channel
        await channel.purge()
        await ctx.send("Channel purged successfully.")

    # Admin Commands

    @commands.command()
    @is_owner()
    async def rules(self, ctx):
        """Resets the rules channel message"""
        channel = self.bot.get_channel(settings.rules_ID.id)
        await channel.purge()
        view = View()
        view.add_item(Button(style=discord.ButtonStyle.danger, label="Accept", custom_id="accept_rules"))
        view.add_item(Button(style=discord.ButtonStyle.primary, label="Decline", custom_id="decline_rules"))
        await channel.send(
            "```\nWelcome to the server!\n\n"
            "Rules:\n\n"
            "1. No malice.\n\n"
            "Please accept the rules by clicking the button below\n```",
            view=view
        )

    @commands.command()
    @is_owner()
    async def self_assign(self, ctx):
        """Resets the self-assign-roles channel message"""
        channel = self.bot.get_channel(settings.self_assign_roles_ID.id)  # Replace with your channel ID
        await channel.purge()
        await channel.send(
            "```\nWelcome to the self-assign-roles channel!\n\n"
            "Please React to the emotes below to gain access to the corresponding channels.\n\n```",
        )

    # Loads, unloads, and reloads cogs
    @commands.command()
    @is_owner()
    async def load(self, ctx, cog:str):
        """Loads a cog"""
        logger.info(f"Loading {cog}...")
        await self.bot.load_extension(f"cogs.{cog.lower()}") # Load a cog

    @commands.command()
    @is_owner()
    async def unload(self, ctx, cog:str):
        """Unloads a cog"""
        logger.info(f"Unloading {cog}...")
        await self.bot.unload_extension(f"cogs.{cog.lower()}") # Unload a cog

    @commands.command()
    @is_owner()
    async def reload(self, ctx, cog:str):
        """Reloads a cog"""
        logger.info(f"Reloading {cog}...")
        await self.bot.reload_extension(f"cogs.{cog.lower()}") # Reload a cog

    # Command Error Handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error. Try ***.help {command}*** if are having issues.") #await ctx.send("Handled Error Globally")  
        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_time = timedelta(seconds=int(error.retry_after))
            logger.warning(f'CommandOnCooldown for command {ctx.command}: retry after {cooldown_time} seconds')
            await ctx.send(f'You are on cooldown. Try again in {cooldown_time} seconds.')
        elif isinstance(error, commands.CommandError):
            logger.error(f'CommandError in command {ctx.command}: {error}')
            await ctx.send(f'Error: {error}')

async def setup(bot):
    await bot.add_cog(Admin(bot))
