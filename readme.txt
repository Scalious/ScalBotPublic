# ScalBot3.0

## Description

This is a moderation bot created for managing AntiSpam and Ticketing. It also includes a leveling system.

## Installation

To run this project, you need to have the following dependencies installed:

- Python 3.11.2 or higher
- pip (comes with Python)

You can install the dependencies by running the following command:

```bash
pip install -r requirements.txt

You will need;
1. Update the file .env with you TOKEN and GUILD id's before running startup.py
2. Within your setup Discord server: 
    -the bot assumes you have 1 admin role, 1 bot role and 4 reaction roles, to add more you need to modify the startup.py
    -Create an Admin role - move this to the top 2 positions
    -Bot should be in the top 2 positions
    -Create 4 Reaction roles and move them to the bottom eg. (NSFW,Events, Misc1, Misc2)
    -their names do not matter but the order is important for the thresholds in startup.py
=======
You will need to create a file .env with you TOKEN and GUILD id. before running startup.py

Run startup.py

Run main.py

## Known Issues

On startup Errors:
WARNING    - discord.client : PyNaCl is not installed, voice will NOT be supported
Error: 'users.txt' contains invalid JSON. - occurs when users.txt is not created with {} dictionary
Reloading any file with a tasks.loop will cause repeat issues with .reload commands

