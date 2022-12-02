import requests
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
        requests.get(config["LOGGING"]["heartbeat_url"])
        await asyncio.sleep(60)
