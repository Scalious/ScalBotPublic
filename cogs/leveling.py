import discord
from discord.ext import commands

from discord.ext import tasks

import member_function as mf
from member_function import add_member, users, check_threshold, check_roles

#from datetime import datetime

# Leveling is only possible in the Public Lobby: lounge channel currently

class LevelingCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.add_roles.start()
        self.remove_roles_exceed.start()
        self.remove_roles.start()

    # Add roles if they pass a new threshold
    @tasks.loop(minutes=0.50)  # Run this task every 30 seconds
    async def add_roles(self):
        guild = self.bot.get_guild(787746412820824074)  # Replace with your guild ID
        for member in guild.members:
            if member.id not in mf.users:
                await mf.add_member(member.id, member.display_name, 0)
            points = mf.users[member.id]['points']  # or get the points from somewhere else
            role_id = await mf.check_threshold(member.id, points) 
            if role_id:
                role = guild.get_role(int(role_id))
                if role not in member.roles:  # Check if the user already has the role
                    await member.add_roles(role, reason="Passed a new threshold")
                    print(f"Added {role.name} to {member.name}")

    # Remove roles if they exceed the threshold
    @tasks.loop(minutes=0.50)  # Run this task every 30 seconds
    async def remove_roles_exceed(self):
        guild = self.bot.get_guild(787746412820824074)  # Replace with your guild ID
        for member in guild.members:
            if member.id in mf.users:
                points = mf.users[member.id]['points']
                role_id = await mf.check_threshold(member.id, points)
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
            if member.id in mf.users:
                points = mf.users[member.id]['points']
                role_id = await mf.check_threshold(member.id, points)
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
        print(f'User ID: {ctx.author.id}, Points: {mf.users[ctx.author.id]["points"]}')
        matching_roles = await mf.check_roles(ctx.message.author, mf.thresholds)
        print(f'Matching Roles: {matching_roles}')
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
        if message.channel.id == 1189280239432519824 or message.channel.id == 1189434792622706728:
            if message.author.id in mf.users:
                mf.users[message.author.id]['points'] += 1
            else:
                await mf.add_member(message.author.id, message.author.name, 1)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        # Check if the reaction is added in the specific channel you want to listen to
        if reaction.message.channel.id == 1189280239432519824 or reaction.message.channel.id == 986395646632296548:
            if user.id in mf.users:
                mf.users[user.id]['points'] += 300
            else:
                await mf.add_member(user.id, user.name, 300)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return  # ignore DMs and bots
        # Check if the reaction is added in the specific channel you want to listen to
        if reaction.message.channel.id == 1189280239432519824 or reaction.message.channel.id == 1189434792622706728:
            if user.id in mf.users:
                mf.users[user.id]['points'] -= 300
            else:
                await mf.add_member(user.id, user.name, 300)       

async def setup(bot):
    await bot.add_cog(LevelingCog(bot))
