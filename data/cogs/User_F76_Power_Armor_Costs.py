# import discord library
import discord
# Imports commands
from discord.ext import commands
from data.functions.MySQL_Connector import MyDB
import configparser


class User_F76_Power_Armor_Costs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def PACost(self, ctx, arg: str):
        if ctx.guild:
            print(f"A user requested the PACost command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the PACost command in a DM")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        c = MyDB("fallout")
        if arg is None:
            await ctx.send("Please specify what Power Armor you wish to get the costs for")
        else:
            c.execute("SELECT * FROM en_PACost WHERE PowerArmor LIKE %s", ('%{}%'.format(arg),))
            response = c.fetchall()

            try:
                embed = discord.Embed(color=0xffff00, title=response[0]["PowerArmor"])
                embed.set_thumbnail(url=config["EDB.TOOLS"]["F76_Power_Armor_Costs"])
                embed.add_field(name="{}".format(response[0]["LVL"]),
                                value="{}".format(response[0]["MaterialCost"]),
                                inline=True)
                if len(response) >= 2:
                    embed.add_field(name="{}".format(response[1]["LVL"]),
                                    value="{}".format(response[1]["MaterialCost"]),
                                    inline=True)
                    if len(response) >= 3:
                        embed.add_field(name="{}".format(response[2]["LVL"]),
                                        value="{}".format(response[2]["MaterialCost"]),
                                        inline=True)
                embed.set_footer(text="The power armor costs above is the base cost and can be lowered "
                                      "with Power Smith perk card.")
                await ctx.send(embed=embed)

            except IndexError:
                await ctx.send(f"Could not find anything with \"{arg}\" ")

            except Exception as e:
                print("==============PA=ERROR==============")
                print("Something went wrong here. Check log below")
                print(e)
                print("==================END==================")
                await ctx.send("Something went very wrong here. Contact support here https://discord.gg/hMfgSaN!")
        c.close()


def setup(client):
    client.add_cog(User_F76_Power_Armor_Costs(client))
