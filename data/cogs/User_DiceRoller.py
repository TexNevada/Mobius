"""
Extension name: Dice roller
Author: Tex Nevada
Created: 18.04.19 - Europe
Updated: 31.07.20 - Europe
"""
# Imports commands
from discord.ext import commands
# Allows for random numbers to be generated.
import random


class DiceRoller(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["gmroll"])
    async def roll(self, ctx, arg1: str, *, arg2=None):
        if ctx.guild:
            print(f"A user requested the roll command in {ctx.guild.name}")
        else:
            print(f"A user requested the roll command in a private message")
        #
        # Prepping Error messages in advance
        Error = "Did you type it wrong? Example: `>roll 1d10` or `>roll 1d10 +10`"
        # Just Ignore this
        #
        # Will try to find the key letter inside the language json. If it doesn't it results in -1 as an answer
        if arg1.find("d") > -1:
            # will split arg1 into 2 arguments if key letter exists
            spl = arg1.split("d")
            # First is the number of dice rolled
            first = int(spl[0])
            # Second is the number of sides the dice has.
            # +1 is for the random range to work properly between
            second = int(spl[1])+1
            # Counter for multiplier used by players
            multiplier = 0
            if arg2 is not None:
                if arg2.find("+") > -1:
                    third = arg2.split("+")
                    multiplier = int(third[1])
            try:
                if first <= 100:
                    if first > 0:
                        if second <= 10000:
                            if second > 2:
                                result = []
                                for x in range(0, int(first)):
                                    rand = random.randrange(1, int(second))
                                    result.append(rand)
                                random_result = str(result)[1:-1]
                                total_number = 0
                                for num in result:
                                    total_number = num + total_number
                                total = 'Total:'
                                rolled = 'Rolled:'
                                if multiplier != 0:
                                    total_number = total_number + multiplier
                                    FinalAnswer = f"{rolled} {random_result}, +{multiplier}\n" \
                                                  f"{total} {total_number}"
                                else:
                                    FinalAnswer = f"{rolled} {random_result}\n" \
                                                  f"{total} {total_number}"
                                if ctx.invoked_with.lower() == "gmroll":
                                    await ctx.send("The Game Master has rolled their dice!")
                                    await ctx.author.send(FinalAnswer)
                                else:
                                    await ctx.send(FinalAnswer)
                            else:
                                await ctx.send("You can't roll dice with sides that's below 2")
                        else:
                            await ctx.send("You can only do below 10000 for the number of sides for the dice!")
                    else:
                        await ctx.send("You can't roll dice that's below 1")
                else:
                    await ctx.send("You can only do below 100 dice!")
            except Exception as e:
                print(e)
                await ctx.send(Error)
        else:
            await ctx.send(Error)


def setup(client):
    client.add_cog(DiceRoller(client))
