# !/usr/bin/python3

# To run this code
# Python 3.8 64bit or higher is required.
# For required modules. Check Requirements.txt

import discord
from discord.ext import commands
import logging
import os
import glob
from datetime import date, datetime
import random
import configparser

"""
=========
Config
=========
"""

config = configparser.ConfigParser()
config.read("./config.ini")

APP = config["APP"]

Environment = APP["ENVIRONMENT"]
token = APP["TOKEN"]
Debug = APP["DEBUG"]
prefix = APP["PREFIX"]
boot_msg = APP["BOOT_MSG"]
ready_msg = APP["READY_MSG"]

log_location = config["LOGGING"]["LOG"]
log_name = log_location+"Mobius.log"

"""
=========
Logging
=========
"""

if Environment == "Dev":
    print("~~You are running a development version!~~\n"
          "~~It should not be used for production!~~")

try:
    if config["LOGGING"]["LOGS"] == "True":
        files = glob.glob(log_name)
        now = datetime.now()
        time = now.strftime("%H.%M.%S")
        for file in files:
            split = file.split(".")
            new_name = "{} {} {}.log".format(split[0], date.today(), time)
            try:
                os.rename(file, new_name)
            except:
                new_name = "{} {} {} Random {}.log".format(split[0], date.today(), time, random.randint(1, 10000))
                os.replace(file, new_name)
except:
    pass

if Debug == "DEBUG":
    LogLevel = logging.DEBUG
else:
    LogLevel = logging.DEBUG

logger = logging.getLogger('discord')
logger.setLevel(LogLevel)
handler = logging.FileHandler(filename=log_name, encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


"""
===========
Prep files
===========
"""


def get_prefix(client, message):
    # if not message.guild:
    #     return commands.when_mentioned_or(*prefix)(client, message)
    return commands.when_mentioned_or(*prefix)(client, message)


intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(
    command_prefix=get_prefix,
    status=discord.Status.dnd,
    activity=discord.Game(name=boot_msg),
    case_insensitive=True,
    # The total number of shards to use between all clusters
    # shard_count=4,
    # Indicate what shard ID to use
    # shard_ids=(0,),
    intents=intents
    )

# Here we are deleting the standard help function in discord to make our on in a embed later.
# client.remove_command("help")

"""
=================
Functions checks
=================
"""


# defines the fuction is the user the owner.
def is_owner():
    # if the message from the user = his user ID then the user is owner
    async def predicate(ctx):
        config.read("./config.ini")
        Authlist = []
        for key, value in config.items("ADMIN"):
            Authlist.append(int(value))
        if ctx.author.id in Authlist:
            return True
    return commands.check(predicate)

"""
============================
Login procedure for the bot
============================
"""


# will print when the bot has connected to the server
@client.event
async def on_ready():
    # prints that the bot is ready with its username & id
    print(f"\nBot is ready"
          f"\nLogged in as"
          f"\nBot's name: {client.user.name}"
          f"\nBot id: {client.user.id}"
          f"\nDiscord.py version: {discord.__version__}"
          f"\n------"
          f"\nBot is serving: {str(len(client.guilds))} guilds.")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=ready_msg))
    if config["LOGGING"]["LOGS"] == "False":
        print("[WARN]: Logging is disabled! If this was a mistake. Please enable it in the config under LOGGING.")


# starts a client.event
@client.event
# Defines a fuction when a message is sent
async def on_message(message):
    # Keeps the command in mind when event is running to prevent commands from not working
    await client.process_commands(message)


@client.event
async def on_guild_join(guild):
    # await client.change_presence(status=discord.Status.online, activity=discord.Game(name=">help or @MODUS help"))
    print(f"Bot is serving: {str(len(client.guilds))} guilds.")

"""
===========================
extension files loads here!
===========================
"""
# TODO: Rebuilt cog loader
# Here is all the extensions in the discord client. If a new extension is added. Add it here.
# cogs_list = ["cogs", "admin"]
#
# if __name__ == "__main__":
#     for load_dir in cogs_list:
#         for extension in [f.replace('.py', '') for f in listdir(load_dir) if isfile(join(load_dir, f))]:
#             try:
#                 client.load_extension(load_dir + "." + extension)
#                 print('loaded extension {}'.format(extension))
#             except Exception as e:
#                 exc = '{}: {}'.format(type(e).__name__, e)
#                 print('Failed to load extension {}\n{}'.format(extension, exc))


"""
============================
Logs the bot out of discord
============================
"""


# logs out the bot from discord
@client.command(name="logout", aliases=["shutdown"])
# User must have the role to continue
@is_owner()
# defines a new function call logout
async def logout(ctx):
    print("\nBot logout requested. Shutting down...\n")
    await ctx.send("Logging out.")
    await client.change_presence(status=discord.Status.invisible)
    # tells the bot to logout
    await client.close()



"""
===========================
This is the end of the client.
===========================
"""

# Checks token to login the bot into discord.
client.run(token, bot=True, reconnect=True)
