from discord.ext import commands
import topgg
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")


class top_gg(commands.Cog):
    """Handles interactions with the top.gg API"""
    if config["Credentials"]["top_gg_token"] != "":
        def __init__(self, client: commands.Bot) -> None:
            self.client = client
            topgg.DBLClient(self.client, config["Credentials"]["top_gg_token"], autopost=True, post_shard_count=True)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(top_gg(client))
