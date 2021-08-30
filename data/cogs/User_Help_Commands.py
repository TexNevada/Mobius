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
from data.functions.owner import is_owner
config = configparser.ConfigParser()
config.read("./config.ini")

# TODO: Replace database help entries with help_config.ini

"""
===================================
Prep area
"""
Normal_embed_url = "https://cdn.edb.tools/MODUS_Project/images/Enclave/Enclave.png"
Halloween_embed_url = "https://cdn.edb.tools/MODUS_Project/images/Enclave/MODUS-glitching1.gif"

embed_url = Halloween_embed_url
"""
===================================
"""

class prefix_check:
    def __init__(guild, id):
        guild.id = id

    def pref(guild):
        try:
            # Referencing the help database for custom file
            c = MyDB("essential")
            c.execute("SELECT * FROM GuildTable WHERE GuildID LIKE %s", ('{}'.format(guild.id),))
            response = c.fetchone()
            CustomPrefix = []
            if response["Prefix"] is not None:
                CustomPrefix.append(response["Prefix"])
                prefix = CustomPrefix
            else:
                prefix = config["APP"]["Prefix"]
            c.close()
        except:
            prefix = config["APP"]["Prefix"]
        return prefix[0]


"""
==============================
Beginning of discord commands
==============================
"""


# Making a class to reference this file later as extension
class User_Help_Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Waiting for command from user
    @commands.group(name="help", aliases=["h", "commands"], case_insensitive=True)
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.guild:
                print(f"A user requested the command \"help\" in {ctx.guild.name}")
            else:
                print(f"A user requested the command \"help\" in a private message")

            # Referencing the help database for custom file
            c = MyDB("help")
            c.execute("SELECT * FROM en_HelpCommands")
            response = c.fetchall()
            # starts a embed in discord
            embed = discord.Embed(color=0x80ff80, title=":information_source:  Help Commands!")
            embed.set_thumbnail(url=embed_url)
            try:
                x = prefix_check(ctx.guild.id)
                prefix = x.pref()
            except:
                prefix = config["APP"]["Prefix"]

            # Loop every entry in the database
            for entry in response:
                if entry["Visible"] == "True":
                    # Add embed from entry
                    embed.add_field(name=f'**{prefix+entry["CommandName"]}**', value=entry["CommandDescription"], inline=False)
            embed.add_field(name="\uFEFF", value="Stuck? [Check the documentation](https://modus.enclavedb.net/)", inline=False)
            # sends embed after closing the db
            await ctx.send(embed=embed)

            # ==============================
            # Start of Admin Commands Embed
            # ==============================

            if ctx.author.guild_permissions.manage_channels:
                c.execute("SELECT * FROM en_AdminHelpCommands")
                response = c.fetchall()

                embed = discord.Embed(color=discord.Color.red(), title=":tools: Admin help commands!")
                embed.set_thumbnail(url=embed_url)

                # check for prefix with guild id
                try:
                    x = prefix_check(ctx.guild.id)
                    prefix = x.pref()
                except:
                    prefix = config["APP"]["Prefix"]

                # Loop every entry in the database
                for entry in response:
                    if entry["Visible"] == "True":
                        # Add embed from entry
                        embed.add_field(name=f'**{prefix+entry["CommandName"]}**', value=entry["CommandDescription"], inline=False)
                embed.add_field(name="\uFEFF", value="Stuck? [Check the documentation](https://modus.enclavedb.net/)", inline=False)
                # sends embed after closing the db
                await ctx.send(embed=embed)
            c.close()

    """
    ==============================
    Sub help command
    ==============================
    """
    @help.command()
    async def reactionroles(self, ctx):
        if ctx.author.guild_permissions.manage_channels:
            if ctx.guild:
                print(f"A user requested the command \"help reactionroles\" in {ctx.guild.name}")
            else:
                print(f"A user requested the command \"help reactionroles\" in a private message")

            c = MyDB("help")
            c.execute("SELECT * FROM en_AdminHelpReactionRolesCommands")
            response = c.fetchall()
            # starts a embed in discord
            embed = discord.Embed(color=discord.Color.red(), title=":tools: Admin help commands!")

            try:
                x = prefix_check(ctx.guild.id)
                prefix = x.pref()
            except:
                prefix = config["APP"]["Prefix"]

            # Loop every entry in the database
            for entry in response:
                if entry["Visible"] == "True":
                    # Add embed from entry
                    embed.add_field(name=f'**{prefix+entry["CommandName"]}**', value=entry["CommandDescription"], inline=False)
            # sends embed
            await ctx.send(embed=embed)
            c.close()

    """
    ==============================
    Sub help command
    ==============================
    """

    @help.command()
    async def fallout(self, ctx):
        if ctx.guild:
            print(f"A user requested the command \"help fallout\" in {ctx.guild.name}")
        else:
            print(f"A user requested the command \"help fallout\" in a private message")

        c = MyDB("help")
        c.execute("SELECT * FROM en_FalloutHelpCommands")
        response = c.fetchall()
        # starts a embed in discord
        embed = discord.Embed(color=0x80ff80, title=":radioactive: Fallout help commands!")
        embed.set_thumbnail(url=embed_url)

        # check for prefix with guild id
        try:
            x = prefix_check(ctx.guild.id)
            prefix = x.pref()
        except:
            prefix = config["APP"]["Prefix"]

        # Loop every entry in the database
        for entry in response:
            if entry["Visible"] == "True":
                # Add embed from entry
                embed.add_field(name=f'**{prefix+entry["CommandName"]}**', value=entry["CommandDescription"], inline=False)
        embed.add_field(name="\uFEFF", value="Stuck? [Check the documentation](https://modus.enclavedb.net/)", inline=False)
        await ctx.send(embed=embed)
        c.close()

    """
    ==============================
    Sub help command owner
    ==============================
    """

    @help.command(aliases=["owner"])
    @is_owner()
    async def secret(self, ctx):

        c = MyDB("help")
        c.execute("SELECT * FROM en_OwnerHelpCommands")
        response = c.fetchall()
        # starts a embed in discord
        embed = discord.Embed(color=discord.Color.red(), title="Owner help commands!")

        # check for prefix with guild id
        try:
            x = prefix_check(ctx.guild.id)
            prefix = x.pref()
        except:
            prefix = config["APP"]["Prefix"]

        # Loop every entry in the database
        for entry in response:
            # Add embed from entry
            embed.add_field(name=f'**{prefix+entry["CommandName"]}**', value=entry["CommandDescription"], inline=False)

        # sends embed
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(User_Help_Commands(client))
