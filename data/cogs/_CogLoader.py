from discord.ext import commands, tasks
import discord
import os
import data.functions.owner as owner
import configparser


class _CogLoader(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        # self.load_all.start()

    # @tasks.loop(count=1)
    # async def load_all(self):
    #     # Loads the cog at the beginning
    #     cogs = os.listdir("./data/cogs/")
    #     for item in ["_CogLoader.py", "__init__.py", "__pycache__", "Unfinished cogs"]:
    #         cogs.remove(item)
    #     errors = []
    #     passed = []
    #     passed_chk = False
    #     for cog in cogs:
    #         cog = cog.split(".")
    #         try:
    #             await self.client.load_extension("data.cogs." + cog[0])
    #             passed.append(cog[0])
    #             passed_chk = True
    #         except Exception as e:
    #             errors.append(cog[0])
    #             config = configparser.ConfigParser()
    #             config.read("./config.ini")
    #             if config["APP"]["Debug"] == "DEBUG":
    #                 print(e)
    #     if bool(errors):
    #         for cog in errors:
    #             print(f"ERROR! Could not load the following `{cog}`")
    #     if passed_chk is True:
    #         for cog in passed:
    #             print(f"OK! Loaded {cog}")
    #     # await self.client.tree.sync(guild=discord.Object(id=704725246187536489))

    @commands.group(case_insensitive=True)
    @owner.is_owner()
    async def cog(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Available subcommands: reload, reload_all, load, unload")

    @cog.command()
    @owner.is_owner()
    async def reload_all(self, ctx):
        cogs = os.listdir("./data/cogs/")
        for item in ["_CogLoader.py", "__init__.py", "__pycache__"]:
            cogs.remove(item)
        error = []
        passed = []
        passed_chk = False
        for cog in cogs:
            cog = cog.split(".")
            try:
                try:
                    await self.client.unload_extension("data.cogs."+cog[0])
                except Exception as e:
                    error.append(e)
                await self.client.load_extension("data.cogs."+cog[0])
                passed.append(cog[0])
                passed_chk = True
            except Exception as e:
                error.append(e)
        if bool(error):
            await ctx.send(f"ERROR! Could not load the following\n`{error}`")
        if passed_chk is True:
            await ctx.send(passed)

    @cog.command()
    @owner.is_owner()
    async def reload(self, ctx, arg: str = None):
        if arg is None:
            await ctx.send("No cog was given.")
        else:
            error = []
            passed = False
            try:
                try:
                    await self.client.unload_extension("data.cogs." + arg)
                except Exception as e:
                    error.append(e)
                await self.client.load_extension("data.cogs." + arg)
                passed = True
            except Exception as e:
                error.append(e)
            if bool(error):
                await ctx.send(error)
            if passed is True:
                await ctx.send(f"OK! Reloaded: {arg}")

    @cog.command()
    @owner.is_owner()
    async def load(self, ctx, arg: str = None):
        if arg is None:
            await ctx.send("No cog was given.")
        else:
            error = []
            passed = False
            try:
                await self.client.load_extension("data.cogs." + arg)
                passed = True
            except Exception as e:
                error.append(e)
            if bool(error):
                await ctx.send(error)
            if passed is True:
                await ctx.send(f"OK! Loaded: {arg}")

    @cog.command()
    @owner.is_owner()
    async def unload(self, ctx, arg: str = None):
        if arg is None:
            await ctx.send("No cog was given.")
        else:
            error = []
            passed = False
            try:
                await self.client.unload_extension("data.cogs." + arg)
                passed = True
            except Exception as e:
                error.append(e)
            if bool(error):
                await ctx.send(error)
            if passed is True:
                await ctx.send(f"OK! Unloaded: {arg}")


async def setup(client: commands.Bot):
    await client.add_cog(_CogLoader(client))
