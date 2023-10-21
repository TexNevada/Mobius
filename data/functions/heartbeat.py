import aiohttp
import configparser
import asyncio
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
        async with aiohttp.ClientSession() as session:
            async with session.get(config["Logging"]["heartbeat_url"]):
                await asyncio.sleep(60)
