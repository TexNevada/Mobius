# !/usr/bin/python3

# To run this code
# Python 3.8 64bit or higher is required.
# Checks if all requirements are installed. If not it will install them.
import data.functions.ReqInstaller as ReqInstaller
ReqInstaller.check()

# Imports the rest of the modules
import discord
from discord.ext import commands, tasks
from discord import app_commands
import logging
import os
import glob
from datetime import date, datetime
import random
from data.functions.heartbeat import heartbeat
from data.functions.owner import is_owner
import data.functions.ConfigSetup as ConfigSetup
import configparser
import sys
sys.path.append(".")
from data.functions.MySQL_Connector import MyDB

"""
=========
Config
=========
"""
# Checks to see if the config file exists.
# Will pass if config does exist.
ConfigSetup.check()

# Reads the config and configures parameters.
config = configparser.ConfigParser()
config.read("./config.ini")

APP = config["APP"]

Environment = APP["Environment"]
token = APP["Token"]
Debug = APP["Debug"]
prefix = APP["Prefix"]
boot_msg = APP["Boot_msg"]
ready_msg = APP["Ready_msg"]
bot_name = APP["Bot_Name"]

log_location = config["LOGGING"]["Log"]
log_name = log_location+bot_name+".log"

"""
=========
Logging
=========
"""

if Environment == "Dev":
    print("~~You are running a development version!~~\n"
          "~~It should not be used for production!~~")


if config["LOGGING"]["Logs"] == "True":
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

if Debug == "DEBUG":
    LogLevel = logging.DEBUG
else:
    LogLevel = logging.WARNING

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
should_sync = input("Do you want to sync commands? [y/n]: ")
dev_guild = discord.Object(id=config["APP"]["DevGuild"])

intents = discord.Intents.all()
intents.members = eval(APP["Members"])
intents.presences = eval(APP["Presences"])
intents.messages = eval(APP["Messages"])


class MyClient(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(intents=intents,
                         command_prefix=get_prefix,
                         help_command=None,
                         case_insensitive=eval(APP["Case_insensitive"]))

    # # @tasks.loop(count=1)
    # async def tree_sync(self):
    #     # await client.load_extension("data.cogs._CogLoader")
    #     client.tree.copy_global_to(guild=dev_guild)
    #     await self.tree.sync(guild=dev_guild)

    async def setup_hook(self) -> None:
        #
        # Loads the cog at the beginning
        #           VVVVV

        cogs = os.listdir("./data/cogs/")
        # TODO: Remove last entry in list
        for item in ["_CogLoader.py", "__init__.py", "__pycache__", "Unfinished cogs"]:
            cogs.remove(item)
        errors = []
        passed = []
        passed_chk = False
        for cog in cogs:
            cog = cog.split(".")
            try:
                await client.load_extension("data.cogs." + cog[0])
                passed.append(cog[0])
                passed_chk = True
            except Exception as e:
                errors.append(cog[0])
                if config["APP"]["Debug"] == "DEBUG":
                    print(e)
        if bool(errors):
            for cog in errors:
                print(f"ERROR! Could not load the following `{cog}`")
        if passed_chk is True:
            for cog in passed:
                print(f"OK! Loaded {cog}")
        # await self.client.tree.sync(guild=discord.Object(id=704725246187536489))

        #
        # Syncing
        #   VVV
        self.tree.copy_global_to(guild=dev_guild)
        if should_sync.lower() == "y":
            client.tree.clear_commands(guild=dev_guild)
            await self.tree.sync()


def get_prefix(client, message):
    try:
        if message.guild:
            c = MyDB("Essential")
            c.execute("SELECT * FROM GuildTable WHERE GuildID = %s", (message.guild.id,))
            response = c.fetchone()
            CustomPrefix = []
            if response["Prefix"] is not None:
                CustomPrefix.append(response["Prefix"])
                prefix = CustomPrefix
            else:
                prefix = APP["Prefix"]
            c.close()
        else:
            prefix = APP["Prefix"]
    except:
        prefix = APP["Prefix"]

    if not message.guild:
        return commands.when_mentioned_or(*prefix)(client, message)

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefix)(client, message)


client = MyClient()


# client = commands.Bot(
#     command_prefix=get_prefix,
#     status=discord.Status.dnd,
#     activity=discord.Game(name=boot_msg),
#     case_insensitive=eval(APP["Case_insensitive"]),
#     # The total number of shards to use between all clusters
#     # shard_count=4,
#     # Indicate what shard ID to use
#     # shard_ids=(0,),
#     intents=intents,
#     application_id=APP["Application_ID"]
#     )
# # tree = app_commands.CommandTree(client)
# # Here we are deleting the standard help function in discord to make our on in a embed later.
# client.remove_command("help")

"""
============================
Slash commands procedure
============================
"""


@client.command()
@is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec=None) -> None:
    if not guilds:
        # sync current guild
        if spec == "local":
            synced = await client.tree.sync(guild=ctx.guild)
        # copies all global app commands to current guild and syncs
        elif spec == "global-to-local":
            client.tree.copy_global_to(guild=ctx.guild)
            synced = await client.tree.sync(guild=ctx.guild)
        # clears all commands from the current guild target and syncs (removes guild commands)
        elif spec == "clear-sync":
            client.tree.clear_commands(guild=ctx.guild)
            await client.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await client.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await client.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

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
          f"\nBot app id: {APP['Application_ID']}"
          f"\nDiscord.py version: {discord.__version__}"
          f"\n------"
          f"\nBot is serving: {str(len(client.guilds))} guilds.")
    # await client.load_extension("data.cogs._CogLoader")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=ready_msg))
    if config["LOGGING"]["Logs"] == "False":
        print("[WARN]: Logging is disabled! If this was a mistake. Please enable it in the config under LOGGING.")
    if config["LOGGING"]["heartbeat_url"] != "":
        client.loop.create_task(heartbeat())


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

# Loads the Cogs Loader


@client.command()
@is_owner()
async def sync_slash(ctx):
    await client.tree.sync(guild=discord.Object(id=704725246187536489))
    await ctx.send("Synced!")

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
client.run(token, reconnect=True)

