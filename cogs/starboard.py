import discord
from discord.ext import commands
import asyncio

class Starboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot  # Save the bot instance
        self.reaction_counts = {}  # Dictionary to track reaction counts for each message
        self.posted_messages = set()  # Set to track messages that have been posted
        self.target_channel_id = 1203709271972511785  # Replace with your target channel ID

    async def send_to_starboard(self, message_content, reaction_count):
        target_channel = self.bot.get_channel(self.target_channel_id)
        if target_channel:
            # Check if the message has already been posted
            if message_content.id not in self.posted_messages:
                # Create a markdown-formatted message
                formatted_message = (
                    f"{reaction_count} ⭐ | {message_content.jump_url}"
                    # f"**Author:** {message_content.author.mention}\n"
                    f"```{message_content.content}```\n"
                )
                # 2-minute delay for reaction counting
                await asyncio.sleep(120)
                await target_channel.send(formatted_message)
                # Add the message ID to the set of posted messages
                self.posted_messages.add(message_content.id)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        # Check if the reaction is from a bot
        if user.bot:
            return

        message_id = reaction.message.id

        # Initialize the set for this message if not already present
        if message_id not in self.reaction_counts:
            self.reaction_counts[message_id] = set()

        # Check if the user has already reacted to this message
        if user.id not in self.reaction_counts[message_id]:
            self.reaction_counts[message_id].add(user.id)
            print(f"Reaction count for message {message_id}: {len(self.reaction_counts[message_id])}")

            # Check if the reaction count exceeds 5
            if len(self.reaction_counts[message_id]) > 5:
                message_content = reaction.message
                reaction_count = len(self.reaction_counts[message_id])
                await self.send_to_starboard(message_content, reaction_count)

async def setup(bot):
    await bot.add_cog(Starboard(bot))
