import discord, settings, json
from discord.ext import commands, tasks
from datetime import datetime, timedelta, timezone

class ActivityCheckerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_channel = {} 
        self.check_activity_weekly.start()
        self.check_activity_5_weeks.start()
        self.users = self.bot.user_handler

    # Add timestamp of user's last message to user.json
    @commands.Cog.listener()
    async def on_message(self, message):
        author_id = str(message.author.id)
        if type(message.channel) is not discord.TextChannel or message.author.bot: return
        self.last_channel[author_id] = message.channel  # ignore DMs and bots
        if message.channel.category_id == settings.Public_Lobby_ID.id or message.channel.id == settings.scalbot_test_ID.id:  
            if author_id in self.bot.user_handler._users:
                self.bot.user_handler._users[author_id]['last_message_time'] = message.created_at.isoformat()
                #await self.user_handler.save_users()
            else:
                pass

    # Check activity every week
    @tasks.loop(hours=168)  # Loop every week
    async def check_activity_weekly(self):
        current_time = datetime.now(tz=timezone.utc)
        with open('user.json', 'r') as file:
            user_data = json.load(file)

        for user_id, user_info in user_data.items():
            if 'last_message_time' not in user_info:
                user_info['last_message_time'] = datetime.now(tz=timezone.utc).isoformat()
            last_message_time = datetime.fromisoformat(user_info['last_message_time'])
            time_difference = current_time - last_message_time
            if time_difference > timedelta(hours=168):
                user_info['last_message_time'] = current_time.isoformat()
                guild = self.bot.get_guild(settings.GUILDS_ID.id)
                if guild is not None:
                    # Get the member
                    member = guild.get_member(user_id)
                    if member is not None:
                        # Send a message to the member
                        await member.send("You have been inactive for a week. Inactivity of a month results in a ban")

    # Check activity every 5 weeks
    @tasks.loop(hours=840)  # Loop every 5 weeks
    async def check_activity_5_weeks(self):
        current_time = datetime.now(tz=timezone.utc)
        with open('user.json', 'r') as file:
            user_data = json.load(file)

        for user_id, user_info in user_data.items():
            last_message_time = datetime.fromisoformat(user_info['last_message_time'])
            time_difference = current_time - last_message_time
            if time_difference > timedelta(hours=840):
                user_info['last_message_time'] = current_time.isoformat()

                guild = self.bot.get_guild(settings.GUILDS_ID.id)
                if guild is not None:
                    # Get the member
                    member = guild.get_member(user_id)
                    if member is not None:
                        # Send a message to the member
                        await member.ban("You have been inactive for 5 weeks")

async def setup(bot):
    await bot.add_cog(ActivityCheckerCog(bot))
