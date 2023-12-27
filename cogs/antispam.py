import discord
from discord.ext import commands
from datetime import timedelta

import re
import collections

import settings

class Antispam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.anti_spam_message = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member) #5 messages in 15 seconds
        self.anti_spam_message_links = commands.CooldownMapping.from_cooldown(4, 30, commands.BucketType.member) #4 links in 30 seconds
        self.anti_spam_reaction = commands.CooldownMapping.from_cooldown(10, 15, commands.BucketType.member) #5 reactions in 15 seconds
        self.too_many_violations = commands.CooldownMapping.from_cooldown(2, 60, commands.BucketType.member) #3 violations in 60 seconds

        self.message_cache = collections.defaultdict(list)  # A cache for messages
    
    @commands.Cog.listener()
    async def on_message(self, message): #when a message is sent
        self.message_cache[message.author.id].append(message) #add the message to the cache
        if len(self.message_cache[message.author.id]) > 5: #if the user has sent more than 5 messages
            self.message_cache[message.author.id].pop(0) #remove the first message from the cache
        if type(message.channel) is not discord.TextChannel or message.author.bot: return  #ignore DMs and bots
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.content):
            bucket = self.anti_spam_message_links.get_bucket(message) #
            retry_after = bucket.update_rate_limit() #returns the time left before the cooldown is over
            if retry_after: #if the user has violated the cooldown
                # Get the history of messages in the channel
                for msg in self.message_cache[message.channel.id]:
                    if msg.author == message.author and re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg.content):
                        await msg.delete()  # Delete the message
                await message.channel.send(f"{message.author.mention}, don't spam links!", delete_after = 10) #sends a message to the channel
                violations = self.too_many_violations.get_bucket(message) #checks if the user has violated the cooldown
                check = violations.update_rate_limit() #returns the time left before the cooldown is over
                if check: #if the user has violated the cooldown
                    if any(role.id == settings.ADMIN_ID for role in message.author.roles):
                        await message.channel.send(f"Powwa ABUUSE! {message.author.mention}")
                        return  # Don't timeout admins or the owner
                    await message.author.timeout(timedelta(minutes = 10), reason = "Spamming links") #mutes the user for 10 minutes
                    try: await message.author.send("You have been muted for spamming links!") #sends a DM to the user
                    except: pass 
                else:
                    return
        else:
            bucket = self.anti_spam_message.get_bucket(message)
            retry_after = bucket.update_rate_limit() #returns the time left before the cooldown is over
            if retry_after: #if the user has violated the cooldown
                await message.delete() #deletes the message
                await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 6) #sends a message to the channel
                violations = self.too_many_violations.get_bucket(message) #checks if the user has violated the cooldown
                check = violations.update_rate_limit() #returns the time left before the cooldown is over
                if check: #if the user has violated the cooldown
                    if any(role.id == settings.ADMIN_ID for role in message.author.roles):
                        await message.channel.send(f"Powwa ABUUSE! {message.author.mention}")
                        return  # Don't timeout admins or the owner
                    await message.author.timeout(timedelta(minutes = 10), reason = "Spamming") #mutes the user for 10 minutes
                    try: await message.author.send("You have been muted for spamming!") #sends a DM to the user
                    except: pass #if the user has DMs disabled, it will ignore the error

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if type(reaction.message.channel) is not discord.TextChannel or user.bot: return
        bucket = self.anti_spam_reaction.get_bucket(reaction.message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            await reaction.message.channel.send(f"{user.mention}, don't spam reactions!", delete_after = 10)
            violations = self.too_many_violations.get_bucket(reaction.message)
            check = violations.update_rate_limit()
            if check:
                await user.timeout(timedelta(minutes = 10), reason = "Spamming reactions")
                try: await user.send("You have been muted for spamming reactions!")
                except: pass

async def setup(bot):
    await bot.add_cog(Antispam(bot))






























































# import discord
# from discord.ext import commands
# from datetime import timedelta

# class Antispam(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot
#         intents = discord.Intents.default() #antispam doesn't need message content intent
#         super().__init__(intents = intents)
#         self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member)
#         self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member)

#     @commands.Cog.listener()
#     async def on_ready(self):
#         print(f'We have logged in as {self.bot.user}.')
#         await self.bot.add_cog(Antispam(self.bot))  # Load the Antispam cog

#     @commands.Cog.listener()
#     async def on_message(self, message):
#         if type(message.channel) is not discord.TextChannel or message.author.bot: return
#         bucket = self.anti_spam.get_bucket(message)
#         retry_after = bucket.update_rate_limit()
#         if retry_after:
#             await message.delete()
#             await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 10)
#             violations = self.too_many_violations.get_bucket(message)
#             check = violations.update_rate_limit()
#             if check:
#                 await message.author.timeout(timedelta(minutes = 10), reason = "Spamming")
#                 try: await message.author.send("You have been muted for spamming!")
#                 except: pass

# def setup(bot):
#     bot.add_cog(Antispam(bot))


