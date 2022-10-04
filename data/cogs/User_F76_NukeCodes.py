# import discord library
import json

import discord
# Imports commands
from discord.ext import commands
from discord import app_commands
import requests
# Allows the code to retrieve data online
from datetime import datetime
import configparser


class User_F76_NukeCodes(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__() # Important for grouping Slash commands

    @app_commands.command(name="codes", description="Will output the current nuke codes for Fallout 76")
    async def codes(self, interaction: discord.Interaction) -> None:
        """ /codes """
        print("A user requested nuke codes")
        config = configparser.ConfigParser()
        config.read("./config.ini")

        data = config["NukaCrypt"]["API_key"]
        header = config["NukaCrypt"]["Header"]
        r = requests.post(url=f'https://nukacrypt.com/api/codes', data=json.loads(data), headers=json.loads(header))
        response = r.json()
        code_response = f'Nuke codes reset every <t:{response["since_epoch"]+604800}:F> \n' \
                        f'**Alpha**: {response["ALPHA"]}\n' \
                        f'**Bravo**: {response["BRAVO"]}\n' \
                        f'**Charlie**: {response["CHARLIE"]}'

        embed = discord.Embed(color=0xe7e9d3, title="Fallout 76 Nuclear Codes")

        embed.set_footer(text="Special thanks to https://nukacrypt.com/ for providing codes for all these years!")
        # embed.set_image(url="")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        embed.set_thumbnail(url=config["EDB.TOOLS"]["F76_NukeCodes"])

        embed.add_field(name="This week's nuclear codes",
                        value=code_response)

        # await interaction.response.send_message(code_response)
        await interaction.response.send_message(embed=embed)

    @commands.command(name="codes", aliases=["nukecodes", "nukecode", "nc", "code", "cc"])
    async def _codes(self, ctx):
        print("A user requested nuke codes")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])

        # Command will still function for the time being.
        config = configparser.ConfigParser()
        config.read("./config.ini")

        data = config["NukaCrypt"]["API_key"]
        header = config["NukaCrypt"]["Header"]
        r = requests.post(url=f'https://nukacrypt.com/api/codes', data=json.loads(data), headers=json.loads(header))
        response = r.json()
        code_response = f'Nuke codes reset every <t:{response["since_epoch"]+604800}:F> \n' \
                        f'**Alpha**: {response["ALPHA"]}\n' \
                        f'**Bravo**: {response["BRAVO"]}\n' \
                        f'**Charlie**: {response["CHARLIE"]}'
        await ctx.send(code_response)


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(User_F76_NukeCodes(client))
