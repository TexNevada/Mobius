import discord
from discord.ext import commands
from discord import app_commands
from typing import Literal
from data.functions.MySQL_Connector import MyDB
import configparser
from data.functions.logging import get_log
logger = get_log(__name__)


# start of the extension as a class.
class User_F76_Mutations(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="mutation", description="Allows you to look up information about Fo76's mutations!")
    async def _mutation(self, interaction: discord.Interaction,
                        mutation: Literal["Adrenal Reaction", "Bird Bones", "Carnivore", "Chameleon", "Eagle Eyes",
                                          "Egg Head", "Electrically Charged", "Empath", "Grounded", "Healing Factor",
                                          "Herbivore", "Herd Mentality", "Marsupial", "Plague Walker", "Scaly Skin",
                                          "Speed Demon", "Talons", "Twisted Muscles", "Unstable Isotope"]):
        logger.info(f"A user requested the mutation command")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        c = MyDB("fallout")
        c.execute("SELECT * FROM en_Mutations WHERE Mutation LIKE %s", ('%{}%'.format(mutation),))
        response = c.fetchone()
        embed = discord.Embed(color=0x28df28, title=f"The {response['Mutation']} Mutation")

        # embed.set_footer(text="This was brought to you by Enclave Database automated reply system")
        # embed.set_image(url="https://i.imgur.com/XaNIjHG.png")

        if response["ImageURL"]:
            # embed.set_thumbnail(url=response["ImageURL"])
            embed.set_image(url=response["ImageURL"])
        # embed.set_author(name=f"The {response['Mutation']} Mutation")
        embed.set_thumbnail(url=config["EDB.TOOLS"]["F76_Mutation"])

        embed.add_field(name="__**Mutation effects**__",
                        value=f"**Positive effects:** {response['PositiveEffects']}\n"
                              f"**Negative effects:** {response['NegativeEffects']}",
                        inline=False)
        # Adding as space between fields
        # embed.add_field(name="\uFEFF", value="\uFEFF", inline=False)
        embed.add_field(
            name=f"__**{response['Mutation']} serum can by doing the following requirements**__",
            value=f"**Requirements:** {response['Requirements']}\n"
                  f"**Materials:** {response['Materials']}",
            inline=False)
        # Bot runs the embed
        embed.set_footer(text="Special thanks to Shia for the art!\n"
                              "You can find him here: https://www.deviantart.com/overshia")
        await interaction.response.send_message(embed=embed)
        c.close()

    @commands.command()
    async def mutation(self, ctx):
        logger.info(f"A user requested a legacy command")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(User_F76_Mutations(client))
