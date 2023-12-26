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
ADMIN_ID = discord.Object(id=int(os.getenv("ADMIN")))

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
