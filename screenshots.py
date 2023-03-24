import logging
# import sys
from typing import List

from discord import Attachment, Member, Message, TextChannel, Thread
from discord.abc import Messageable
from discord.errors import Forbidden, HTTPException, NotFound

import logging_config

# from discord.utils import _ColourFormatter

logging_config.configure_logging()
logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler(sys.stdout)
# formatter = _ColourFormatter()
# handler.setFormatter(formatter)
# logger.addHandler(handler)


async def handle_in_screenshots(message: Message):
    pictures: List[Attachment] = [
        pic for pic in message.attachments if pic.content_type.startswith("image")
    ]
    logger.debug(f"{len(pictures)=}")
    author: Member = message.author  # type: ignore

    channel: Messageable = message.channel
    if not isinstance(channel, TextChannel):
        return
    if pictures:
        logger.debug(f"{pictures=}")
        # Create thread
        new_thread: Thread = await message.channel.create_thread(  # type: ignore
            name=f"Screenshot from {author.name}",
            message=message,
        )
        # for index, picture in enumerate(pictures):
        #     sender: Member | User = message.author
        #     imagefile: File = await picture.to_file(filename="image", use_cached=True)
        #     initial_description: str = (  # Description to prepend if first image
        #         f"User {sender.name} posted {message.content} " if index == 1 else ""
        #     )
        #     # Create index'th embed
        #     an_embed: Embed = Embed(
        #         description=initial_description + f"{index}/{len(pictures)}",
        #     )
        #     # Add the image
        #     an_embed.set_image(url="attachment://image")

        #     await new_thread.send(file=imagefile, embed=an_embed)

    else:
        if channel.permissions_for(author).manage_messages:

            return
        logger.debug(message.channel.permissions_for(author))
        logger.debug(message.channel.permissions_for(author).manage_messages)

        response: Message = await channel.send(
            f"{author.mention}, Only messages with screenshots can "
            "can be sent in this channel, if you want to comment on "
            "another screenshot here, you may do so in its thread."
        )
        try:
            await message.delete()
        except NotFound:
            logger.warn(
                f"Message in {channel.name} ({channel.id}) "
                f"from {author.name} ({author.id}) could not be found."
            )
        except Forbidden:
            error_msg: str = (
                f"Missing Permission: Manage Messages in channel "
                f"{channel.name} ({channel.id}) of server {channel.guild.name} ({channel.guild.id}). "
                f"Please give permission for full functionality"
            )
            logger.error(error_msg)
        except HTTPException as e:
            logger.error(f"HTTPException: {e.code=}, {e.text=}, {e.status=}")
        await response.delete(delay=5)
