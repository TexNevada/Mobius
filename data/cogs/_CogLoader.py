from discord.ext import commands
import os
import data.functions.owner as owner


class _CogLoader(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Loads the cog at the beginning
        cogs = os.listdir("./data/cogs/")
        for item in ["_CogLoader.py", "__init__.py", "__pycache__"]:
            cogs.remove(item)
        errors = []
        passed = []
        passed_chk = False
        for cog in cogs:
            cog = cog.split(".")
            try:
                self.client.load_extension("data.cogs." + cog[0])
                passed.append(cog[0])
                passed_chk = True
            except Exception as e:
                errors.append(cog[0])
                # TODO: Add check for error
        if bool(errors):
            for cog in errors:
                print(f"ERROR! Could not load the following `{cog}`")
        if passed_chk is True:
            for cog in passed:
                print(f"OK! Loaded {cog}")

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
                    self.client.unload_extension("data.cogs."+cog[0])
                except Exception as e:
                    error.append(e)
                self.client.load_extension("data.cogs."+cog[0])
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
                    self.client.unload_extension("data.cogs." + arg)
                except Exception as e:
                    error.append(e)
                self.client.load_extension("data.cogs." + arg)
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
                self.client.load_extension("data.cogs." + arg)
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
                self.client.unload_extension("data.cogs." + arg)
                passed = True
            except Exception as e:
                error.append(e)
            if bool(error):
                await ctx.send(error)
            if passed is True:
                await ctx.send(f"OK! Unloaded: {arg}")


def setup(client):
    client.add_cog(_CogLoader(client))
