import discord
import json
import settings

from discord.ext import commands

import asyncio

from thresholds import thresholds

logger = settings.logging.getLogger("bot")

class UserHandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._users = {}
        self._lock = asyncio.Lock()
        self.bot.loop.create_task(self.load_users())

    def get_users(self):
        return self._users

    async def add_member(self, member_id, display_name, points, roles, joined_at):
        async with self._lock:
            if member_id not in self._users:
                self._users[member_id] = {
                    'member_id': member_id,
                    'display_name': display_name,
                    'points': points if points is not None else 0,
                    'roles': [role.name for role in roles],
                    'joined_at': joined_at.isoformat(),
                }
            else:
                if points is not None:
                    self._users[member_id]['points'] = points
                self._users[member_id]['display_name'] = display_name
                self._users[member_id]['roles'] = [role.name for role in roles]

            # Write the users to the file
            with open('users.json', 'w') as f:
                json.dump(self._users, f, indent=4)

    async def check_threshold(self, points): 
        thresholds.sort(key=lambda x: x['threshold'], reverse=True)
        for role in thresholds:
            if points >= role['threshold']:
                return role['role_id'] 
        return None

    async def save_users(self):
        async with self._lock:
            with open('users.json', 'w') as f:
                json.dump(self._users, f, indent=4)

    async def load_users(self):
        try:
            with open('users.json', 'r') as f:
                data = json.load(f)
                self._users = data
        except FileNotFoundError:
            print("Error: 'users.json' not found.")
        except PermissionError:
            print("Error: Permission denied when trying to read 'users.json'.")
        except json.JSONDecodeError:
            print("Error: 'users.json' contains invalid JSON.")

async def setup(bot):
    bot.user_handler = UserHandler(bot)  # Create a new UserHandler instance and add it as an attribute to the bot
    await bot.user_handler.load_users()  # Load users from file
    await bot.add_cog(bot.user_handler)  # Add the same UserHandler instance as a cog    {'threshold': 0, 'role_id': 787746412820824074},


