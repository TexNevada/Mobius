# import discord library
import discord
# Imports commands
from discord.ext import commands
from discord import app_commands
import requests
import configparser


class Partner_F76_Plan_Collectors(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="tpc", description="Look up F76 plans using the plan collectors tool!")
    @app_commands.describe(search="Search for any plan in the game!",
                           page="Requires a number. Otherwise this will fail.")
    async def tpc(self, interaction: discord.Interaction, search: str, page: int = None):
        print(f"A user requested the Plan Collectors command")
        requestUrl = f"https://fed76.info/plan-api/?q={search}"
        try:
            if page is not None:
                if int(page) > 0:
                    requestUrl += f"&o={page}"
            requestUrl = requestUrl.replace(" ", "%20")
            r = requests.get(requestUrl)
            x = r.json()
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
            print("==============TPC=ERROR==============")
            # print(f"Request returned: {r.status_code}")
            print("Most of the time this is a user input error")
            print(e)
            print("==================END==================")

            await interaction.response.send_message("There seems to have been a connection error to The Plan Collectors Database. Please try again later")

    @commands.command(aliases=["TPC", "plan"])
    async def plancollectors(self, ctx, *, args=None):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])
        if args:
            try:
                argumentWords = args.split(" ")
                1 + int(argumentWords[-1])
                arg1 = " ".join(argumentWords[:-1])
                arg2 = argumentWords[-1]
            except ValueError:
                arg1 = args
                arg2 = "0"
            if ctx.guild:
                print(f"A user requested the Plan Collectors command in \"{ctx.guild.name}\"")
            else:
                print(f"A user requested the Plan Collectors command in a private message")
            if arg1 is None:
                await ctx.send("This tool is meant as a quick check on prices before you make your "
                               "judgement on selling or buying.\n"
                               "Here are examples of how to use the command.\n"
                               "Plain search: `>tpc underarmor`\n"
                               "Search with class/subclass filters: `>tpc camp/grahm/stone`\n"
                               "'Scrolling' the search: `>tpc underarmor 1`\n"
                               "Search only by filters: `>tpc camp/mischief/` (with '/' in the end)\n"
                               "Additional commands: `>tpc commands`")
            else:
                requestUrl = f"https://fed76.info/plan-api/?q={arg1}"
                try:
                    if int(arg2) > 0:
                        requestUrl += f"&o={arg2}"
                    requestUrl = requestUrl.replace(" ", "%20")
                    r = requests.get(requestUrl)
                    x = r.json()
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
                    await ctx.send(embed=embed)
                except Exception as e:
                    print("==============TPC=ERROR==============")
                    print(f"Request returned: {r.status_code}")
                    print("Most of the time this is a user input error")
                    print(e)
                    print("==================END==================")

                    await ctx.send(f"This tool is meant as a quick check on prices before you make your "
                                   f"judgement on selling or buying.\n"
                                   f"Here is a examples of how to use the command.\n"
                                   f"Plain search: `>tpc underarmor`\n"
                                   f"Search with class/subclass filters: `>tpc camp/grahm/stone`\n"
                                   f"'Scrolling' the search: `>tpc underarmor 1`\n"
                                   f"Search only by filters: `>tpc camp/mischief/` (with '/' in the end)\n"
                                   f"Additional commands: `>tpc commands`")
        else:
            await ctx.send(f"This tool is meant as a quick check on prices before you make your "
                           f"judgement on selling or buying.\n"
                           f"Here is a examples of how to use the command.\n"
                           f"Plain search: `>tpc underarmor`\n"
                           f"Search with class/subclass filters: `>tpc camp/grahm/stone`\n"
                           f"'Scrolling' the search: `>tpc underarmor 1`\n"
                           f"Search only by filters: `>tpc camp/mischief/` (with '/' in the end)\n"
                           f"Additional commands: `>tpc commands`")


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Partner_F76_Plan_Collectors(client))
