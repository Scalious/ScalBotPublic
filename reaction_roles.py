import discord, settings
from discord.ext import commands

class ReactionRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        channel_id = settings.Roles_ID.id 
        if message.channel.id == channel_id:
            emojis = ['🔞', '🎉', '👋', '🐸']
            for emoji in emojis:
                await message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == settings.Roles_ID.id:
            guild = self.bot.get_guild(payload.guild_id)
            emojis_roles = {
                '🔞': settings.NSFW_ID.id,
                '🎉': settings.EVENTS_ID.id,
                '👋': settings.WAVE_ID.id,
                '🐸': settings.FROG_ID.id,
            }

            # Get the emoji that was reacted with
            emoji = str(payload.emoji)

            # Check if the emoji is in the dictionary
            if emoji in emojis_roles:
                # Get the role ID that corresponds to the emoji
                role_id = emojis_roles[emoji]

                # Get the role and member objects
                role = discord.utils.get(guild.roles, id=role_id)
                member = discord.utils.get(guild.members, id=payload.user_id)

                # Add the role to the member
                await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.channel_id == settings.Roles_ID.id:
            guild = self.bot.get_guild(payload.guild_id)
            emojis_roles = {
                '🔞': settings.NSFW_ID.id,
                '🎉': settings.EVENTS_ID.id,
                '👋': settings.WAVE_ID.id,
                '🐸': settings.FROG_ID.id,
            }
            emoji = str(payload.emoji)
            if emoji in emojis_roles:
                role_id = emojis_roles[emoji]
                role = discord.utils.get(guild.roles, id=role_id)
                member = discord.utils.get(guild.members, id=payload.user_id)
                await member.remove_roles(role)


async def setup(bot):
    await bot.add_cog(ReactionRoles(bot))
