import discord
import discord.ext.commands
from discord.ext import commands
from discord import app_commands
import datetime
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")


class User_General_Cmds(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    # @app_commands.command(description="Allows")
    # @commands.guild_only()
    # async def _joined(self, ctx, *, member: discord.Member = None):
    #     print(f"A user requested when it joined \"{ctx.guild.name}\" ")
    #     """Says when a member joined."""
    #     if not member:
    #         member = ctx.author
    #     x = datetime.datetime.strptime(str(member.joined_at), "%Y-%m-%d %H:%M:%S.%f")
    #     x = x.strftime("%d %B %Y | %H:%M:%S UTC")
    #     embed = discord.Embed(title="Joined the server at:",
    #                           description=f"{x}", colour=member.colour)
    #     embed.set_author(icon_url=member.avatar_url, name=str(member))
    #     await ctx.send(embed=embed)

    # @commands.command()
    # async def credits(self, ctx):
    #     if ctx.guild:
    #         print(f"A user requested the credits command in \"{ctx.guild.name}\" ")
    #     else:
    #         print("A user requested the credits command in a private message")
    #     conf = configparser.ConfigParser()
    #     conf.read("./config.ini")
    #     await ctx.send(config["LEGACY"]["UseSlash"])
    #     await ctx.send(f"You can find the credits to the bot right here: {conf['APP']['Credits']}")

    @commands.command()
    async def support(self, ctx):
        if ctx.guild:
            print(f"A user requested the support command in \"{ctx.guild.name}\"")
        else:
            print("A user requested the support command in a private message")
        conf = configparser.ConfigParser()
        conf.read("./config.ini")
        await ctx.send(conf["APP"]["Discord"])

    @commands.command()
    async def guilds(self, ctx):
        if ctx.guild:
            print(f"A user requested the guilds command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the guilds command in a private message")
        await ctx.send(f"{config['APP']['Bot_Name']} is in {str(len(self.client.guilds))} servers so far!")

    @commands.command()
    async def invite(self, ctx):
        if ctx.guild:
            print(f"A user requested the invite command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the invite command in a private message")
        await ctx.send("You can invite me to your server by pressing on my "
                       "profile picture and then \"Add to server\" button")

    @commands.command()
    async def ping(self, ctx):
        if ctx.guild:
            print(f"A user requested \"ping\" in \"{ctx.guild.name}\" ")
        else:
            print(f"A user requested \"ping\" in a private message")

        ping_ = self.client.latency
        ping = round(ping_ * 1000)
        await ctx.send(f"Ping result: `{str(ping)} ms`")

    @commands.command()
    @commands.guild_only()
    async def enlarge(self, ctx, *, member: discord.Member = None):
        print(f"A user requested to enlarge a user profile image in \"{ctx.guild.name}\" ")
        try:
            if not member:
                member = ctx.author
            embed = discord.Embed(colour=member.colour, title=str(member))
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(f"Could not find anyone by the name {member}")











    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member = None):
        print(f"A user requested when it joined \"{ctx.guild.name}\" ")
        """Says when a member joined."""
        await ctx.send(config["LEGACY"]["UseSlash"])
        if not member:
            member = ctx.author
        x = datetime.datetime.strptime(str(member.joined_at), "%Y-%m-%d %H:%M:%S.%f")
        x = x.strftime("%d %B %Y | %H:%M:%S UTC")
        embed = discord.Embed(title="Joined the server at:",
                              description=f"{x}", colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        await ctx.send(embed=embed)

    # @commands.command()
    # async def credits(self, ctx):
    #     if ctx.guild:
    #         print(f"A user requested the credits command in \"{ctx.guild.name}\" ")
    #     else:
    #         print("A user requested the credits command in a private message")
    #     conf = configparser.ConfigParser()
    #     conf.read("./config.ini")
    #     await ctx.send(config["LEGACY"]["UseSlash"])
    #     await ctx.send(f"You can find the credits to the bot right here: {conf['APP']['Credits']}")

    @commands.command()
    async def support(self, ctx):
        if ctx.guild:
            print(f"A user requested the support command in \"{ctx.guild.name}\"")
        else:
            print("A user requested the support command in a private message")
        conf = configparser.ConfigParser()
        conf.read("./config.ini")
        await ctx.send(conf["APP"]["Discord"])

    @commands.command()
    async def guilds(self, ctx):
        if ctx.guild:
            print(f"A user requested the guilds command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the guilds command in a private message")
        await ctx.send(f"{config['APP']['Bot_Name']} is in {str(len(self.client.guilds))} servers so far!")

    @commands.command()
    async def invite(self, ctx):
        if ctx.guild:
            print(f"A user requested the invite command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the invite command in a private message")
        await ctx.send("You can invite me to your server by pressing on my "
                       "profile picture and then \"Add to server\" button")

    @commands.command()
    async def ping(self, ctx):
        if ctx.guild:
            print(f"A user requested \"ping\" in \"{ctx.guild.name}\" ")
        else:
            print(f"A user requested \"ping\" in a private message")

        ping_ = self.client.latency
        ping = round(ping_ * 1000)
        await ctx.send(f"Ping result: `{str(ping)} ms`")

    @commands.command()
    @commands.guild_only()
    async def enlarge(self, ctx, *, member: discord.Member = None):
        print(f"A user requested to enlarge a user profile image in \"{ctx.guild.name}\" ")
        try:
            if not member:
                member = ctx.author
            embed = discord.Embed(colour=member.colour, title=str(member))
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)
        except Exception:
            await ctx.send(f"Could not find anyone by the name {member}")


def setup(client):
    client.add_cog(User_General_Cmds(client))
