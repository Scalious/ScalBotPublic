import discord, settings
from discord.ext import commands

from discord.ext import tasks

import cogs.member_function as mf

from cogs.member_function import UserHandler

# Leveling is only possible in the Public Lobby: lounge channel currently

logger = settings.logging.getLogger("bot")

class LevelingCog(commands.Cog):

    def __init__(self, bot, user_handler):
        self.bot = bot
        self.add_roles.start()
        self.remove_roles_exceed.start()
        self.remove_roles.start()
        self.update_counter = 0
        self.user_handler = user_handler
        self.last_channel = {}  
        self.role_change_tasks = {}

    # Add roles if they pass a new threshold
    @tasks.loop(seconds=5)  # Run this task every 30 seconds
    async def add_roles(self):
        guild = self.bot.get_guild(settings.GUILDS_ID.id)  # Replace with your guild ID
        await self.user_handler.load_users()
        users = self.user_handler.get_users()
        for member in guild.members:
            member_id_str = str(member.id)
            if member_id_str in users:  
                points = users[member_id_str]['points']  # Get the user's points from the dictionary
                role_id = await self.user_handler.check_threshold(points) 
                if role_id:
                    role = guild.get_role(int(role_id))
                    ignore_roles_ids = [
                        settings.Admin_ID.id,
                        settings.ScalBot3_0_ID.id,
                    ]
                    if role not in member.roles and role.id not in ignore_roles_ids:  # Check if the user already has the role
                        await member.add_roles(role, reason="Passed a new threshold")
                        await self.user_handler.save_users()
            else:
                await self.user_handler.add_member(member_id_str, member.display_name, 1, member.roles, member.joined_at)    
        await self.user_handler.save_users() #  Save users to file

    # Remove roles if they exceed the threshold
    @tasks.loop(seconds=3)  # Run this task every 3 seconds
    async def remove_roles_exceed(self):
        guild = self.bot.get_guild(settings.GUILDS_ID.id)  # Replace with your guild ID
        for member in guild.members:
            users = self.user_handler.get_users()
            if str(member.id) in users:
                points = users[str(member.id)]['points']
                role_id = await self.user_handler.check_threshold(points)
                if role_id:
                    role = guild.get_role(int(role_id))
                    threshold_roles = [guild.get_role(int(role['role_id'])) for role in mf.thresholds]
                    ignore_roles_ids = [
                        settings.Admin_ID.id,
                        settings.ScalBot3_0_ID.id,
                    ]
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position < role.position and member_role.id not in ignore_roles_ids:
                            await member.remove_roles(member_role, reason="Exceeds current threshold")

    # Remove roles if they previously had a higher threshold
    @tasks.loop(seconds=7)  # Run this task every 7 seconds
    async def remove_roles(self):
        guild = self.bot.get_guild(settings.GUILDS_ID.id)  # Replace with your guild ID
        for member in guild.members:
            users = self.user_handler.get_users()
            if str(member.id) in users:
                points = users[str(member.id)]['points']
                role_id = await self.user_handler.check_threshold(points)
                if role_id:
                    role = guild.get_role(int(role_id))
                    threshold_roles = [guild.get_role(int(role['role_id'])) for role in mf.thresholds]
                    ignore_roles_ids = [
                        settings.Admin_ID.id,
                        settings.ScalBot3_0_ID.id,
                    ]
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position > role.position and member_role.id not in ignore_roles_ids:
                            await member.remove_roles(member_role, reason="Exceeds current threshold")

    # Announcing Levels
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        users = self.user_handler.get_users()
        if str(after.id) in users:
            before_roles = set(before.roles)
            after_roles = set(after.roles)

            added_roles = after_roles - before_roles
            removed_roles = before_roles - after_roles

        if added_roles:
            if after.id in self.role_change_tasks:
                self.role_change_tasks[after.id].cancel()
            self.role_change_tasks[after.id] = tasks.loop(seconds=8, count=1)(self.send_role_change_message)
            self.role_change_tasks[after.id].start(after, added_roles)

        if removed_roles:
            member_id_str = str(after.id)
            current_roles = self.user_handler._users[member_id_str]['roles']
            self.user_handler._users[member_id_str]['roles'] = [role for role in current_roles if role not in [r.name for r in removed_roles]]
            await self.user_handler.save_users()
                
    async def send_role_change_message(self, member, added_roles):
        channel = self.last_channel.get(str(member.id))  # Get the last channel
        if channel is not None:
            role_names = ", ".join(role.name for role in added_roles) 
            await channel.send(f"{member.mention} has been given the role - {role_names}!")
            member_id_str = str(member.id)
            self.user_handler._users[member_id_str]['roles'] = [role.name for role in member.roles]
            await self.user_handler.save_users()

    # Points System for Leveling

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.add_roles()
        author_id = str(message.author.id)
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        self.last_channel[author_id] = message.channel  # ignore DMs and bots
        if message.channel.id == settings.lounge_test_ID.id or message.channel.id == settings.scalbot_test_ID.id:
            if author_id in self.user_handler._users:
                self.user_handler._users[author_id]['points'] += 1
                await self.user_handler.save_users()
            else:
                pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.add_roles()
        author_id = str(user.id)
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        if reaction.message.channel.id == settings.lounge_test_ID.id or reaction.message.channel.id == settings.scalbot_test_ID.id:
            if author_id in self.user_handler._users:
                self.user_handler._users[author_id]['points'] += 3
                await self.user_handler.save_users()
            else:
                pass

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.add_roles()
        author_id = str(user.id)
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        if reaction.message.channel.id == settings.lounge_test_ID.id or reaction.message.channel.id == settings.scalbot_test_ID.id:
            if author_id in self.user_handler._users:
                self.user_handler._users[author_id]['points'] -= 3
                await self.user_handler.save_users()
            else:
                pass       

async def setup(bot):
    user_handler = UserHandler(bot)
    await bot.add_cog(LevelingCog(bot, user_handler))
