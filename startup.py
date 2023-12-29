import discord, settings, os

intents = discord.Intents.all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    # Get the guild (server) you want to gather IDs from
    guild = client.get_guild(settings.GUILDS_ID.id)  # Replace 'GUILD_ID' with the ID of your guild

    if not os.path.exists('thresholds.py'):
        # Open the .env file in append mode
        with open('.env', 'a') as f:
            f.write("\n\n")
            # Iterate over all the roles in the guild
            for role in guild.roles:
                # Write the role's ID and name to the file in the format KEY=VALUE
                f.write(f"{role.name.upper().replace(' ', '_').replace('.', '_').replace('@', '')}={role.id}\n")
            
            for channel in guild.channels:
                f.write(f"{channel.name.upper().replace(' ', '_').replace('-', '_')}={channel.id}\n")

        # Open the .env file in append mode
        with open('settings.py', 'a') as f:
            f.write("\n\n")
            # Iterate over all the channels in the guild
            for role in guild.roles:     
                f.write(f"{role.name.replace(' ', '_').replace('.', '_').replace('@', '')}_ID = discord.Object(id=int(os.getenv('{role.name.replace(' ', '_').replace('.', '_').replace('@', '')}')))\n\n") 
            for channel in guild.channels:
                f.write(f"{channel.name.replace(' ', '_').replace('-', '_')}_ID = discord.Object(id=int(os.getenv('{channel.name.replace(' ', '_').replace('-', '_')}')))\n\n")
            
        # creates the thresholds.py file
        with open('thresholds.py', 'a') as f:
            non_linear_list = [i**4 for i in range(len(guild.roles))]
            # change the 5:-2 here, for additional reaction roles to 5 (eg 6,7,8), for addition admin roles add to -2 (eg -3, -4, -5)
            thresholds = [{'threshold': i, 'role_id': role.id} for i, role in zip(non_linear_list, guild.roles[5:-2])]
            f.write("thresholds = [\n\n")      
            for threshold in thresholds:
                f.write(f"     {threshold}, # {guild.get_role(threshold['role_id'])}\n")
            f.write("\n]\n\n")
    else:
        print("Setup has already been complete. You may now run the main.py file.")
        await client.close()

    print("Done! You may now run the main.py file.")
    await client.close()   

# Run the Discord client
client.run(settings.TOKEN)