import discord
from discord.ext import commands
from datetime import timedelta

class Antispam(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.anti_spam = commands.CooldownMapping.from_cooldown(5, 15, commands.BucketType.member) #5 messages in 15 seconds
        self.too_many_violations = commands.CooldownMapping.from_cooldown(4, 60, commands.BucketType.member) #4 violations in 60 seconds
    
    @commands.Cog.listener()
    async def on_message(self, message): #when a message is sent
        if type(message.channel) is not discord.TextChannel or message.author.bot: return  #ignore DMs and bots
        bucket = self.anti_spam.get_bucket(message) #
        retry_after = bucket.update_rate_limit() #returns the time left before the cooldown is over
        if retry_after: #if the user has violated the cooldown
            await message.delete() #deletes the message
            await message.channel.send(f"{message.author.mention}, don't spam!", delete_after = 10) #sends a message to the channel
            violations = self.too_many_violations.get_bucket(message) #checks if the user has violated the cooldown
            check = violations.update_rate_limit() #returns the time left before the cooldown is over
            if check: #if the user has violated the cooldown
                await message.author.timeout(timedelta(minutes = 10), reason = "Spamming") #mutes the user for 10 minutes
                try: await message.author.send("You have been muted for spamming!") #sends a DM to the user
                except: pass #if the user has DMs disabled, it will ignore the error

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


