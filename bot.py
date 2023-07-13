import argparse
import json
import logging
import os
from typing import List

import discord
from discord.ext import commands
from dotenv import load_dotenv

import handlers
import logging_config

logging_config.configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_GUILDS: List[int] = json.loads(os.getenv("BOT_GUILDS"))  # type: ignore

parser = argparse.ArgumentParser(description="Run the bot")
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
args = parser.parse_args()

description = """
A bot intended to perform tasks on the Fus and Auriel's Dream Discord server
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="&", description=description, intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")  # type: ignore
    logger.info(f"Listening on servers: {BOT_GUILDS}")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if message.guild is None or message.guild.id not in BOT_GUILDS:
        return
    logger.info(
        f"{message.author} sent message in " f"#{message.channel}: {message.content}"
    )

    if "screenshots" in message.channel.name:  # type: ignore
        logger.debug("Message was sent in screenshot channel, handling...")
        await handlers.handle_screenshots(message, args.debug)
    if message.channel.name == "new-mod-releases":  # type: ignore
        logger.debug("Message was sent in new mod releases channel, handling...")
        await handlers.handle_mod_releases(message)


bot.run(BOT_TOKEN)  # type: ignore
