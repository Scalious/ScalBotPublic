import discord, settings
from discord.ext import commands

from discord.ext import tasks

import cogs.member_function as mf

from cogs.member_function import UserHandler

# Leveling is only possible in the Public Lobby: lounge channel currently

class LevelingCog(commands.Cog):

    def __init__(self, bot, user_handler):
        self.bot = bot
        self.add_roles.start()
        self.remove_roles_exceed.start()
        self.remove_roles.start()
        self.update_counter = 0
        self.user_handler = user_handler  

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
                    if role not in member.roles:  # Check if the user already has the role
                        await member.add_roles(role, reason="Passed a new threshold")
                        await self.user_handler.save_users()
                        print(f"Added {role.name} to {member.name}")
                        channel = self.bot.get_channel(settings.scalbot_test_ID.id)  # Set to the test channel - 
                        await channel.send(f"{member.mention} has been given the new role {role.name}!")
            else:
                await self.user_handler.add_member(member_id_str, member.display_name, 1)# Check if the user is in the dictionary
        await self.user_handler.save_users() #  Save users to file

    # Remove roles if they exceed the threshold
    @tasks.loop(seconds=7)  # Run this task every 6 seconds
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
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position < role.position:
                            await member.remove_roles(member_role, reason="Exceeds current threshold")
                            print(f"Removed {member_role.name} from {member.name}")
                            # channel = self.bot.get_channel(settings.scalbot_test_ID.id)  # Set to the test channel - 
                            # await channel.send(f"The Role {member_role.name} has been removed from {member.mention}!")

    # Remove roles if they previously had a higher threshold
    @tasks.loop(seconds=7)  # Run this task every 6 seconds
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
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position > role.position:
                            await member.remove_roles(member_role, reason="Exceeds current threshold")
                            print(f"Removed {member_role.name} from {member.name}")
                            # channel = self.bot.get_channel(settings.scalbot_test_ID.id)  # Set to the test channel - 
                            # await channel.send(f"The Role {member_role.name} has been removed from {member.mention}!")

    # Points System for Leveling

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.add_roles()
        author_id = str(message.author.id)
        if type(message.channel) is not discord.TextChannel or message.author.bot: return  # ignore DMs and bots
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
