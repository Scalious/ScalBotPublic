import discord
import json
import settings

from discord.ext import commands

import asyncio

from thresholds import thresholds

logger = settings.logging.getLogger("bot")

class UserHandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot # Save the bot instance
        self._users = {} # Create an empty dictionary to store the users
        self._lock = asyncio.Lock() #
        self.bot.loop.create_task(self.load_users()) # Load the users from the file
        self.bot.loop.create_task(self.save_users_periodically()) # Save the users periodically
        self.update_interval = 5 # Save users every 5 seconds

    # Getters
    def get_users(self):
        return self._users 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.type == discord.MessageType.premium_guild_subscription:
            await self.add_roles()
            author_id = str(message.author.id)
            await message.author.add_roles(author_id)
    
    # Setters
    async def save_users_periodically(self):
        while True:
            await asyncio.sleep(self.update_interval)        
            async with self._lock:
                with open('users.json', 'w') as file:
                    json.dump(self._users, file, indent=4)

    async def add_member(self, member_id, display_name, points, roles, joined_at, mutes, last_message_time):
        async with self._lock:
            if member_id not in self._users:
                self._users[member_id] = {
                    'member_id': member_id,
                    'display_name': display_name,
                    'points': points if points is not None else 0,
                    'roles': [role.name for role in roles[1:]],
                    'joined_at': joined_at.isoformat(),
                    'muted_count': mutes if mutes is not None else 0,
                    'last_message_time': last_message_time.isoformat() if last_message_time is not None else ''
                }
            else:
                if points is not None:
                    self._users[member_id]['points'] = points
                if mutes is not None:
                    self._users[member_id]['muted_count'] = mutes
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
    
    async def next_threshold(self, points): 
        thresholds.sort(key=lambda x: x['threshold'])
        for role in thresholds:
            if points <= role['threshold']:
                return role['threshold'] 
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
    await bot.add_cog(bot.user_handler)  # Add the same UserHandler instance as a cog    {'threshold': 0, 'role_id': 787746412820824074},


