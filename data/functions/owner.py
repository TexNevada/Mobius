from discord.ext import commands
import configparser
from data.functions.logging import get_log
logger = get_log(__name__)


# defines the function is the user the owner.
def is_owner():
    # if the message from the user = his user ID then the user is owner
    async def predicate(ctx):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        for key, value in config.items("ADMIN"):
            if eval(config["Credentials"]["Active"]) is False:
                logger.log("Authentication is disabled")
            elif ctx.author.id == int(value):
                logger.info(f"Authenticated for {ctx.author}")
                return True
    return commands.check(predicate)
