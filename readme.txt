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

The following id's are hard-coded as I was unable to get them to function via the settings file;

Guest Role ID
New Member Role ID
Member Role ID
Super Member Role ID
Leveling Channel ID (the channels members can earn points to become Member/Super Member)
    Currently the 2nd learning channel is setup to be the test Channel
Guild ID (this is your discord server)
Admin Role ID
Rules Channel ID (the channel you wish to host your rules accept/decline message)

## Known Issues

On startup Errors:
WARNING    - discord.client : PyNaCl is not installed, voice will NOT be supported
Error: 'users.txt' contains invalid JSON. - occurs when users.txt is not created
Reloading any file with a tasks.loop will cause repeat issues

