import discord
from discord.ext import commands
import datetime


class User_General_Cmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def joined(self, ctx, *, member: discord.Member = None):
        print(f"A user requested when it joined \"{ctx.guild.name}\" ")
        """Says when a member joined."""
        if not member:
            member = ctx.author
        x = datetime.datetime.strptime(str(member.joined_at), "%Y-%m-%d %H:%M:%S.%f")
        x = x.strftime("%d %B %Y | %H:%M:%S UTC")
        embed = discord.Embed(title="Joined the server at:",
                              description=f"{x}", colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))
        await ctx.send(embed=embed)

    @commands.command()
    async def credits(self, ctx):
        if ctx.guild:
            print(f"A user requested the credits command in \"{ctx.guild.name}\" ")
        else:
            print("A user requested the credits command in a private message")
        await ctx.send("You can find the credits to the bot right here: "
                       "https://modus.enclavedb.net/books/changelog-credits-other/page/credits-significant-contributors")

    @commands.command()
    async def support(self, ctx):
        if ctx.guild:
            print(f"A user requested the support command in \"{ctx.guild.name}\"")
        else:
            print("A user requested the support command in a private message")
        await ctx.send("https://discord.gg/hMfgSaN")

    @commands.command()
    async def guilds(self, ctx):
        if ctx.guild:
            print(f"A user requested the guilds command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the guilds command in a private message")
        await ctx.send(f"MODUS is in {str(len(self.client.guilds))} servers so far!")

    @commands.command()
    async def invite(self, ctx):
        if ctx.guild:
            print(f"A user requested the invite command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the invite command in a private message")
        await ctx.send("https://discord.com/oauth2/authorize?client_id=532591107553624084&permissions=1879960790&scope=bot")

    @commands.command()
    async def ping(self, ctx):
        if ctx.guild:
            print(f"A user requested \"ping\" in \"{ctx.guild.name}\" ")
        else:
            print(f"A user requested \"ping\" in a private message")

        ping_ = self.client.latency
        ping = round(ping_ * 1000)
        await ctx.send(f"Ping result: `{str(ping)} ms`")


def setup(client):
    client.add_cog(User_General_Cmds(client))
