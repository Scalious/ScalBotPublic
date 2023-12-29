# ScalBot3.0

## Description

This is a moderation bot created for managing AntiSpam and Ticketing. It also includes a leveling system.

Future iterations to include reaction roles, more checks.

## Installation

To run this project, you need to have the following dependencies installed:

- Python 3.11.2 or higher
- pip (comes with Python)

You can install the dependencies by running the following command:

```bash
pip install -r requirements.txt

You will need to create a file .env with you TOKEN and GUILD id. before running startup.py

Run startup.py

Run main.py

## Known Issues

On startup Errors:
WARNING    - discord.client : PyNaCl is not installed, voice will NOT be supported
Error: 'users.txt' contains invalid JSON. - occurs when users.txt is not created with {} dictionary
Reloading any file with a tasks.loop will cause repeat issues with .reload commands

