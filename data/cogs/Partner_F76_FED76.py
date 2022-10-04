# import discord library
import discord
# Imports commands
from discord.ext import commands
from discord import app_commands
import requests
import configparser


class fed76(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="fed76", description="Look up Fallout 76 weapon prices on FED76!")
    async def fed(self, interaction: discord.Interaction, item: str, mods: str, grade: str = None):
        r = requests.get(f"https://fed76.info/pricing-api/?item={item}&mods={mods}&grade={grade}")
        try:
            x = r.json()
            embed = discord.Embed(color=0xc7974b, title="FED Legendary Item Value Estimator",
                                  url="https://fed76.info/i/item-pricing-tool")
            embed.set_footer(text="Experienced traders can buy cheaper and sell higher")
            embed.set_thumbnail(url=x["review"]["author"]["logo"])
            embed.add_field(name=f"__**{x['category']}**__", value=x['name'], inline=True)
            embed.add_field(name="__**FED Rating**__",
                            value=f"{x['review']['reviewRating']['ratingValue']}/5.0", inline=True)
            # embed.add_field(name="__**Price range**__", value=x['price'], inline=False)
            embed.add_field(name="__**Recommendation**__", value=x['review']['description'], inline=False)

            # Embed image
            # file = discord.File(f"items/images/Fed76/HowToMobile.jpg", filename=f"HowToMobile.jpg")
            # embed.set_image(url=f"attachment://HowToMobile.jpg")
            embed.set_image(url="https://fed76.s3.eu-west-2.amazonaws.com/HowToPricing.jpg")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print("==============FED76=ERROR==============")
            print(f"Request returned: {r.status_code}")
            print("Most of the time this is a user input error")
            print(e)
            print("==================END==================")
            await interaction.response.send_message("There seems to have been a connection error to FED76. Please try again later")

    @app_commands.command(name="fed76info", description="Look up information about weapons & items!")
    async def fed_info(self, interaction: discord.Interaction, item: str, mods: str = None, grade: str = None):
        print(f"A user requested the FED76INFO command")

        if mods is None:
            mods = ""
        if grade is None:
            grade = ""
        r = requests.get(f"https://fed76.info/pricing/explain/?item={item}&mods={mods}&grade={grade}")
        try:
            x = r.json()
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
            print("==============FED76=ERROR==============")
            print(f"Request returned: {r.status_code}")
            print("Most of the time this is a user input error")
            print(e)
            print("==================END==================")

            await interaction.response.send_message("Hmm. That didn't seem to work. Check abbreviations here: "
                                                    "https://fed76.info/i/discord-abbreviations/")


    @commands.command(aliases=["fed"])
    async def fed76(self, ctx, arg1=None, arg2=None, arg3=None):
        if ctx.guild:
            print(f"A user requested the FED76 command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the FED76 command in a private message")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])
        if arg2 is None:
            await ctx.send("This tool is meant as a quick check on prices before you make your judgement on selling or "
                           "buying.\n"
                           "Check out https://fed76.info/i/discord-abbreviations/ for abbreviations on how to use "
                           "this tool.\n"
                           "Here is a examples of how to use the command.\n"
                           "Weapon search: `>Fed76 tesla q/25/25`\n"
                           "Armor search: `>Fed76 metal uny/ap/sent heavy`")
        else:
            r = requests.get(f"https://fed76.info/pricing-api/?item={arg1}&mods={arg2}&grade={arg3}")
            try:
                x = r.json()
                embed = discord.Embed(color=0xc7974b, title="FED Legendary Item Value Estimator",
                                      url="https://fed76.info/i/item-pricing-tool")
                embed.set_footer(text="Experienced traders can buy cheaper and sell higher")
                embed.set_thumbnail(url=x["review"]["author"]["logo"])
                embed.add_field(name=f"__**{x['category']}**__", value=x['name'], inline=True)
                embed.add_field(name="__**FED Rating**__",
                                value=f"{x['review']['reviewRating']['ratingValue']}/5.0", inline=True)
                # embed.add_field(name="__**Price range**__", value=x['price'], inline=False)
                embed.add_field(name="__**Recommendation**__", value=x['review']['description'], inline=False)

                # Embed image
                # file = discord.File(f"items/images/Fed76/HowToMobile.jpg", filename=f"HowToMobile.jpg")
                # embed.set_image(url=f"attachment://HowToMobile.jpg")
                embed.set_image(url="https://fed76.s3.eu-west-2.amazonaws.com/HowToPricing.jpg")
                await ctx.send(embed=embed)
            except Exception as e:
                print("==============FED76=ERROR==============")
                print(f"Request returned: {r.status_code}")
                print("Most of the time this is a user input error")
                print(e)
                print("==================END==================")

                await ctx.send("This tool is meant as a quick check on prices before you make your judgement on "
                               "selling or buying.\n"
                               "Check out https://fed76.info/i/discord-abbreviations/ for abbreviations on how to "
                               "use this tool.\n"
                               "Here is a examples of how to use the command.\n"
                               "Weapon search: `>Fed76 tesla q/25/25`\n"
                               "Armor search: `>Fed76 metal uny/ap/sent heavy`")

    @commands.command(aliases=["fedinfo"])
    async def fed76info(self, ctx, arg1=None, arg2=None, arg3=None):
        if ctx.guild:
            print(f"A user requested the FED76INFO command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the FED76INFO command in a private message")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])
        if arg1 is None:
            await ctx.send(
                "This tool provides additional information regarding legendary items, effects, and how they go together..\n"
                "Check out https://fed76.info/i/discord-abbreviations/ for abbreviations on how to use this tool.\n"
                "Here is a examples of how to use the command.\n"
                "Weapon search: `>fedinfo tesla q/25/25`\n"
                "Armor search: `>fedinfo metal uny/ap/sent heavy`"
                "Effect search: '>fedinfo junkies'")
        else:
            if arg2 is None:
                arg2 = ""
            if arg3 is None:
                arg3 = ""
            r = requests.get(f"https://fed76.info/pricing/explain/?item={arg1}&mods={arg2}&grade={arg3}")
            try:
                x = r.json()
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
                await ctx.send(embed=embed)
            except Exception as e:
                print("==============FED76=ERROR==============")
                print(f"Request returned: {r.status_code}")
                print("Most of the time this is a user input error")
                print(e)
                print("==================END==================")

                await ctx.send("Hmm. That didn't seem to work. Check abbreviations here: "
                               "https://fed76.info/i/discord-abbreviations/")


# ends the extension
async def setup(client) -> None:
    await client.add_cog(fed76(client))
