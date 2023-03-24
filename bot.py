import logging
import os
import random
import sys

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
BOT_GUILD: int = int(os.getenv("BOT_GUILD"))  # type: ignore

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
    server: discord.Guild = bot.get_guild(874974449403826197)
    # print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    # print("------")


# @bot.command()
# async def add(ctx: Messageable, left: int, right: int):
#     """Adds two numbers together."""
#     await ctx.send(left + right)


# @bot.command()
# async def roll(ctx: Messageable, dice: str):
#     """Rolls a dice in NdN format."""
#     rolls: int
#     limit: int
#     try:
#         rolls, limit = map(int, dice.split("d"))
#     except Exception:
#         await ctx.send("Format has to be in NdN!")
#         return

#     result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
#     await ctx.send(result)


# @bot.command(description="For when you wanna settle the score some other way")
# async def choose(ctx, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx, times: int, content="repeating..."):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f"{member.name} joined {discord.utils.format_dt(member.joined_at)}")


# @bot.group()
# async def cool(ctx):
#     """Says if a user is cool.

#     In reality this just checks if a subcommand is being invoked.
#     """
#     if ctx.invoked_subcommand is None:
#         await ctx.send(f"No, {ctx.subcommand_passed} is not cool")


# @cool.command(name="bot")
# async def _bot(ctx):
#     """Is the bot cool?"""
#     await ctx.send("Yes, the bot is cool.")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    logger.info(
        f"{message.author} sent message in " f"#{message.channel}: {message.content}"
    )

    # if message.content == "&reboot":
    #     python = sys.executable
    #     os.execl(python, python, *sys.argv)

    if "screenshots" in message.channel.name:
        logger.debug("Message was sent in screenshot channel, handling...")
        await screenshots.handle_in_screenshots(message)

    # if message.content.startswith("&hello"):
    #     await message.channel.send("Hello!")


bot.run(BOT_TOKEN)
