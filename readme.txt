======= ScalBot3.0 =======

======= Description =======

This is a moderation bot created for managing AntiSpam, Ticketing, Member Activity Roles, and Self-Assign Roles.

======= Local Installation Requirements =======

To run this project, you need to have the following dependencies installed:

- Python 3.11.2 or higher
- pip (comes with Python)

You can install the dependencies by running the following command:

```bash
pip install -r requirements.txt

======= Server / Bot Setup =======

You will need;
1. Update the file .env with you TOKEN and GUILD id's before running startup.py
2. Within your setup Discord server: 
    -the bot assumes you have 1 admin role, 1 bot role and 4 reaction roles, to add more you need to modify the startup.py
    -the Admin and Bot roles are ignored in the leveling.py, if add more roles you will need to include them here
    -Create an Admin role - move this to the top 2 positions
    -A bot role is automatically created - move this to the top 2 positions
    -Create 4 Reaction roles and move them to the bottom eg. (NSFW,Events, Misc1, Misc2)
        -their names do not matter but the order is important for the thresholds in startup.py
    -Create a Channel Category called PUBLIC LOBBY
        -this is where users can earn points for additional ranks, points are not generated anywhere else
        -I lied create a scalbot-test channel anywhere in your server to test points functions
        -points can be manually changed in the users.json file
3. You will need to create a file .env with you TOKEN and GUILD id. before running startup.py in the same folder

Run startup.py

Run main.py

======= Known Issues =======

On startup Errors:
# library not used
WARNING    - discord.client : PyNaCl is not installed, voice will NOT be supported
# users.json is not created with {} dictionary
Error: 'users.json' contains invalid JSON. - 
# it just does
Reloading any file with a tasks.loop will cause repeat issues with .reload commands
# not certain if this error is an issue or how to avoid it
Removing roles outside of the thresholds list will cause an error
# no clue - might be a load order or timing issue
The role update message will show the previous role when adding/removing roles sometimes

