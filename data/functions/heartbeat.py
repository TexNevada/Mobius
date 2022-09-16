import requests
import configparser
"""
=================================================
Sends heartbeats to monitoring service
=================================================
"""

# Reads the config and configures parameters.
config = configparser.ConfigParser()
config.read("./config.ini")


def heartbeat():
    requests.get(config["LOGGING"]["heartbeat_url"])
