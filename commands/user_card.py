from io import BytesIO
import json
import discord
from discord.ext import commands
# from PIL import Image, ImageDraw
from easy_pil import Canvas, Editor, Font, load_image_async

# Potential to add to users.json - role_colour, role_name, next_threshold(points), next_threshold_name(points

class UserCard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.users = self.bot.user_handler

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        """Display a user's profile card"""
        member = ctx.author # Remove this line if you want to mention a user
        with open('users.json', 'r') as f:
            users = json.load(f)
        user_info = users.get(str(member.id), {})  # Get the user's info from the users.json file

        # Users Role Colour
        colour_hash = await self.bot.user_handler.role_colour(user_info.get("points", 0)) # Get the user's colour
        colour = '#{:06x}'.format(colour_hash)

        # Current Points / Next Threshold Pts
        points = user_info.get("points", 0)  # Get the user's points
        next_threshold = await self.bot.user_handler.next_threshold(points) # Get the user's next threshold points
        percentage = (user_info.get("points") / next_threshold) * 100 # Calculate the percentage of the bar
        
        # Main Canvas
        background = Editor(Canvas((500, 200), color=("#202020")))
        background.rectangle((0, 0), width=500, height=200, outline=("#000000"), stroke_width=4, radius=5) # Border

        # Right Side of the Card
        card_right_shape = [(495, 0), (495, 200), (500, 200), (500, 0)] # Right side of the card
        background.polygon(card_right_shape, color=(colour))  

        # Profile Picture
        profile_picture = await load_image_async(str(member.avatar.url))
        profile = Editor(profile_picture).resize((100, 100)).circle_image()  
        large_background_circle = Editor(Canvas((220, 220), color=(colour))).circle_image() 
        background_circle = large_background_circle.resize((110, 110)) 
        background_circle.paste(profile, (5, 5)) 
        background.paste(background_circle, (20, 20))

        # Fonts
        poppins = Font.poppins(size=35)  # Larger text
        poppins_small = Font.poppins(size=20)  # Smaller text
        
        # Current Role       
        rank_name = await self.bot.user_handler.next_threshold_name(points) # Get the user's current threshold points
        background.text(
            (350, 10),  # Position in the top right corner of the rectangle
            f"{rank_name}",
            font=poppins_small,  # Use smaller text for details
            color=(colour)  # Text color
        )

        # Rank: Position
        all_users_points = [(user_id, user_info.get("points", 0)) for user_id, user_info in users.items()]
        all_users_points.sort(key=lambda x: x[1], reverse=True)
        user_position = [user_id for user_id, _ in all_users_points].index(str(member.id)) + 1
        background.text(
            (350, 30),  # Adjust the position as needed
            f"Rank: #{user_position}",
            font=poppins_small,
            color=("#656463")
        )
        
        # Leveling Bar
        background.rectangle((25, 160), width=450, height=20, color=("#656463"), radius=5) 
        background.bar((25, 160), max_width=450, height=20, percentage=percentage, color=(colour), radius=5) 
        
        # Display Name
        background.text((150, 40), user_info.get("display_name", ""), font=poppins, color=("#FFFFFF")) 

        # Divider
        background.rectangle((150, 90), width=250, height=2, color=(colour))  # Move line to the left

        # Points
        background.text(
            (150, 100),
            f"{points} / {next_threshold} Pts",
            font=poppins_small,  # Use smaller text for details
            color=("#656463")
        )

        file = discord.File(fp=background.image_bytes, filename="user_card.png")
        await ctx.send(file=file)

async def setup(bot):
    await bot.add_cog(UserCard(bot))