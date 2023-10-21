# import discord library
import discord
# Imports commands
import aiohttp
import configparser

from discord import app_commands
from discord.ext import commands

from data.functions.logging import get_log
logger = get_log(__name__)



class fed76(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="fed76", description="Look up Fallout 76 weapon prices on FED76!")
    @app_commands.describe(item="Type in the item you wish to search for",
                           mods="Type in the mod(s) you wish to look for. Example: uny/ap/sent",
                           grade="Used with search of armor. Options are: [light, sturdy, heavy]")
    async def fed(self, interaction: discord.Interaction, item: str, mods: str, grade: str = None):
        logger.info("A user requested the FED76 command")
        async with aiohttp.ClientSession() as session:
            url = f"https://fed76.info/pricing-api/?item={item}&mods={mods}&grade={grade}"
            async with session.get(url) as http_response:
                x = await http_response.json()
                try:
                    embed = discord.Embed(color=0xc7974b, title="FED Legendary Item Value Estimator",
                                          url="https://fed76.info/i/item-pricing-tool")
                    embed.set_footer(text="Experienced traders can buy cheaper and sell higher")
                    embed.set_thumbnail(url=x["review"]["author"]["logo"])
                    if "Failed to interpret" in x['review']['description']:
                        embed.add_field(name=f"__**Unable to determine**__", value=x['name'], inline=True)
                    else:
                        embed.add_field(name=f"__**{x['category']}**__", value=x['name'], inline=True)
                    embed.add_field(name="__**FED Rating**__",
                                    value=f"{x['review']['reviewRating']['ratingValue']}/5.0", inline=True)
                    # embed.add_field(name="__**Price range**__", value=x['price'], inline=False)
                    if "Failed to interpret the key" in x['review']['description']:
                        embed.add_field(name="__**Recommendation**__",
                                        value="Could not interpret your mods. Please look up abbreviations for FED76 "
                                              "here: https://fed76.info/i/discord-abbreviations/",
                                        inline=False)
                    elif "Failed to interpret the item" in x['review']['description']:
                        embed.add_field(name="__**Recommendation**__",
                                        value="Could not interpret your item. Please check FED76 for supported items "
                                              "here: https://fed76.info/i/discord-abbreviations/",
                                        inline=False)
                    else:
                        embed.add_field(name="__**Recommendation**__", value=x['review']['description'], inline=False)

                    # Embed image
                    # file = discord.File(f"items/images/Fed76/HowToMobile.jpg", filename=f"HowToMobile.jpg")
                    # embed.set_image(url=f"attachment://HowToMobile.jpg")
                    embed.set_image(url="https://fed76.s3.eu-west-2.amazonaws.com/HowToPricing.jpg")
                    await interaction.response.send_message(embed=embed)
                except Exception as e:
                    logger.info("==============FED76=ERROR==============")
                    logger.info(f"Request returned: {r.status}")
                    logger.info("Most of the time this is a user input error")
                    logger.info(e)
                    logger.info("==================END==================")
                    await interaction.response.send_message("There seems to have been a connection error to FED76. Please try again later")

    @app_commands.command(name="fed76info", description="Look up information about weapons & items!")
    @app_commands.describe(item="Type in the item you wish to search for",
                           mods="Type in the mod(s) you wish to look for. Example: uny/ap/sent",
                           grade="Used with search of armor. Options are: [light, sturdy, heavy]")
    async def fed_info(self, interaction: discord.Interaction, item: str, mods: str = None, grade: str = None):
        logger.info(f"A user requested the FED76INFO command")

        if mods is None:
            mods = ""
        if grade is None:
            grade = ""
        async with aiohttp.ClientSession() as session:
            url = f"https://fed76.info/pricing/explain/?item={item}&mods={mods}&grade={grade}"
            async with session.get(url) as http_response:
                x = await http_response.json()
                try:
                    embed = discord.Embed(color=0xc7974b, title="FED76 - Item Pricing Tool for Fallout 76",
                                          url="https://fed76.info/i/item-pricing-tool")
                    embed.set_footer(text="")
                    embed.set_thumbnail(url='https://fed76.info/static/fed150.png')
                    embed.add_field(name=f"__**{x['names'][0]}**__", value=x['itemDescription'], inline=False)
                    for i in range(len(x['names'][1:])):
                        conditional = x['effectConditionalDescriptions'][i]
                        value = f"{x['effectDescriptions'][i]}\n```{conditional}```" if conditional else f"{x['effectDescriptions'][i]}"
                        embed.add_field(name=f"__**{x['names'][i + 1]}**__", value=value, inline=True)
                    # embed.add_field(name="__**FED Rating**__", value=f"{x['rating']}/5.0", inline=False)

                    # Bot runs the embed
                    await interaction.response.send_message(embed=embed)
                except Exception as e:
                    logger.info("==============FED76=ERROR==============")
                    logger.info(f"Request returned: {x.status}")
                    logger.info("Most of the time this is a user input error")
                    logger.info(e)
                    logger.info("==================END==================")

                    await interaction.response.send_message("Hmm. That didn't seem to work. Check abbreviations here: "
                                                            "https://fed76.info/i/discord-abbreviations/")

    @commands.command(aliases=["fed"])
    async def fed76(self, ctx):
        logger.info(f"A user requested a legacy command")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])

    @commands.command(aliases=["fedinfo"])
    async def fed76info(self, ctx, arg1=None, arg2=None, arg3=None):
        logger.info(f"A user requested a legacy command")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(fed76(client))
