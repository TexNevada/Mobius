from discord.ext import commands
import os
import data.functions.owner as owner


class _CogLoader(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def command(self, ctx):
        await ctx.send("Stuff")

    @commands.command()
    @owner.is_owner()
    async def reload(self, ctx):
        print(f"A reload command was executed in \"{ctx.guild.name}\" ")
        cogs = os.listdir("./data/cogs/")
        for item in ["_CogLoader.py", "__init__.py", "__pycache__"]:
            cogs.remove(item)
        error = []
        passed = []
        for cog in cogs:
            cog = cog.split(".")
            try:
                try:
                    self.client.unload_extension("data.cogs."+cog[0])
                except Exception as e:
                    error.append(e)
                self.client.load_extension("data.cogs."+cog[0])
                passed.append(cog[0])
            except Exception as e:
                error.append(e)
        if bool(error):
            await ctx.send(error)

        await ctx.send(passed)
        # self.client.unload_extension()
        # # loads extension
        # self.client.load_extension()
        # # If extension fails to load. Execption error
        #
        # await ctx.send(f"Refreshed the following cogs:\n{tempcoglist}")


def setup(client):
    client.add_cog(_CogLoader(client))
