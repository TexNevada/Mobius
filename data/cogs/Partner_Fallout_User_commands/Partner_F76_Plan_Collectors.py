# import discord library
import discord
# Imports commands
import aiohttp
import configparser
from discord import app_commands
from discord.ext import commands
from data.functions.logging import get_log
logger = get_log(__name__)

class Partner_F76_Plan_Collectors(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="tpc", description="Look up F76 plans using the plan collectors tool!")
    @app_commands.describe(search="Search for any plan in the game!",
                           page="Requires a number. Otherwise this will fail.")
    async def tpc(self, interaction: discord.Interaction, search: str, page: int = None):
        logger.info(f"A user requested the Plan Collectors command")
        requestUrl = f"https://fed76.info/plan-api/?q={search}"
        try:
            if page is not None:
                if int(page) > 0:
                    requestUrl += f"&o={page}"
            else:
                requestUrl += f"&o=1"
            requestUrl = requestUrl.replace(" ", "%20")
            async with aiohttp.ClientSession() as session:
                url = requestUrl
                async with session.get(url) as http_response:
                    x = await http_response.json()
                    if x["plan_count"] > 5:
                        embed = discord.Embed(color=0x477097,
                                              title="Click this link to see full search results on the website",
                                              url=x["link"])
                        embed.add_field(name=f"__**Message:**__", value=x['message'])
                    elif x['plan_count'] < 0:  # displays custom message
                        embed = discord.Embed(color=0x477097,
                                              title="The Plan Collectors (click to visit)",
                                              description=x['message'],
                                              url=x["link"])
                        if x["image"]:
                            embed.set_image(url=x["image"])
                    else:  # plans are only displayed if there's less than 6 of them, suggestion message is displayed otherwise
                        embed = discord.Embed(color=0x477097,
                                              title="Plan Pricecheck",
                                              url=x["link"])
                        if x['plans']:
                            for plan in x["plans"]:
                                if not plan["tradeable"]:
                                    embed.add_field(name=plan['name'], value=f"**Tradable:** False", inline=False)
                                else:
                                    embed.add_field(name=plan['name'], value=plan['verdict'], inline=False)
                        else:
                            embed.add_field(name='Unfortunately', value=x['message'], inline=False)
                    if x['warnings']:
                        embed.set_footer(text=("\n".join(x['warnings'])))
                    else:
                        embed.set_footer(text='The Plan Collectors')
                    embed.set_thumbnail(url=x["review"]["author"]["logo"])
                    # Bot runs the embed
                    await interaction.response.send_message(embed=embed)
        except Exception as e:
            logger.info("==============TPC=ERROR==============")
            logger.info(f"Request returned: {x.status}")
            logger.info(e)
            logger.info("==================END==================")

            await interaction.response.send_message("There seems to have been a connection error to The Plan Collectors Database. Please try again later")

    @commands.command(aliases=["TPC", "plan"])
    async def plancollectors(self, ctx, *, args=None):
        logger.info(f"A user requested a legacy command")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Partner_F76_Plan_Collectors(client))
