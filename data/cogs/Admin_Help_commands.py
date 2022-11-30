"""
Extension name: Help commands
Author: Tex Nevada
"""

# import discord library
import discord
# Imports commands
from discord.ext import commands
import configparser
from data.functions.MySQL_Connector import MyDB
config = configparser.ConfigParser()
config.read("./config.ini")

"""
================
Prep area
================
"""
Normal_embed_url = "https://cdn.edb.tools/MODUS_Project/images/Enclave/Enclave.png"
Halloween_embed_url = "https://cdn.edb.tools/MODUS_Project/images/Enclave/MODUS-glitching1.gif"

embed_url = Halloween_embed_url

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
                print(f"A user requested the command \"help\" in {ctx.guild.name}")
            else:
                print(f"A user requested the command \"help\" in a private message")

            # ==============================
            # Start of Admin Commands Embed
            # ==============================
            if ctx.author.guild_permissions.manage_channels:
                c = MyDB("help")
                c.execute("SELECT * FROM en_AdminHelpCommands")
                response = c.fetchall()

                embed = discord.Embed(color=discord.Color.red(), title=":tools: Admin help commands!")
                embed.set_thumbnail(url=embed_url)

                prefix = "@MODUS "

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
