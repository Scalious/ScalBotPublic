import discord
from discord.ext import commands

from discord.ext import tasks

import cogs.member_function as mf
#from cogs.member_function import add_member, users, check_threshold
#from cogs.member_function import users

#from cogs.member_function import save_users, load_users
from cogs.member_function import UserHandler

#from datetime import datetime

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
    @tasks.loop(minutes=0.50)  # Run this task every 30 seconds
    async def add_roles(self):
        guild = self.bot.get_guild(787746412820824074)  # Replace with your guild ID
        for member in guild.members: # Loop through all members in the guild
            if member.id not in self.user_handler._users: # If the user is not in the dictionary
                await self.user_handler.add_member(member.id, member.display_name, 0) # Add the user to the dictionary
            users = self.user_handler.get_users()
            if member.id in users:  # Check if the user is in the dictionary
                points = users[member.id]['points']  # Get the user's points from the dictionary
                role_id = await self.user_handler.check_threshold(points) 
                if role_id:
                    role = guild.get_role(int(role_id))
                    if role not in member.roles:  # Check if the user already has the role
                        await member.add_roles(role, reason="Passed a new threshold")
                        await self.user_handler.save_users()
                        print(f"Added {role.name} to {member.name}")
        await self.user_handler.save_users() #  Save users to file

    # Remove roles if they exceed the threshold
    @tasks.loop(minutes=0.50)  # Run this task every 30 seconds
    async def remove_roles_exceed(self):
        guild = self.bot.get_guild(787746412820824074)  # Replace with your guild ID
        for member in guild.members:
            users = self.user_handler.get_users()
            if member.id in users:
                points = users[member.id]['points']
                role_id = await self.user_handler.check_threshold(points)
                if role_id:
                    role = guild.get_role(int(role_id))
                    threshold_roles = [guild.get_role(int(role['role_id'])) for role in mf.thresholds]
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position < role.position:
                            await member.remove_roles(member_role, reason="Exceeds current threshold")
                            print(f"Removed {member_role.name} from {member.name}")

    # Remove roles if they previously had a higher threshold
    @tasks.loop(minutes=0.50)  # Run this task every 30 seconds
    async def remove_roles(self):
        guild = self.bot.get_guild(787746412820824074)  # Replace with your guild ID
        for member in guild.members:
            users = self.user_handler.get_users()
            if member.id in users:
                points = users[member.id]['points']
                role_id = await self.user_handler.check_threshold(points)
                if role_id:
                    role = guild.get_role(int(role_id))
                    threshold_roles = [guild.get_role(int(role['role_id'])) for role in mf.thresholds]
                    for member_role in member.roles:
                        if member_role in threshold_roles and member_role.position > role.position:
                            await member.remove_roles(member_role, reason="Exceeds current threshold")
                            print(f"Removed {member_role.name} from {member.name}")

    # Test Commands

    @commands.command()
    async def print_users(self, ctx):
        await self.add_roles()
        users = self.user_handler.get_users()
        print(f'User ID: {ctx.author.id}, Points: {users[ctx.author.id]["points"]}')
        await ctx.send(f'Users: {users}')
 
    @commands.command()
    async def purge_channel(self, ctx):
        channel = ctx.channel
        await channel.purge()
        await ctx.send("Channel purged successfully.")

    # Points System for Leveling

    @commands.Cog.listener()
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return  # ignore DMs and bots
        # Check if the message is sent in the specific channel you want to listen to
        if message.channel.id == 1189280239432519824 or message.channel.id == 986395646632296548:
            if message.author.id in self.user_handler._users:
                self.user_handler._users[message.author.id]['points'] += 1
                self.update_counter += 1
                if self.update_counter == 5: 
                    await self.user_handler.save_users()
                    self.update_counter = 0
            else:
                #await mf.add_member(message.author.id, message.author.name, 1)
                pass

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        # Check if the reaction is added in the specific channel you want to listen to
        if reaction.message.channel.id == 1189280239432519824 or reaction.message.channel.id == 986395646632296548:
            if user.id in self.user_handler._users:
                self.user_handler._users[user.id]['points'] += 3
                await self.user_handler.save_users()
            else:
                #await mf.add_member(user.id, user.name, 300)
                pass

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        # Check if the reaction is added in the specific channel you want to listen to
        if reaction.message.channel.id == 1189280239432519824 or reaction.message.channel.id == 986395646632296548:
            if user.id in self.user_handler._users:
                self.user_handler._users[user.id]['points'] -= 3
                await self.user_handler.save_users()
            else:
                #await mf.add_member(user.id, user.name, 300)
                pass       

async def setup(bot):
    user_handler = UserHandler(bot)
    await bot.add_cog(LevelingCog(bot, user_handler))
