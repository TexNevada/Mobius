"""
Extension name: Dice roller
Author: Tex Nevada
Created: 18.04.19 - Europe
Updated: 31.07.20 - Europe
"""
import discord
# Imports commands
from discord.ext import commands
from discord import app_commands
# Allows for random numbers to be generated.
import random
import configparser


class DiceRoller(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="roll", description="Roll 1 up to 100 dice with support up to 10,000 sides!")
    @app_commands.describe(dice="Allows you to input how many dice you wish to roll!",
                           sides="Allows you to input how many sides on the dice you wish to have",
                           multiplier="Will add whatever number you type in to the total amount")
    async def _roll(self, interaction: discord.Interaction, dice: int, sides: int, multiplier: int = None):
        print(f"A user requested the roll command")
        # print(self.qualified_name)
        # Prepping Error messages in advance
        number_of_dice = dice
        number_of_sides = sides
        if number_of_dice < 100:
            if number_of_dice > 0:
                if number_of_sides < 10000:
                    if number_of_sides > 1:
                        result = []
                        for x in range(0, int(number_of_dice)):
                            rand = random.randrange(1, int(number_of_sides))
                            result.append(rand)
                        random_result = str(result)[1:-1]
                        total_number = 0
                        for num in result:
                            total_number = num + total_number
                        total = 'Total:'
                        rolled = 'Rolled:'
                        if multiplier is not None:
                            total_number = total_number + multiplier
                            FinalAnswer = f"{rolled} {random_result}, +{multiplier}\n" \
                                          f"{total} {total_number}"
                        else:
                            FinalAnswer = f"{rolled} {random_result}\n" \
                                          f"{total} {total_number}"
                        await interaction.response.send_message(FinalAnswer)
                    else:
                        await interaction.response.send_message("You can't roll a dice with less then 2 sides", ephemeral=True)
                else:
                    await interaction.response.send_message("You can only roll dice with 10 000 sides or lower", ephemeral=True)
            else:
                await interaction.response.send_message("You can't roll 0 dice or negative dice!", ephemeral=True)
        else:
            await interaction.response.send_message("You can only roll 100 dice or lower!", ephemeral=True)

    @commands.command(aliases=["gmroll"])
    async def roll(self, ctx, arg1: str, *, arg2=None):
        if ctx.guild:
            print(f"A user requested the roll command in {ctx.guild.name}")
        else:
            print(f"A user requested the roll command in a private message")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])
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


async def setup(client: commands.Bot) -> None:
    await client.add_cog(DiceRoller(client))
