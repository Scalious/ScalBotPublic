import discord
import json
import settings

from discord.ext import commands

import asyncio

# This works but the threshold roles are not in the same order below
#from thresholds import thresholds

thresholds = [
    {'threshold': 0, 'role_id': settings.Guest_ID.id},  # Guest
    {'threshold': 1, 'role_id': settings.New_Member_ID.id},  # New Member
    {'threshold': 10, 'role_id': settings.Member_ID.id},  # Member
    {'threshold': 200, 'role_id': settings.Super_Member_ID.id},  # Super Member
]

class UserHandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._users = {}
        self._lock = asyncio.Lock()
        self.bot.loop.create_task(self.load_users())

    def get_users(self):
        return self._users

    async def add_member(self, member_id, display_name, points=None):
        async with self._lock:
            if member_id not in self._users:
                self._users[member_id] = {
                    'member_id': member_id,
                    'display_name': display_name,
                    'points': points if points is not None else 0
                }
            else:
                if points is not None:
                    self._users[member_id]['points'] = points

            # Write the users to the file
            with open('users.txt', 'w') as f:
                json.dump(self._users, f)

    async def check_threshold(self, points): 
        thresholds.sort(key=lambda x: x['threshold'], reverse=True)
        for role in thresholds:
            if points >= role['threshold']:
                return role['role_id'] 
        return None

    async def save_users(self):
        async with self._lock:
            with open('users.txt', 'w') as f:
                json.dump(self._users, f)

    async def load_users(self):
        try:
            with open('users.txt', 'r') as f:
                data = json.load(f)
                self._users = data
        except FileNotFoundError:
            print("Error: 'users.txt' not found.")
        except PermissionError:
            print("Error: Permission denied when trying to read 'users.txt'.")
        except json.JSONDecodeError:
            print("Error: 'users.txt' contains invalid JSON.")

async def setup(bot):
    bot.user_handler = UserHandler(bot)  # Create a new UserHandler instance and add it as an attribute to the bot
    await bot.user_handler.load_users()  # Load users from file
    await bot.add_cog(bot.user_handler)  # Add the same UserHandler instance as a cog    {'threshold': 0, 'role_id': 787746412820824074},


