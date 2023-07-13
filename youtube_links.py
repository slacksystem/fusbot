import logging
from enum import Enum, auto
import os
import re
import aiohttp
import logging_config
import re
from dotenv import load_dotenv
from urllib.parse import urlparse

logging_config.configure_logging()
logger = logging.getLogger(__name__)

load_dotenv()

YT_API_KEY = os.getenv("YT_API_KEY")

yt_regex = re.compile(
    r"(^|\s)(?:https:\/\/)?(?:((?:[\w\d.]+)+\.)+)?(?:youtube\.com|youtu\.be|googlevideo\.com)(?:\/[\w\d._~:/?#\[\]@!$&'()*+,;=%-]*)?"
)


async def link_is_yt(url) -> bool:
    return yt_regex.match(url) is not None
