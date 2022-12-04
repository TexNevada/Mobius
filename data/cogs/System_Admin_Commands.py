import discord
from discord.ext import commands
import time
from data.functions.owner import is_owner
from data.functions.MySQL_Connector import MyDB


class owner(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(aliases=["lam"])
    @is_owner()
    async def listallmembers(self, ctx):
        try:
            print(f"Listed members in all server in {ctx.guild.name}")
        except:
            print("Listed members in private message")
        activeServers = self.client.guilds
        sum = 0
        for s in activeServers:
            sum += len(s.members)
        await ctx.send(f"There is {sum} members in total of {len(self.client.guilds)} servers")

    # # logs out the bot from discord
    # @commands.command()
    # # User must have the role to continue
    # @is_owner()
    # async def memory(self, ctx):
    #     import os
    #     import psutil
    #     memory_usage = psutil.virtual_memory()
    #     totalGB = round(float(memory_usage.total)/(1024*1024*1024), 3)
    #     usedGB = round(float(memory_usage.used)/(1024*1024*1024), 3)
    #
    #     process = psutil.Process(os.getpid())
    #     process_usage = round(process.memory_percent(), 3)
    #
    #     embed = discord.Embed(title='Memory usage', colour=ctx.author.colour)
    #     embed.add_field(name='MODUS USAGE', value=f"{process_usage}%/{totalGB}GB", inline=False)
    #     embed.add_field(name='SQL USAGE', value=f"{process_usage}%/{totalGB}GB PLACEHOLDER", inline=False)
    #     embed.add_field(name='TOTAL USAGE', value=f"{usedGB}GB/{totalGB}GB", inline=False)
    #
    #     await ctx.send(content=None, embed=embed)  # in bytes

    # @commands.command()
    # @is_owner()
    # async def publish(self, ctx, *, content: str):
    #     try:
    #         list = []
    #         for x in list:
    #             url = x
    #             try:
    #                 webhook = Webhook.from_url(url, adapter=RequestsWebhookAdapter())
    #                 webhook.send(content=content, username=ctx.author.name, avatar_url=ctx.author.avatar_url)
    #             except Exception as e:
    #                 # await ctx.send("Error pushing message to {} in channel {}".format(str(x["GuildName"]), x["ChannelName"]))
    #                 await ctx.send(e)
    #         await ctx.send("I've pushed the message to all webhooks.")
    #     except Exception as e:
    #         await ctx.send("Something went wrong")
    #         await ctx.send(e)

    @commands.group(case_insensitive=True)
    @is_owner()
    async def display(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Error: No argument given.")

    @display.command()
    @is_owner()
    async def playing(self, ctx, *, arg:str):
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Game(name=arg))

    @display.command()
    @is_owner()
    async def streaming(self, ctx, arg2, *, arg:str):
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Streaming(name=arg, url=arg2))

    @display.command()
    @is_owner()
    async def listening(self, ctx, *, arg):
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Activity(type=discord.ActivityType.listening, name=arg))

    @display.command()
    @is_owner()
    async def watching(self, ctx, *, arg:str):
        await self.client.change_presence(status=discord.Status.online,
                                          activity=discord.Activity(type=discord.ActivityType.watching, name=arg))

    # Plan is to move this over to be a admin command eventually.
    # Command is not ours. Its copied from the internet.
    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @is_owner()
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        # A simple command which checks a members Guild Permissions.
        # If member is not provided, the author will be checked.

        if not member:
            member = ctx.author

        # Here we check if the value of each permission is True.
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        # And to make it look nice, we wrap it in an Embed.
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        # \uFEFF is a Zero-Width Space, which basically allows us to have an empty field name.
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        # Thanks to Gio for the Command.

    @commands.command()
    @is_owner()
    async def mysqlping(self, ctx):
        start = time.time()
        c = MyDB("essential")
        c.execute("SELECT * FROM GuildTable where GuildID = %s", (ctx.guild.id,))
        c.fetchone()
        await ctx.send(f'It took {time.time()-start} seconds.')

    @commands.command()
    @is_owner()
    async def guildshard(self, ctx):
        await ctx.send(f"This guild shard id: {ctx.guild.shard_id}")


async def setup(client: commands.Bot):
    await client.add_cog(owner(client))
