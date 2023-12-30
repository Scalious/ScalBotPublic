import discord
from discord.ext import commands
from datetime import timedelta

import re
import collections
import logging

import asyncio

import settings
logger = settings.logging.getLogger("bot")

LINK_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
MESSAGE_LIMIT = 7 #number of messages before warnings in 15 seconds
LINK_LIMIT = 4 #number of links before warmings in 30 seconds
REACTION_LIMIT = 10 #number of reactions before warnings in 15 seconds    
VIOLATION_LIMIT = 4 #number of violations before timeout in 60 seconds
TIMEOUT_DURATION = 10 #minutes 
DELETE_AFTER = 5 #seconds

class Antispam(commands.Cog):
    """A cog for preventing spam in a Discord server."""

    def __init__(self, bot):
        self.bot = bot
        self.anti_spam_message = commands.CooldownMapping.from_cooldown(MESSAGE_LIMIT, 15, commands.BucketType.member) # messages in 15 seconds
        self.anti_spam_message_links = commands.CooldownMapping.from_cooldown(LINK_LIMIT, 30, commands.BucketType.member) # links in 30 seconds
        self.anti_spam_reaction = commands.CooldownMapping.from_cooldown(REACTION_LIMIT, 15, commands.BucketType.member) # reactions in 15 seconds
        self.too_many_violations = commands.CooldownMapping.from_cooldown(VIOLATION_LIMIT, 60, commands.BucketType.member) # violations in 60 seconds

        self.message_cache = collections.defaultdict(list)
        self.user_spam_count = {}

    def is_link(self, message):
        """Check if the message is a link."""
        return re.search(LINK_REGEX, message)
    
    # User Mute ban threshold check
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        guild = self.bot.get_guild(settings.GUILDS_ID.id)  # Replace with your guild ID
        self.user_handler = self.bot.get_cog("UserHandler")
        await self.user_handler.load_users()
        users = self.user_handler.get_users()
        for member in guild.members:
            member_id_str = str(member.id)
            if member_id_str in users:  
                mutes = users[member_id_str]['muted_count']  # Get the user's mutes from the dictionary
                if mutes > 3:
                    await member.ban(reason="Exceeded mute limit")

    # Timeout spammer & mute - auto mute & unmute after 10 minutes 
    async def timeout_spam(self, message, author, reason):
        """Timeout a spammer."""
        await author.timeout(timedelta(minutes = TIMEOUT_DURATION), reason=reason)
        muted_role = discord.utils.get(message.guild.roles, id=settings.Muted_ID.id)
        await author.add_roles(muted_role)
        try:
            await author.send(f"You have been muted for {reason}!")
        except Exception as e:
            logging.error(f"Error sending DM: {e}")
        
        await asyncio.sleep(TIMEOUT_DURATION)
        await author.remove_roles(muted_role)

    # Spam handler
    async def handle_spam(self, message, spam_type):
        """Handle a spam violation."""
        for msg in self.message_cache[message.channel.id]:
            if msg.author == message.author and (spam_type == "links" and self.is_link(msg.content) or spam_type == "messages"):
                try:
                    await msg.delete()
                except Exception as e:
                    logging.error(f"Error deleting message: {e}")
        await message.channel.send(f"{message.author.mention}, don't spam {spam_type}!", delete_after = DELETE_AFTER)
        violations = self.too_many_violations.get_bucket(message)
        check = violations.update_rate_limit()
        if check:
            if any(role.id == settings.Admin_ID.id for role in message.author.roles):
                await message.channel.send(f"Powwa ABUUSE! {message.author.mention}")
                return
            await self.timeout_spam(message, message.author, f"Spamming {spam_type}! You have been timed out for {TIMEOUT_DURATION} minutes.")

    @commands.Cog.listener()
    async def on_message(self, message):
        self.message_cache[message.author.id].append(message)
        if len(self.message_cache[message.author.id]) > MESSAGE_LIMIT:
            self.message_cache[message.author.id].pop(0) 
        if not isinstance(message.channel, discord.TextChannel) or message.author.bot:
            return

        if self.is_link(message.content):
            bucket = self.anti_spam_message_links.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await self.handle_spam(message, "links")
        else:
            bucket = self.anti_spam_message.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await self.handle_spam(message, "messages")      

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not isinstance(reaction.message.channel, discord.TextChannel) or user.bot:
            return
        bucket = self.anti_spam_reaction.get_bucket(reaction.message)
        retry_after = bucket.update_rate_limit()
        check = False
        if retry_after:
            await reaction.message.channel.send(f"{user.mention}, don't spam reactions!", delete_after = DELETE_AFTER)
            violations = self.too_many_violations.get_bucket(reaction.message)
            check = violations.update_rate_limit()
        if check:
            await self.handle_spam(reaction.message, user, "spamming reactions")

async def setup(bot):
    await bot.add_cog(Antispam(bot))


