import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord

# Load environment variables from .env file
load_dotenv()
# Access the Discord API token from the environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

#access the parent directory with the settings and cogs files
BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "commands"
COGS_DIR = BASE_DIR / "cogs"

GUILDS_ID = discord.Object(id=int(os.getenv("GUILD")))

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters":{
        "verbose":{
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard":{
            "format": "%(levelname)-10s - %(name)s : %(message)s"
        },
    },
    "handlers":{
        "console": {
            'level': "DEBUG",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "console2": {
            'level': "WARNING",
            'class': "logging.StreamHandler",
            'formatter': "standard"
        },
        "file": {
            'level': "DEBUG",
            'class': "logging.FileHandler",
            'filename': "Logs/infos.log",
            'mode': "w",
            'formatter': "verbose"
            },
    },
    "loggers":{
        "bot":{
            'handlers': ['console', 'file'],
            "level": "INFO",
            "propagate": False
        },
        "discord": {
            'handlers': ['console2', "file"],
            "level": "INFO",
            "propagate": False
        },
    }
}

dictConfig(LOGGING_CONFIG)

everyone_ID = discord.Object(id=int(os.getenv('everyone')))

Frog_ID = discord.Object(id=int(os.getenv('Frog')))

Wave_ID = discord.Object(id=int(os.getenv('Wave')))

Events_ID = discord.Object(id=int(os.getenv('Events')))

NSFW_ID = discord.Object(id=int(os.getenv('NSFW')))

Guest_ID = discord.Object(id=int(os.getenv('Guest')))

New_Member_ID = discord.Object(id=int(os.getenv('New_Member')))

Member_ID = discord.Object(id=int(os.getenv('Member')))

Super_Member_ID = discord.Object(id=int(os.getenv('Super_Member')))

ScalBot3_0_ID = discord.Object(id=int(os.getenv('ScalBot3_0')))

Admin_ID = discord.Object(id=int(os.getenv('Admin')))

Public_Lobby_ID = discord.Object(id=int(os.getenv('Public_Lobby')))

Voice_Channels_ID = discord.Object(id=int(os.getenv('Voice_Channels')))

General_ID = discord.Object(id=int(os.getenv('General')))

system_ID = discord.Object(id=int(os.getenv('system')))

rules_ID = discord.Object(id=int(os.getenv('rules')))

scalbot_test_ID = discord.Object(id=int(os.getenv('scalbot_test')))

general_ID = discord.Object(id=int(os.getenv('general')))

welcome_ID = discord.Object(id=int(os.getenv('welcome')))

Server_Admin_ID = discord.Object(id=int(os.getenv('Server_Admin')))

test1_ID = discord.Object(id=int(os.getenv('test1')))

test2_ID = discord.Object(id=int(os.getenv('test2')))

test3_ID = discord.Object(id=int(os.getenv('test3')))

test4_ID = discord.Object(id=int(os.getenv('test4')))

Lobby_ID = discord.Object(id=int(os.getenv('Lobby')))

lounge_test_ID = discord.Object(id=int(os.getenv('lounge_test')))

lounge_ID = discord.Object(id=int(os.getenv('lounge')))

self_assign_roles_ID = discord.Object(id=int(os.getenv('self_assign_roles')))

Adult_Content_ID = discord.Object(id=int(os.getenv('Adult_Content')))

Events_ID = discord.Object(id=int(os.getenv('Events')))

