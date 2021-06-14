# !/usr/bin/python3
"""
Program name: Mobius core
Author: Tex Nevada
Created: 14.06.21 - Europe
"""

# To run this code
# Python 3.8 64bit or higher is required.
# For required modules. Check Requirements.txt

"""
========================
Modules is placed here!
========================
"""

# import discord library
import discord
# Imports commands
from discord.ext import commands
# This is required to fetch the nuke codes or other files from urls
# Allows us to read json files
import json

from os import listdir
from os.path import isfile, join
import logging
import os
import glob
from datetime import date, datetime
import random

print(f"Discord.py version: {discord.__version__}")
"""
=========
Logging
=========
"""

logs = False
try:
    if os.path.exists("disablelogs.txt") is False:
        files = glob.glob("discord.log")
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


logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


"""
===========
Prep files
===========
"""

# opens token.json file on disk to be read. You will need to edit the token file for your own use.
with open("token.json") as json_file:
    # makes the name "data" a reference to the json file.
    data = json.load(json_file)

with open("prefix.json") as json_prefix:
    # makes the name "prefix" a reference to the json file.
    pre = json.load(json_prefix)


def get_prefix(client, message):
    try:
        if message.guild:
            # TODO: MongoDB or MySQL
            if response["Prefix"] is not None:
                CustomPrefix.append(response["Prefix"])
                prefix = CustomPrefix
            else:
                prefix = pre["prefix"]
            c.close()
        else:
            prefix = pre["prefix"]
    except:
        prefix = pre["prefix"]

    if not message.guild:
        return commands.when_mentioned_or(*prefix)(client, message)

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefix)(client, message)


# Makes "token" a reference to the json file's value token
token = data["token"]

intents = discord.Intents.default()
intents.members = True
# This is the bot prefix. All "async def usercommand():" will always check if user has used the prefix
client = commands.AutoShardedBot(
    command_prefix=get_prefix,
    status=discord.Status.idle,
    activity=discord.Game(name="Booting..."),
    case_insensitive=True,
    # The total number of shards to use between all clusters
    # shard_count=4,
    # Indicate what shard ID to use
    # shard_ids=(0,),
    intents=intents
    )

# Here we are deleting the standard help function in discord to make our on in a embed later.
client.remove_command("help")

"""
=================
Functions checks
=================
"""


# defines the fuction is the user the owner.
def is_owner():
    # if the message from the user = his user ID then the user is owner
    async def predicate(ctx):
        Authlist = [189490137762103298, 214200757992292353]
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
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name="@MODUS help"))
    if os.path.exists("disablelogs.txt") is True:
        print("[WARNING]: Logging is disabled! To enable logging. Delete disablelogs.txt!")
    client.db_Essential = MyDB("Essential")
    client.db_Fallout = MyDB("Fallout")
    client.db_Help = MyDB("Help")
    # client.db_Logging = MyDB("Logging")
    client.logo = "https://cdn.edb.tools/MODUS_Project/images/Enclave/EnclaveDatabase.png"

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

# Here is all the extensions in the discord client. If a new extension is added. Add it here.
cogs_list = ["cogs", "admin", "_Partners"]

if __name__ == "__main__":
    for load_dir in cogs_list:
        for extension in [f.replace('.py', '') for f in listdir(load_dir) if isfile(join(load_dir, f))]:
            try:
                client.load_extension(load_dir + "." + extension)
                print('loaded extension {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))


"""
==================
Cogs / Extensions
==================
"""
# TODO: Rewrite the reload command to proper unloading of cogs
# client starts a command group
@client.group(hidden=True)
# checks to see if the user is the owner of the bot
@is_owner()
# Defines a function when the owner uses the reload command
async def reload(ctx):
    print(f"A reload command was executed in \"{ctx.guild.name}\" ")
    # if no sub command in group is run. Run code.
    if ctx.invoked_subcommand is None:
        # Reloads a extension.
        if __name__ == "__main__":
            tempcoglist = []
            # Will loop through the startup_extensions list
            for extension in [f.replace('.py', '') for f in listdir(cogs_list[0]) if isfile(join(cogs_list[0], f))]:
                # Code will try to unload the extensions & reload the extensions
                try:
                    # unloads extension
                    cogToUnload = client.get_cog(extension)
                    if cogToUnload:
                        client.unload_extension(cogs_list[0] + "." + extension)
                    # loads extension
                    client.load_extension(cogs_list[0] + "." + extension)
                    tempcoglist.append(extension)
                # If extension fails to load. Execption error
                except Exception as e:
                    # Bot will shot itself
                    await ctx.channel.send('\N{PISTOL}')
                    # Bot replys with the problem
                    await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
            # Prints out each extension it reloads
            await ctx.send(f"Reloaded the following cogs:\n{tempcoglist}")

# command recognizes its in a group.
# will not run without main command being specified.
@reload.command(hidden=True)
# checks to see if the user is the owner of the bot
@is_owner()
# Defines a function when the owner uses the reload command
async def admin(ctx):
    print(f"A reload command was executed in \"{ctx.guild.name}\" ")
    # Reloads a extension.
    if __name__ == "__main__":
        tempcoglist = []
        # Will loop through the startup_extensions list
        for extension in [f.replace('.py', '') for f in listdir(cogs_list[1]) if isfile(join(cogs_list[1], f))]:
            # Code will try to unload the extensions & reload the extensions
            try:
                # unloads extension
                cogToUnload = client.get_cog(extension)
                if cogToUnload:
                    client.unload_extension(cogs_list[1] + "." + extension)
                # loads extension
                client.load_extension(cogs_list[1] + "." + extension)
                tempcoglist.append(extension)
            # If extension fails to load. Execption error
            except Exception as e:
                # Bot will shot itself
                await ctx.channel.send('\N{PISTOL}')
                # Bot replys with the problem
                await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        # Prints out each extension it reloads
        await ctx.send(f"Reloaded the following cogs:\n{tempcoglist}")

"""
============================
Logs the bot out of discord
============================
"""


# logs out the bot from discord
@client.command(name="logout", aliases=["shutdown", "kill-yourself"])
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
