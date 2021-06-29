from discord.ext import commands
import configparser


# defines the function is the user the owner.
def is_owner():
    # if the message from the user = his user ID then the user is owner
    async def predicate(ctx):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        for key, value in config.items("ADMIN"):
            if eval(config["Credentials"]["Active"]) is True:
                # TODO: Authentication could be logged.
                pass
            if ctx.author.id == int(value):
                return True
    return commands.check(predicate)
