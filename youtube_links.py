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


def video_id(url: str):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = urlparse(url)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            p = urlparse.parse_qs(query.query)
            return p["v"][0]
        if query.path[:7] == "/embed/":
            return query.path.split("/")[2]
        if query.path[:3] == "/v/":
            return query.path.split("/")[2]
    # fail?
    return None


# class ReturnCode(Enum):
#     VALID_YT_LINK = auto()
#     NON_YT_LINK = auto()
#     INVALID_YT_LINK = auto()


async def yt_video_exists(video_id: str) -> bool:
    logger.info(f"Checking if video with id {video_id} exists")
    url = f"http://www.youtube.com/oembed?url=http://www.youtube.com/watch?v={video_id}&format=json"
    url = f"https://www.googleapis.com/youtube/v3/videos?part=id&id={video_id}&key={YT_API_KEY}"

    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            logger.info(f"Check for video id {video_id} returned: {response.status}")
            return response.status == 200


async def link_is_yt(url) -> bool:
    return yt_regex.match(url) is not None
