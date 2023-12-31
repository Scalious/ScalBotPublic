import discord, settings
from discord.ext import commands

from discord.ext import tasks

from thresholds import thresholds

import asyncio

# Leveling is only possible in the Public Lobby: lounge channel currently

logger = settings.logging.getLogger("bot")

class LevelingCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.add_roles.start()
        self.remove_roles_exceed.start()
        self.remove_roles.start()
        self.last_channel = {}  
        self.role_change_tasks_add = {}
        self.role_change_tasks_exceed = {}
        self.role_change_tasks_remove = {}
        self.users = self.bot.user_handler

    # Add roles if they pass a new threshold
    @tasks.loop(seconds=1)  # Run this task every 1 seconds
    async def add_roles(self):
        guild = self.bot.get_guild(settings.GUILDS_ID.id)  # Replace with your guild ID
        users = self.users.get_users()  # Get the users data
        role_change_tasks_add = []
        for member in guild.members:
            member_id_str = str(member.id)
            user_data = users.get(member_id_str)
            if user_data:  # Check if the user data exists
                points = user_data['points']  # Get the user's points from the dictionary
                role_id = await self.bot.user_handler.check_threshold(points) 
                if role_id:
                    role = guild.get_role(int(role_id))
                    ignore_roles_ids = [
                        settings.Admin_ID.id,
                        settings.ScalBot3_0_ID.id,
                    ]
                    if role not in member.roles and role.id not in ignore_roles_ids:  # Check if the user already has the role
                        role_change_tasks_add.append(member.add_roles(role, reason="Passed a new threshold"))
        if role_change_tasks_add:
            await asyncio.gather(*role_change_tasks_add)  # Wait for all role changes to finish
            #await self.user_handler.save_users()

    # Remove roles if they exceed the threshold
    @tasks.loop(seconds=3)  # Run this task every 3 seconds
    async def remove_roles_exceed(self):
        guild = self.bot.get_guild(settings.GUILDS_ID.id)  # Replace with your guild ID
        users = self.users.get_users()  # Get the users data
        role_change_tasks_exceed = []
        for member in guild.members:
            member_id_str = str(member.id)
            user_data = users.get(member_id_str)
            if user_data:
                points = user_data['points']
                role_id = await self.bot.user_handler.check_threshold(points)
                if role_id:
                    role = guild.get_role(int(role_id))
                    threshold_roles = [guild.get_role(int(role['role_id'])) for role in thresholds]
                    ignore_roles_ids = [
                        settings.Admin_ID.id,
                        settings.ScalBot3_0_ID.id,
                    ]
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position < role.position and member_role.id not in ignore_roles_ids:
                            role_change_tasks_exceed.append(member.remove_roles(member_role, reason="Exceeds current threshold"))
        if role_change_tasks_exceed:
            await asyncio.gather(*role_change_tasks_exceed)  # Wait for all role changes to finish
            #await self.user_handler.save_users()

    # Remove roles if they are above the threshold
    @tasks.loop(seconds=3)  # Run this task every 3 seconds
    async def remove_roles(self):
        guild = self.bot.get_guild(settings.GUILDS_ID.id)  # Replace with your guild ID
        users = self.users.get_users()  # Get the users data
        role_change_tasks_remove = []
        for member in guild.members:
            member_id_str = str(member.id)
            user_data = users.get(member_id_str)
            if user_data:
                points = user_data['points']
                role_id = await self.bot.user_handler.check_threshold(points)
                if role_id:
                    role = guild.get_role(int(role_id))
                    threshold_roles = [guild.get_role(int(role['role_id'])) for role in thresholds]
                    ignore_roles_ids = [
                        settings.Admin_ID.id,
                        settings.ScalBot3_0_ID.id,
                    ]
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position > role.position and member_role.id not in ignore_roles_ids:
                            role_change_tasks_remove.append(member.remove_roles(member_role, reason="Exceeds current threshold"))
        if role_change_tasks_remove:
            await asyncio.gather(*role_change_tasks_remove)  # Wait for all role changes to finish
            #await self.user_handler.save_users()

    # Announcing Levels
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        users = self.bot.user_handler.get_users()
        if str(after.id) in users:
            before_roles = set(before.roles)
            after_roles = set(after.roles)

            added_roles = after_roles - before_roles
            removed_roles = before_roles - after_roles
        
        # Reset points to 0 if Guest role is added - Declining rules
        if any(role.id == settings.Guest_ID.id for role in added_roles):
            self.bot.user_handler._users[str(after.id)]['points'] = 0 
            await self.bot.user_handler.save_users()
        # Reset points to 1 if New Member role is added - Accepting rules
        if any(role.id == settings.New_Member_ID.id for role in added_roles):
            self.bot.user_handler._users[str(after.id)]['points'] = 1 
            await self.bot.user_handler.save_users()
        # Increment muted count if Muted role is added
        if any(role.id == settings.Muted_ID.id for role in added_roles):
            self.bot.user_handler._users[str(after.id)]['muted_count'] += 1 
            await self.bot.user_handler.save_users()

        # Updates user roles in users.json
        if added_roles:
            added_role_names = ', '.join(role.name for role in added_roles)
            print(f"Added roles to: {after.name}: {added_role_names}")
            if after.id in self.role_change_tasks_add and self.role_change_tasks_add[after.id].is_running():
                self.role_change_tasks_add[after.id].cancel()

            member_id_str = str(after.id)
            current_roles = self.bot.user_handler._users[member_id_str]['roles']
            self.bot.user_handler._users[member_id_str]['roles'] = [role for role in current_roles if role not in [r.name for r in removed_roles] and role != settings.Muted_ID.id]
            await self.bot.user_handler.save_users()

            await asyncio.sleep(1)
            if after.id not in self.role_change_tasks_add:
                self.role_change_tasks_add[after.id] = self.send_role_change_message

            try:
                self.role_change_tasks_add[after.id].start(after, added_roles)
            except RuntimeError:
                pass

        if removed_roles:
            removed_role_names = ', '.join(role.name for role in removed_roles)
            print(f"Removed roles from: {after.name}: {removed_role_names}")
            member_id_str = str(after.id)
            # Handle self.role_change_tasks_exceed
            task_exceed = self.role_change_tasks_exceed.get(member_id_str)
            if task_exceed is not None and task_exceed.is_running():
                task_exceed.cancel()
            await asyncio.sleep(1)
            if task_exceed is not None:
                try:
                    task_exceed.start(after, removed_roles)
                except RuntimeError:
                    pass
            # Handle self.role_change_tasks_remove
            task_remove = self.role_change_tasks_remove.get(member_id_str)
            if task_remove is not None and task_remove.is_running():
                task_remove.cancel()
            await asyncio.sleep(1)
            if task_remove is not None:
                try:
                    task_remove.start(after, removed_roles)
                except RuntimeError:
                    pass

    
    # Send message to channel when a role is added - this shit is finiky af
    @tasks.loop(seconds=3, count=1)            
    async def send_role_change_message(self, member, added_roles):
        await asyncio.sleep(1)
        if self.send_role_change_message.current_loop == 0:
            channel = self.last_channel.get(str(member.id))
            if channel is not None:
                role_names = ", ".join(role.name for role in added_roles if role.name != settings.Muted_ID.id) 
                await channel.send(f"{member.mention} has been given the role - {role_names}!")
                member_id_str = str(member.id)
                self.bot.user_handler._users[member_id_str]['roles'] = [role.name for role in member.roles]
                #await self.user_handler.save_users()

    # Points System for Leveling

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.add_roles()
        author_id = str(message.author.id)
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        self.last_channel[author_id] = message.channel
        if message.channel.category_id == settings.Public_Lobby_ID.id or message.channel.id == settings.scalbot_test_ID.id:  
            if author_id in self.bot.user_handler._users:
                self.bot.user_handler._users[author_id]['points'] += 1
                #await self.user_handler.save_users()
            else:
                pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.add_roles()
        author_id = str(user.id)
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        if reaction.message.channel.category_id == settings.Public_Lobby_ID.id or reaction.message.channel.id == settings.scalbot_test_ID.id:
            if author_id in self.bot.user_handler._users:
                self.bot.user_handler._users[author_id]['points'] += 3
                #await self.user_handler.save_users()
            else:
                pass

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.add_roles()
        author_id = str(user.id)
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        if reaction.message.channel.category_id == settings.Public_Lobby_ID.id or reaction.message.channel.id == settings.scalbot_test_ID.id:
            if author_id in self.bot.user_handler._users:
                self.bot.user_handler._users[author_id]['points'] -= 3
                #await self.user_handler.save_users()
            else:
                pass       

async def setup(bot):
    await bot.add_cog(LevelingCog(bot))
