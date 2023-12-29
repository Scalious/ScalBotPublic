import discord
import json
import settings

from discord.ext import commands

import asyncio

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
    {'threshold': 1, 'role_id': 1190053473186758717},
    {'threshold': 4, 'role_id': 1190053306953900162},
    {'threshold': 9, 'role_id': 1190053221553680464},
    {'threshold': 16, 'role_id': 1190053142906294373},
    {'threshold': 25, 'role_id': 1189255069082853527},
    {'threshold': 36, 'role_id': 787747687675199508},
    {'threshold': 49, 'role_id': 1189245504912113664},
    {'threshold': 64, 'role_id': 1189244962940911698},
    {'threshold': 81, 'role_id': 1189311831412588644},
    {'threshold': 100, 'role_id': 1188282870347870232},
    {'threshold': 121, 'role_id': 787747360398770176},

]

    {'threshold': 0, 'role_id': 787746412820824074},
    {'threshold': 1, 'role_id': 1190053473186758717},
    {'threshold': 4, 'role_id': 1190053306953900162},
    {'threshold': 9, 'role_id': 1190053221553680464},
    {'threshold': 16, 'role_id': 1190053142906294373},
    {'threshold': 25, 'role_id': 1189255069082853527},
    {'threshold': 36, 'role_id': 787747687675199508},
    {'threshold': 49, 'role_id': 1189245504912113664},
    {'threshold': 64, 'role_id': 1189244962940911698},
    {'threshold': 81, 'role_id': 1189311831412588644},
    {'threshold': 100, 'role_id': 1188282870347870232},
    {'threshold': 121, 'role_id': 787747360398770176},

]

    {'threshold': 0, 'role_id': 787746412820824074},
    {'threshold': 1, 'role_id': 1190053473186758717},
    {'threshold': 4, 'role_id': 1190053306953900162},
    {'threshold': 9, 'role_id': 1190053221553680464},
    {'threshold': 16, 'role_id': 1190053142906294373},
    {'threshold': 25, 'role_id': 1189255069082853527},
    {'threshold': 36, 'role_id': 787747687675199508},
    {'threshold': 49, 'role_id': 1189245504912113664},
    {'threshold': 64, 'role_id': 1189244962940911698},
    {'threshold': 81, 'role_id': 1189311831412588644},
    {'threshold': 100, 'role_id': 1188282870347870232},
    {'threshold': 121, 'role_id': 787747360398770176},

]

    {'threshold': 0, 'role_id': 787746412820824074},
    {'threshold': 1, 'role_id': 1190053473186758717},
    {'threshold': 4, 'role_id': 1190053306953900162},
    {'threshold': 9, 'role_id': 1190053221553680464},
    {'threshold': 16, 'role_id': 1190053142906294373},
    {'threshold': 25, 'role_id': 1189255069082853527},
    {'threshold': 36, 'role_id': 787747687675199508},
    {'threshold': 49, 'role_id': 1189245504912113664},
    {'threshold': 64, 'role_id': 1189244962940911698},
    {'threshold': 81, 'role_id': 1189311831412588644},
    {'threshold': 100, 'role_id': 1188282870347870232},
    {'threshold': 121, 'role_id': 787747360398770176},

]

