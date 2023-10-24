import discord
import configparser
from discord.ext import commands
from data.functions.MySQL_Connector import MyDB
from data.functions.logging import get_log
config = configparser.ConfigParser()
config.read("./config.ini")
logger = get_log(__name__)


"""
================
Prep area
================
"""
Normal_embed_url = "https://cdn.edb.tools/MODUS_Project/images/Enclave/Enclave.png"
Halloween_embed_url = "https://cdn.edb.tools/MODUS_Project/images/Enclave/MODUS-glitching1.gif"

embed_url = Halloween_embed_url


class prefix_check:
    def __init__(guild, id):
        guild.id = id

    def pref(guild):
        try:
            # Referencing the help database for custom file
            c = MyDB("Essential")
            c.execute("SELECT * FROM GuildTable WHERE GuildID LIKE %s", ('{}'.format(guild.id),))
            response = c.fetchone()
            CustomPrefix = []
            if response["Prefix"] is not None:
                CustomPrefix.append(response["Prefix"])
                prefix = CustomPrefix
            else:
                prefix = pre["prefix"]
            c.close()
        except:
            prefix = pre["prefix"]
        return prefix[0]

"""
==============================
Beginning of discord commands
==============================
"""


# Making a class to reference this file later as extension
class User_Help_Commands(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    # Waiting for command from user
    @commands.group(name="help", aliases=["h", "commands"], case_insensitive=True)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.guild:
                logger.info(f"A user requested the command \"help\" in {ctx.guild.name}")
            else:
                logger.info(f"A user requested the command \"help\" in a private message")

            # ==============================
            # Start of Admin Commands Embed
            # ==============================
            if ctx.author.guild_permissions.manage_channels:
                c = MyDB("help")
                c.execute("SELECT * FROM en_AdminHelpCommands")
                response = c.fetchall()

                embed = discord.Embed(color=discord.Color.red(), title=":tools: Admin help commands!")
                embed.set_thumbnail(url=embed_url)

                try:
                    x = prefix_check(ctx.guild.id)
                    prefix = x.pref()
                except:
                    prefix = config["APP"]["prefix"]

                # Loop every entry in the database
                for entry in response:
                    if entry["Visible"] == "True":
                        # Add embed from entry
                        embed.add_field(name=f'**{prefix + entry["CommandName"]}**', value=entry["CommandDescription"], inline=False)
                # embed.add_field(name="\uFEFF", value="Stuck? [Check the documentation](https://modus.enclavedb.net/)", inline=False)
                # sends embed after closing the db

                c.execute("SELECT * FROM en_AdminHelpReactionRolesCommands")
                response = c.fetchall()
                # Loop every entry in the database
                for entry in response:
                    if entry["Visible"] == "True":
                        # Add embed from entry
                        embed.add_field(name=f'**{prefix + entry["CommandName"]}**', value=entry["CommandDescription"],
                                        inline=False)

                await ctx.send(embed=embed)
                c.close()

                # c = MyDB("help")
                # c.execute("SELECT * FROM en_AdminHelpReactionRolesCommands")
                # response = c.fetchall()
                # # starts a embed in discord
                # embed = discord.Embed(color=discord.Color.red(), title=":tools: Admin help commands!")
                #
                # # Loop every entry in the database
                # for entry in response:
                #     if entry["Visible"] == "True":
                #         # Add embed from entry
                #         embed.add_field(name=f'**{prefix + entry["CommandName"]}**', value=entry["CommandDescription"],
                #                         inline=False)
                # # sends embed
                # await ctx.send(embed=embed)
                # c.close()
            else:
                await ctx.send(
                    "The regular help command has been deprecated in favor of the new slash commands which lists"
                    "all commands when typing / and selecting MODUS from the side list. If you are a administrator"
                    "in a discord server then you should still be able to see the regular admin help commands.")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(User_Help_Commands(client))
