# import discord library
import discord
# Imports commands
from discord.ext import commands
import requests
from pprint import pprint
import re


class User_F76_Seasons(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["sr", "seasons"])
    async def season(self, ctx, *, arg=None):
        if arg is None:
            rank = []
            rank_info = []
            r = requests.get("https://fallout.bethesda.net/api/v1/pages?route=/seasons&lang=en")
            response = r.json()
            seasons_lists = response["sections"][2]["data"]["categories"]
            for rank_list in seasons_lists:
                for another_list in rank_list["items"]:
                    rank.append(another_list["rank_title"])
                    rank_info.append(another_list["title"])

            # Removes HTML from string because Bethesda can't do it themselves.
            def html_rm(input):
                result = re.compile(r"<.*?>")
                return result.sub("", input)
            embed = discord.Embed(color=0x47758e, title=f'Here are the {response["sections"][2]["data"]["title"]}',
                                  description=html_rm(response["sections"][2]["data"]["content"]))
            embed.set_thumbnail(url=f'https:{response["sections"][2]["data"]["categories"][0]["items"][0]["image"]}')
            embed2 = discord.Embed(color=0x47758e)
            embed3 = discord.Embed(color=0x47758e)
            embed4 = discord.Embed(color=0x47758e)
            nr = 0
            while rank:
                try:
                    if nr > 75:
                        embed4.add_field(name=rank[nr], value=rank_info[nr])
                    elif nr > 50:
                        embed3.add_field(name=rank[nr], value=rank_info[nr])
                    elif nr > 24:
                        embed2.add_field(name=rank[nr], value=rank_info[nr])
                    else:
                        embed.add_field(name=rank[nr], value=rank_info[nr])
                    nr = nr + 1
                except:
                    break
            embeds = [embed, embed2, embed3, embed4]
            for embed in embeds:
                await ctx.send(embed=embed)
        else:
            if "rank" not in arg:
                arg = f"rank {arg}"
            rank = arg.lower()
            r = requests.get("https://fallout.bethesda.net/api/v1/pages?route=/seasons&lang=en")
            response = r.json()
            seasons_lists = response["sections"][2]["data"]["categories"]
            for rank_list in seasons_lists:
                for another_list in rank_list["items"]:
                    if rank == another_list["rank_title"].lower() or rank+" " == another_list["rank_title"].lower():
                        embed = discord.Embed(color=0x47758e, title=f'At {another_list["rank_title"]} you will get:')
                        embed.set_image(url=f'https:{another_list["image"]}')
                        embed.add_field(name=another_list["title"], value=another_list["content"])
                        embed.set_footer(text="You can enlarge the pictures by clicking on them")
                        await ctx.send(embed=embed)
            else:
                # await ctx.send("Couldn't find anything")
                return


# ends the extension
def setup(client):
    client.add_cog(User_F76_Seasons(client))

