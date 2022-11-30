"""
Extension name: Creatures
Author: Tex Nevada
Created: 07.05.19 - Europe
"""
# import discord library
import discord
# Imports commands
from discord.ext import commands
from spellchecker import SpellChecker
from data.functions.MySQL_Connector import MyDB

spell = SpellChecker()
spell.word_frequency.load_text_file("./data/cogs_data/F76_Perk_Cards_List.txt")

spellNW = SpellChecker()
spellNW.word_frequency.load_text_file("./data/cogs_data/F76_Nuclear_Winter_Perk_Cards_List.txt")


class User_F76_PerkCards(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="perkcard", aliases=["perk"])
    async def perk_card(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("You need to specify the perk you want to look")
        else:
            async with ctx.channel.typing():
                if ctx.guild:
                    print(f"A user requested the perk card command in \"{ctx.guild.name}\"")
                else:
                    print(f"A user requested the perk card command in a DM")

                c = MyDB("fallout")
                c.execute("SELECT * FROM en_PerkCards WHERE PerkName LIKE %s", ('%{}%'.format(arg),))
                response = c.fetchall()
                if not response:
                    print(f"Checking spell checker with the following word: {arg}")
                    entryNR = 0
                    for entry in spell.candidates(arg):
                        entryNR = entryNR + 1
                        c.execute("SELECT * FROM en_PerkCards WHERE PerkName LIKE %s", ('%{}%'.format(entry),))
                        response = c.fetchall()
                        if response or entryNR == 3:
                            break

                # sets extra perks if response length greater than 1 row(more than one patch)
                eperks = []
                if len(response) > 1:
                    for perk in response[1:]:
                        eperks.append(perk['PerkName'])

                try:
                    # sets main perk to first perk
                    perk = response[0]

                    embed = discord.Embed(color=0xffff00, title=f"{perk['PerkName']}")
                    # TODO: Add perk cost to icon URL
                    # embed.set_author(name=f"{perk['SPECIAL']}", icon_url="")
                    embed.set_thumbnail(url=f"https://cdn.edb.tools/MODUS_Project/images/SPECIAL/{perk['SPECIAL']}.png")

                    # embed.add_field(name="The Perk Card Database", value="For your perk card needs!", inline=False)
                    # embed.add_field(name="Perk card", value=perk["PerkName"], inline=False)
                    embed.add_field(name=":star:", value=perk["Level1"], inline=False)
                    if perk["Level2"]:
                        embed.add_field(name=":star: :star:", value=perk["Level2"], inline=False)
                        if perk["Level3"]:
                            embed.add_field(name=":star: :star: :star:", value=perk["Level3"], inline=False)
                            if perk["Level4"]:
                                embed.add_field(name=":star: :star: :star: :star:", value=perk["Level4"], inline=False)
                                if perk["Level5"]:
                                    embed.add_field(name=":star: :star: :star: :star: :star:", value=perk["Level5"], inline=False)
                    if perk["Note"]:
                        embed.add_field(name="\uFEFF", value=perk["Note"])
                    # checks if extra perk length greater than 0
                    if len(eperks) > 0:
                        embed.add_field(name="\uFEFF", value=f'__**Were you looking for something else?**__\n{", ".join(eperks)}', inline=False)
                    FinalPerk = perk['PerkName'].replace(' ', '').replace('\'', '').replace('!', '')
                    embed.set_image(url=f"https://cdn.edb.tools/MODUS_Project/images/PerkCardsAnimated/{FinalPerk}.gif")
                    # Bot runs the embed
                    await ctx.send(embed=embed)
                # Will report to the player if what they typed doesn't exist within the database
                except TypeError:
                    await ctx.send("Could not find anything by that name. Did you type it correctly?")
                except IndexError:
                    await ctx.send(f"I could not find anything in the database with {arg}")
                # Will throw this error if something else went wrong
                except Exception as e:
                    await ctx.send("Something went wrong here. Please contact support here: https://discord.gg/hMfgSaN")
                    print(e)
                c.close()

    @commands.command(aliases=["nwperk"])
    async def nwperkcard(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send("You need to write the perk you want to look for in the command you wrote as well.")
        else:
            async with ctx.channel.typing():
                if ctx.guild:
                    print(f"A user requested the nuclear winter perk card command in \"{ctx.guild.name}\"")
                else:
                    print(f"A user requested the nuclear winter perk card command in a DM")

                c = MyDB("fallout")
                c.execute("SELECT * FROM en_PerkCardsNW WHERE PerkName LIKE %s", ('%{}%'.format(arg),))
                response = c.fetchall()
                if not response and ctx.invoked_with != RussianAlias:
                    if len(arg) < 15:
                        print(f"Checking spell checker with the following word: {arg}")
                        entryNR = 0
                        for entry in spellNW.candidates(arg):
                            entryNR = entryNR + 1
                            c.execute("SELECT * FROM en_PerkCardsNW WHERE PerkName LIKE %s", ('%{}%'.format(entry),))
                            response = c.fetchall()
                            if response or entryNR == 3:
                                break

                # sets extra perks if response length greater than 1 row(more than one patch)
                eperks = []
                if len(response) > 1:
                    for perk in response[1:]:
                        eperks.append(perk['PerkName'])

                try:
                    # sets main perk to first perk
                    perk = response[0]
                    embed = discord.Embed(color=0xffff00, title=perk["PerkName"], description=perk["Description"])

                    embed.set_thumbnail(url=f"https://cdn.edb.tools/MODUS_Project/images/SPECIAL/{perk['SPECIAL']}.png")
                    # embed.set_author(name="{}".format(perk["SPECIAL"]), icon_url="")
                    # embed.add_field(name="Perk card effect", value=perk["Description"], inline=False)

                    # checks if extra perk length greater than 0
                    if len(eperks)>0:
                        embed.add_field(name="\uFEFF",
                                        value=f'__**Were you looking for something else?**__\n{", ".join(eperks)}',
                                        inline=False)
                    FinalPerk = perk['PerkName'].replace(' ', '').replace('\'', '')
                    embed.set_image(url=f"https://cdn.edb.tools/MODUS_Project/images/PerkCardsAnimated/{FinalPerk}.gif")

                    # Bot runs the embed
                    await ctx.send(embed=embed)
                # Will report to the player if what they typed doesn't exist within the database
                except TypeError as e:
                    await ctx.send("Could not find anything by that name. Did you type it correctly?")
                except IndexError:
                    await ctx.send(f"I could not find anything in the database with {arg}")
                # Will throw this error if something else went wrong
                except Exception as e:
                    await ctx.send("Something went wrong here. Please contact support here: https://discord.gg/hMfgSaN")
                    print(e)
                c.close()


def setup(client):
    client.add_cog(User_F76_PerkCards(client))
