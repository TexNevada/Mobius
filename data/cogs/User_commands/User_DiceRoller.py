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

from data.functions.logging import get_log
logger = get_log(__name__)

class DiceRoller(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    @app_commands.command(name="roll", description="Roll 1 up to 100 dice with support up to 10,000 sides!")
    @app_commands.describe(dice="Allows you to input how many dice you wish to roll!",
                           sides="Allows you to input how many sides on the dice you wish to have",
                           multiplier="Will add whatever number you type in to the total amount")
    async def _roll(self, interaction: discord.Interaction, dice: int, sides: int, multiplier: int = None):
        logger.info(f"A user requested the roll command")
        # logger.info(self.qualified_name)
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
        logger.info(f"A user requested a legacy command")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])


async def setup(client: commands.Bot) -> None:
    await client.add_cog(DiceRoller(client))
