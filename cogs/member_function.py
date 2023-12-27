import discord
import json

from discord.ext import commands

#users = {}

thresholds = [
    {'threshold': 5, 'role_id': "1189245504912113664"},  # New Member
    {'threshold': 10, 'role_id': "1189244962940911698"},  # Member
    {'threshold': 200, 'role_id': "1189311831412588644"},  # Super Member
]

class UserHandler(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self._users = {}

    def get_users(self):
        return self._users

    async def add_member(self, member_id, display_name, points=None):
        if member_id not in self._users:
            self._users[member_id] = {
                'member_id': member_id,
                'display_name': display_name,
                'points': points if points is not None else 0
            }
        else:
            if points is not None:
                self._users[member_id]['points'] = points

    async def check_threshold(self, points): 
        global users
        thresholds.sort(key=lambda x: x['threshold'], reverse=True)
        for role in thresholds:
            if points >= role['threshold']:
                return role['role_id'] 
        return None

    # this function does not correctly update the users points or save them between bot restarts and must be cleared or delete the users.txt file
    async def save_users(self):
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
    user_handler = UserHandler(bot)
    await user_handler.load_users()
    await bot.add_cog(UserHandler(bot))





# async def add_member(member_id, display_name, points=None):
#     global users
#     if member_id not in users:  # Only add the user if they're not already in the dictionary
#         users[member_id] = {
#             'member_id': member_id,
#             'display_name': display_name,
#             'points': points if points is not None else 0
#         }
#     else:  # If the user is already in the dictionary
#         if points is not None:
#             users[member_id]['points'] = points  # Update the points if provided

# async def check_threshold(member_id, points): 
#     global users
#     thresholds.sort(key=lambda x: x['threshold'], reverse=True)
#     for role in thresholds: # 
#         if points >= role['threshold']: # 
#             return role['role_id'] #
#     return None

# async def save_users():
#     with open('users.txt', 'w') as f:
#         json.dump(users, f)

# async def load_users():
#     global users
#     try:
#         with open('users.txt', 'r') as f:
#             data = json.load(f)
#             users.clear()
#             users.update(data)
#     except FileNotFoundError:
#         pass  # Clear the users dictionary instead of assigning a new dictionary to users

