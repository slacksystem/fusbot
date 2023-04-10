import json
import logging
import os
import random
import sys
from typing import List

import discord
from discord.abc import Messageable
from discord.ext import commands
from dotenv import load_dotenv

import logging_config
import screenshots

logging_config.configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_GUILD: List[int] = json.loads(os.getenv("BOT_GUILD"))  # type: ignore

description = """
A bot intended to perform tasks on the Fus and Auriel's Dream Discord server
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="&", description=description, intents=intents)


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if message.guild is None or message.guild.id != BOT_GUILD:
        return
    logger.info(
        f"{message.author} sent message in " f"#{message.channel}: {message.content}"
    )

    if "screenshots" in message.channel.name:
        logger.debug("Message was sent in screenshot channel, handling...")
        await screenshots.handle_in_screenshots(message)


bot.run(BOT_TOKEN)
