from discord.ext import commands
import configparser
config = configparser.ConfigParser()


# defines the function is the user the owner.
def is_owner():
    # if the message from the user = his user ID then the user is owner
    async def predicate(ctx):
        config.read("./config.ini")
        for key, value in config.items("ADMIN"):
            print(key, value)
            if ctx.author.id == int(value):
                return True
    return commands.check(predicate)
