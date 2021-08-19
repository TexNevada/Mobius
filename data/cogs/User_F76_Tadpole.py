"""
Made by: Yonatan
"""

# import discord library
import discord
# Imports commands
from discord.ext import commands
from data.functions.MySQL_Connector import MyDB


class User_F76_Tadpole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["ta"])
    async def tadpole(self, ctx, category_arg=None, search_arg=None):

        # You could see if the arg is equal to the list below though you want
        # people just to be able to search instantly for a question

        # Tadpole types
        tadpole_types = ["Athlete", "Archer", "Cook", "Codebreaker", "Herpetologist",
                         "Entomologist", "Mammalogist", "Hunter", "Swimmer", "Medic"]

        ### Help command is seperate and is not needed if that is what you meant :)

        # Sends list of categories if the argument don't match
        # TODO: Add the spell error here
        if not category_arg or category_arg.title() not in tadpole_types:
            # Get a string of all types joined by a new line
            tadpole_types_str = "\n".join(tadpole_types)

            # Create the Help Embed
            ta_embed = discord.Embed(color=discord.Color(0xD3E2B7))
            ta_embed.set_thumbnail(url="https://cdn.edb.tools/MODUS_Project/images/TadPole/GPEis4m.png")
            ta_embed.add_field(name="Tadpole Exam Types:", value=tadpole_types_str)
            await ctx.send(embed=ta_embed)
            return

        # Get the data from the database
        c = MyDB("fallout")
        if not search_arg:
            await ctx.send("You seem to be missing an argument!")
            return

        c.execute("SELECT * FROM en_TadpoleExam WHERE Category LIKE %s and Question LIKE %s",
                  ('%{}%'.format(category_arg), '%{}%'.format(search_arg)))
        response = c.fetchall()
        c.close()
        questions = [response[i]['Question'] for i in range(len(response))]
        answers = [response[i]['Answer'] for i in range(len(response))]

        # Create the Answers Embed
        # If no fetched answer / question
        if len(answers) == 0:
            await ctx.send("No Question matching your argument was found")
            return

        ta_embed = discord.Embed(title="🥇Tadpole {category} Exam Answers!".format(category=category_arg.title()),
                                 description="**Q:** {Question}\n**A:** {Answer}".format(Question=questions[0],
                                                                                 Answer=answers[0]),
                                 color=discord.Color(0xE84040))
        ta_embed.set_thumbnail(url="https://cdn.edb.tools/MODUS_Project/images/TadPole/GPEis4m.png")
        if len(answers) > 1:
            ta_embed.add_field(name="Found {} more results".format(len(answers) - 1),
                               value="Where you looking for something else? Be more specific")

        await ctx.send(embed=ta_embed)


# ends the extension
def setup(client):
    client.add_cog(User_F76_Tadpole(client))
