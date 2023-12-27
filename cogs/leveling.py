import discord
from discord.ext import commands

from collections import defaultdict

from discord.ext import tasks

#from datetime import datetime

# Leveling is only possible in the Public Lobby: lounge channel currently

class LevelingCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.points = defaultdict(int)
        #self.save_points.start()
        self.check_thresholds.start()
        self.thresholds = {
            5: "1189245504912113664", # New Member
            10: "1189244962940911698", # Member
            200: "1189311831412588644", # Super Member
        }
    
    #@tasks.loop(minutes=10.0)  # Run this task every 10 minutes
    # @tasks.loop(seconds=10.0)  # Run this task every 10 seconds
    # async def save_points(self):
    #     print("Saving points...")
    #     with open('points.txt', 'a') as f:  # Change 'w' to 'a' to append
    #         for user_id, points in self.points.items():
    #             guild = self.bot.get_guild(787746412820824074)  # Replace with your guild ID
    #             member = await guild.fetch_member(user_id)
    #             roles = ", ".join([role.name for role in member.roles if role.name != "@everyone"])
    #             f.write(f'Timestamp: {datetime.now()}, User ID: {user_id}, Points: {points}, Roles: {roles}\n')
    #     print("Points saved.")
    
    # problem is this will not remove lower ranks if you have a higher rank. This is because it is looping through all thresholds and adding them if they are met. 
    # I think you need to loop through all thresholds and remove them if they are not met.
    
    # @tasks.loop(minutes=0.50)  # Run this task every 30 seconds
    # async def check_thresholds(self): # Check if any users have passed a threshold
    #     for user_id in self.points: # Loop through all users
    #         guild = self.bot.get_guild(787746412820824074) # Replace with your guild ID
    #         member = await guild.fetch_member(user_id)
    #         for threshold, role_id in sorted(self.thresholds.items(), reverse=True): # Loop through all thresholds in descending order
    #             role = guild.get_role(int(role_id))
    #             if self.points[user_id] >= threshold: # If the user has passed a threshold
    #                 if role not in member.roles:  # Check if the user already has the role
    #                     await member.add_roles(role)
    #                     print(f"Added {role.name} to {member.name}")
    #             else:
    #                 if role in member.roles:  # Check if the user has the role
    #                     await member.remove_roles(role)
    #                     print(f"Removed {role.name} from {member.name}")

    @tasks.loop(minutes=0.50)  # Run this task every 30 seconds
    async def check_thresholds(self): # Check if any users have passed a threshold
        for user_id in self.points: # Loop through all users
            guild = self.bot.get_guild(787746412820824074) # Replace with your guild ID
            member = await guild.fetch_member(user_id)
            highest_role = max((role for role in member.roles if role.id in self.thresholds.values()), key=lambda role: self.thresholds.get(str(role.id)), default=None)
            highest_threshold = self.thresholds.get(str(highest_role.id)) if highest_role else 0
            for threshold, role_id in self.thresholds.items():
                if self.points[user_id] >= int(threshold) > highest_threshold: # If the user has passed a higher threshold
                    role = guild.get_role(int(role_id))
                    if role not in member.roles:  # Check if the user already has the role
                        # Remove the current highest role
                        if highest_role:
                            await member.remove_roles(highest_role, reason="Passed a higher threshold")
                            print(f"Passed a higher threshold, removed {highest_role.name}")
                        # Add the new role
                        await member.add_roles(role, reason="Passed a new threshold")
                        print(f"Added {role.name} to {member.name}")
                        break  # Break the loop as soon as a higher threshold is exceeded

    # Test Command to check if the thresholds are working
    @commands.command(
            enabled=True,
            hidden=True,
    )
    async def test_check_thresholds(self, ctx):
        await self.check_thresholds()
        print(f'User ID: {ctx.author.id}, Points: {self.points[ctx.author.id]}')

    @commands.Cog.listener()
    async def on_message(self, message):
        if type(message.channel) is not discord.TextChannel or message.author.bot: return  # ignore DMs and bots
        # Check if the message is sent in the specific channel you want to listen to
        if message.channel.id == 1189280239432519824:
            self.points[message.author.id] += 1
               
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return # ignore DMs and bots
        # Check if the reaction is added in the specific channel you want to listen to
        if reaction.message.channel.id == 1189280239432519824:
            self.points[user.id] += 1          

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return
        # Check if the reaction is removed in the specific channel you want to listen to
        if reaction.message.channel.id == 1189280239432519824:
            self.points[user.id] -= 1          

async def setup(bot):
    await bot.add_cog(LevelingCog(bot))
