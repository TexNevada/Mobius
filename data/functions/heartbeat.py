import aiohttp
import configparser
import asyncio
from data.functions.logging import get_log
logger = get_log(__name__)

"""
=================================================
Sends heartbeats to monitoring service
=================================================
"""

# Reads the config and configures parameters.
config = configparser.ConfigParser()
config.read("./config.ini")


async def heartbeat():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(config["Logging"]["heartbeat_url"]) as response:
                    logger.debug(f"Heartbeat to origin returned: {response.status}")
        except Exception as e:
            logger.error(f"Error in heartbeat: {e}")
        await asyncio.sleep(60)
