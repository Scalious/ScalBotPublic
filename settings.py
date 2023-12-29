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


EVERYONE_ID = discord.Object(id=int(os.getenv('EVERYONE')))

FROG_ID = discord.Object(id=int(os.getenv('FROG')))

WAVE_ID = discord.Object(id=int(os.getenv('WAVE')))

EVENTS_ID = discord.Object(id=int(os.getenv('EVENTS')))

NSFW_ID = discord.Object(id=int(os.getenv('NSFW')))

GUEST_ID = discord.Object(id=int(os.getenv('GUEST')))

USERS_ID = discord.Object(id=int(os.getenv('USERS')))

NEW_MEMBER_ID = discord.Object(id=int(os.getenv('NEW_MEMBER')))

MEMBER_ID = discord.Object(id=int(os.getenv('MEMBER')))

SUPER_MEMBER_ID = discord.Object(id=int(os.getenv('SUPER_MEMBER')))

SCALBOT3_0_ID = discord.Object(id=int(os.getenv('SCALBOT3_0')))

ADMIN_ID = discord.Object(id=int(os.getenv('ADMIN')))

PUBLIC_LOBBY_ID = discord.Object(id=int(os.getenv('PUBLIC_LOBBY')))

VOICE_CHANNELS_ID = discord.Object(id=int(os.getenv('VOICE_CHANNELS')))

GENERAL_ID = discord.Object(id=int(os.getenv('GENERAL')))

SYSTEM_ID = discord.Object(id=int(os.getenv('SYSTEM')))

RULES_ID = discord.Object(id=int(os.getenv('RULES')))

SCALBOT_TEST_ID = discord.Object(id=int(os.getenv('SCALBOT_TEST')))

GENERAL_ID = discord.Object(id=int(os.getenv('GENERAL')))

WELCOME_ID = discord.Object(id=int(os.getenv('WELCOME')))

SERVER_ADMIN_ID = discord.Object(id=int(os.getenv('SERVER_ADMIN')))

TEST1_ID = discord.Object(id=int(os.getenv('TEST1')))

TEST2_ID = discord.Object(id=int(os.getenv('TEST2')))

TEST3_ID = discord.Object(id=int(os.getenv('TEST3')))

TEST4_ID = discord.Object(id=int(os.getenv('TEST4')))

LOBBY_ID = discord.Object(id=int(os.getenv('LOBBY')))

LOUNGE_TEST_ID = discord.Object(id=int(os.getenv('LOUNGE_TEST')))

LOUNGE_ID = discord.Object(id=int(os.getenv('LOUNGE')))

SELF_ASSIGN_ROLES_ID = discord.Object(id=int(os.getenv('SELF_ASSIGN_ROLES')))
