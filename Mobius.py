# !/usr/bin/python3

# To run this code
# Python 3.8 64bit or higher is required.
# Checks if all requirements are installed. If not it will install them.

import data.functions.ReqInstaller as ReqInstaller
ReqInstaller.check()

# Imports the rest of the modules
import discord
from discord.ext import commands, tasks
# from discord import app_commands
import os
import configparser
import sys
from colorama import init, Fore
# import glob
# from datetime import date, datetime
# import random

import data.functions.ConfigSetup as ConfigSetup
from data.functions.heartbeat import heartbeat
from data.functions.owner import is_owner
from data.functions.config import version as mobius_version
from data.functions.MySQL_Connector import MyDB
from data.functions.logging import get_log
init(autoreset=True)
sys.path.append(".")
logger = get_log(__name__)

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
prefix = APP["Prefix"]
boot_msg = APP["Boot_msg"]
ready_msg = APP["Ready_msg"]
bot_name = APP["Bot_Name"]

loaded_cogs = []

"""
===========
Prep files
===========
"""
if eval(APP["sync_prompt"]) is True:
    should_sync = input("Do you want to sync commands? [y/n]: ")
else:
    should_sync = "n"

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

    # async def setup_hook(self) -> None:
    #     #
    #     # Loads the cog at the beginning
    #     #           VVVVV
    #
    #     cogs = os.listdir("./data/cogs/")
    #     # TODO: Remove last entry in list
    #     exception_list = ["_CogLoader.py", "__init__.py", "__pycache__", "Unfinished cogs"]
    #     for item in exception_list:
    #         cogs.remove(item)
    #     errors = []
    #     passed = []
    #     passed_chk = False
    #     for cog in cogs:
    #         cog = cog.split(".")
    #         try:
    #             await client.load_extension("data.cogs." + cog[0])
    #             passed.append(cog[0])
    #             loaded_cogs.append(cog[0])
    #             passed_chk = True
    #         except Exception as e:
    #             errors.append(cog[0])
    #             if config["APP"]["Debug"] == "DEBUG":
    #                 logger.info(e)
    #     if bool(errors):
    #         for cog in errors:
    #             logger.info(f"{Fore.LIGHTWHITE_EX}[{Fore.RED}ERROR{Fore.LIGHTWHITE_EX}] Could not load the following `{cog}`")
    #     if passed_chk is True:
    #         for cog in passed:
    #             logger.info(f"{Fore.LIGHTWHITE_EX}[{Fore.GREEN}OK{Fore.LIGHTWHITE_EX}] Loaded {cog}")
    #     # await self.client.tree.sync(guild=discord.Object(id=704725246187536489))
    #
    #     #
    #     # Syncing
    #     #   VVV
    #     self.tree.copy_global_to(guild=dev_guild)
    #     if should_sync.lower() == "y":
    #         client.tree.clear_commands(guild=dev_guild)
    #         await self.tree.sync()

    async def setup_hook(self) -> None:
        #
        # Loads the cog at the beginning
        #           VVVVV
        exception_list = ["_CogLoader.py", "__init__.py", "__pycache__", "Unfinished cogs", ".git", ".gitignore",
                          "README.md", "LICENSE", "requirements.txt", "deprecated"]
        errors = []

        async def load_cogs(folder, import_path="data.cogs"):
            for filename in os.listdir(folder):
                if filename not in exception_list:
                    filepath = os.path.join(folder, filename)
                    if os.path.isfile(filepath) and filename.endswith('.py'):
                        cog_name = os.path.splitext(filename)[0]
                        full_import_path = f"{import_path}.{cog_name}"
                        try:
                            await client.load_extension(full_import_path)
                            loaded_cogs.append(cog_name)
                            logger.info(f"{Fore.LIGHTWHITE_EX}[{Fore.GREEN}OK{Fore.LIGHTWHITE_EX}] Loaded {cog_name}{Fore.RESET}")
                        except Exception as e:
                            errors.append(cog_name)
                            if Environment == "Dev":
                                logger.info(e)
                    elif os.path.isdir(filepath):
                        new_import_path = f"{import_path}.{filename}"
                        await load_cogs(filepath, import_path=new_import_path)

        await load_cogs("./data/cogs/")

        if bool(errors):
            for cog in errors:
                logger.error(
                    f"{Fore.LIGHTWHITE_EX}[{Fore.RED}ERROR{Fore.LIGHTWHITE_EX}] Could not load the following `{cog}`{Fore.RESET}")

        # Syncing
        #   VVV
        try:
            dev_guild = discord.Object(id=config["APP"]["DevGuild"])
            self.tree.copy_global_to(guild=dev_guild)
            if should_sync.lower() == "y":
                client.tree.clear_commands(guild=dev_guild)
                await self.tree.sync()
        except TypeError:
            logger.warning(f"[{Fore.YELLOW}WARNING{Fore.RESET}] Guild ID is not set in config.ini. "
                           f"Slash commands sync is disabled")


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
    logger.info("")
    logger.info(f"{Fore.GREEN}#" * 110 + Fore.RESET)
    logger.info(f"{Fore.GREEN}#" * 110 + Fore.RESET + "\n")

    if os.path.isfile("./data/functions/ascii.py"):
        import data.functions.ascii as ascii # noqa
        ascii.run()
    else:
        logger.info(f"{Fore.LIGHTGREEN_EX} ███╗   ███╗ ██████╗ ██████╗ ██╗██╗   ██╗███████╗     ██████╗ ██████╗ ██████╗ ███████╗ {Fore.RESET}") # noqa
        logger.info(f"{Fore.LIGHTGREEN_EX} ████╗ ████║██╔═══██╗██╔══██╗██║██║   ██║██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ {Fore.RESET}") # noqa
        logger.info(f"{Fore.LIGHTGREEN_EX} ██╔████╔██║██║   ██║██████╔╝██║██║   ██║███████╗    ██║     ██║   ██║██████╔╝█████╗ {Fore.RESET}") # noqa
        logger.info(f"{Fore.LIGHTGREEN_EX} ██║╚██╔╝██║██║   ██║██╔══██╗██║██║   ██║╚════██║    ██║     ██║   ██║██╔══██╗██╔══╝ {Fore.RESET}") # noqa
        logger.info(f"{Fore.LIGHTGREEN_EX} ██║ ╚═╝ ██║╚██████╔╝██████╔╝██║╚██████╔╝███████║    ╚██████╗╚██████╔╝██║  ██║███████╗ {Fore.RESET}") # noqa
        logger.info(f"{Fore.LIGHTGREEN_EX} ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ {Fore.RESET}") # noqa

    if Environment == "Dev":
        logger.info("  ~~You are running a development version!~~\n"
                    "  ~~It should not be used for production!~~")
    # guilds = client.guilds
    # total_members = []
    # for members in guilds:
    #     for member in members.members._SequenceProxy__copied: # noqa
    #         if member not in total_members:
    #             total_members.append(member)
    # activeServers = client.guilds
    # sum = 0
    # for s in activeServers:
    #     sum += len(s.members)
        # total_members += len(members.members)
    # prints that the bot is ready with its username & id
    logger.info(f"  {Fore.LIGHTWHITE_EX}Mobius version: {Fore.GREEN}{mobius_version()}{Fore.RESET}")
    logger.info(f"  {Fore.LIGHTWHITE_EX}Discord.py version:{Fore.GREEN} {discord.__version__}{Fore.RESET}")
    logger.info(f"  {Fore.LIGHTWHITE_EX}------")
    logger.info(f"  {Fore.LIGHTWHITE_EX}Bot's name:{Fore.GREEN} {client.user.name}{Fore.RESET}")
    logger.info(f"  {Fore.LIGHTWHITE_EX}Bot id:{Fore.GREEN} {client.user.id}{Fore.RESET}")
    logger.info(f"  {Fore.LIGHTWHITE_EX}Loaded cogs: {Fore.GREEN}{len(loaded_cogs)}{Fore.RESET}")
    logger.info(f"  {Fore.LIGHTWHITE_EX}Bot is currently serving:{Fore.GREEN} {len(client.guilds)} {Fore.LIGHTWHITE_EX}guilds.{Fore.RESET}") # noqa
    # logger.info(f"  {Fore.LIGHTWHITE_EX}Bot is currently serving:{Fore.GREEN} {len(total_members)} {Fore.LIGHTWHITE_EX}members across all guilds.{Fore.RESET}") # noqa
    logger.info("")
    logger.info(f"{Fore.GREEN}#" * 110 + Fore.RESET)
    logger.info(f"{Fore.GREEN}#" * 110 + Fore.RESET)
    # await client.load_extension("data.cogs._CogLoader")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=ready_msg))
    if config["Logging"]["Logs"] == "False":
        logger.info(f"{Fore.LIGHTWHITE_EX}[{Fore.YELLOW}WARNING{Fore.LIGHTWHITE_EX}]: Logging is disabled! If this was a mistake. {Fore.RESET}" # noqa
                    f"Please enable it in the config under LOGGING.")
    if config["Logging"]["heartbeat_url"] != "":
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
    logger.info(f"Bot is serving: {str(len(client.guilds))} guilds.")

# Loads the Cogs Loader


@client.command()
@is_owner()
async def sync_slash(ctx):
    await client.tree.sync(guild=discord.Object(id=704725246187536489))
    await ctx.send("Synced!")


@client.command()
@is_owner()
async def test(ctx, emoji):
    #logger.info(ctx.guild)
    #logger.info(ctx.guild.roles)
    logger.info(emoji)
    await ctx.send(emoji)


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
    logger.info("\nBot logout requested. Shutting down...\n")
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

