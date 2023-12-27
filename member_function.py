import discord

users = {}

thresholds = [
    {'threshold': 5, 'role_id': "1189245504912113664"},  # New Member
    {'threshold': 10, 'role_id': "1189244962940911698"},  # Member
    {'threshold': 200, 'role_id': "1189311831412588644"},  # Super Member
]

async def add_member(member_id, nickname, points):
    global users
    users[member_id] = {
        'member_id': member_id,
        'nickname': nickname,
        'points': points
    }

async def check_threshold(member_id, points): # 
    global users
    thresholds.sort(key=lambda x: x['threshold'], reverse=True)
    for role in thresholds: # 
        if points >= role['threshold']: # 
            return role['role_id'] #
    return None

async def check_roles(member: discord.Member, role_id: int):
    # Get all role IDs that the member has
    member_role_ids = [role.id for role in member.roles]

    # Check if the role_id is in the member's role IDs
    has_role = role_id in member_role_ids

    return has_role
