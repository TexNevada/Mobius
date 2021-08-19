import discord
from discord.ext import commands
from spellchecker import SpellChecker
from data.functions.MySQL_Connector import MyDB
import configparser

spell = SpellChecker()
spell.word_frequency.load_text_file("./data/cogs_data/F76_Mutation_Word_List.txt")


# start of the extension as a class.
class User_F76_Mutations(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mutation(self, ctx, *, arg: str):
        if ctx.guild:
            print(f"A user requested the mutation command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the mutation command in a private message")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        c = MyDB("fallout")
        c.execute("SELECT * FROM en_Mutations WHERE Mutation LIKE %s", ('%{}%'.format(arg),))
        async with ctx.channel.typing():
            response = c.fetchone()
            if not response:
                if len(arg) < 15:
                    async with ctx.channel.typing():
                        print(f"Checking spell checker with the following word: {arg}")
                        entryNR = 0
                        for entry in spell.candidates(arg):
                            entryNR = entryNR + 1
                            c.execute("SELECT * FROM en_Mutations WHERE Mutation LIKE %s", ('%{}%'.format(entry),))
                            response = c.fetchone()
                            if response or entryNR == 3:
                                break

            if response:
                try:
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
                    embed.add_field(name=f"__**{response['Mutation']} serum can by doing the following requirements**__",
                                    value=f"**Requirements:** {response['Requirements']}\n"
                                          f"**Materials:** {response['Materials']}",
                                    inline=False)
                    # Bot runs the embed
                    await ctx.send(embed=embed)
                # Will report to the player if what they typed doesn't exist within the database
                except TypeError as e:
                    await ctx.send("Could not find anything by that name. Did you type it correctly?")
                    print(e)
                # Will throw this error if something else went wrong
                except Exception as e:
                    await ctx.send("Something went very wrong here. Contact support here https://discord.gg/hMfgSaN!")
                    print(e)
            else:
                await ctx.send("Could not find anything by that name. Did you type it correctly?")

    @commands.command()
    async def mutations(self, ctx):
        if ctx.guild:
            print(f"A user requested the mutations command in \"{ctx.guild.name}\"")
        else:
            print(f"A user requested the mutations command in a private message")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        c = MyDB("fallout")
        c.execute("SELECT * FROM en_Mutations")
        embed = discord.Embed(color=0x28df28, title=f"All of Fallout 76 mutations!")
        embed.set_thumbnail(url=config["EDB.TOOLS"]["F76_Mutations"])
        async with ctx.channel.typing():
            try:
                response = c.fetchall()
                for mutation in response:
                    embed.add_field(name=mutation['Mutation'],
                                    value=f"**Positive:** {mutation['PositiveEffects']}\n"
                                          f"**Negative:** {mutation['NegativeEffects']}",
                                    inline=False)
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send(e)


# ends the extension
def setup(client):
    client.add_cog(User_F76_Mutations(client))
