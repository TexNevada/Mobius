"""
Extension name: Poll_command
Author: Yonatan
Created: 11.10.20 - Europe
"""
# import discord library
from datetime import datetime

# noinspection PyPackageRequirements
import discord
# Imports commands
# noinspection PyPackageRequirements
from discord.ext import commands
from discord import app_commands
# Importing our own MySQL prebuilt connection
#import sys
import configparser
from typing import Literal

#sys.path.append(".")
#from ourPackages.myDB import MyDB

# Lists for use
emoji_names = [":regional_indicator_a:", ":regional_indicator_b:", ":regional_indicator_c:", ":regional_indicator_d:",
               ":regional_indicator_e:", ":regional_indicator_f:", ":regional_indicator_g:", ":regional_indicator_h:",
               ":regional_indicator_i:", ":regional_indicator_j:", ":regional_indicator_k:", ":regional_indicator_l:",
               ":regional_indicator_m:", ":regional_indicator_n:", ":regional_indicator_o:", ":regional_indicator_p:",
               ":regional_indicator_q:", ":regional_indicator_r:", ":regional_indicator_s:", ":regional_indicator_t:",]
emoji_list = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵",
              "🇶", "🇷", "🇸", "🇹"]


class poll_command(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client
        super().__init__()

    # Handle reactions with an event
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Check if a poll
        # First filter by poll emoji then get the message and check
        if str(payload.emoji) in emoji_list and payload.user_id != self.client.user.id:
            message = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
            member = message.guild.get_member(payload.user_id)

            if message.embeds and message.author.id == self.client.user.id:
                embed_footer = message.embeds[0].footer.text
                if embed_footer.startswith("MODUS - Poll"):

                    # Check for the advanced modes and perform actions as needed
                    if "Single Vote" in embed_footer:
                        # Single Vote Mode - only 1 vote per user
                        # Check if user already voted
                        already_voted = False
                        for reaction in message.reactions:
                            users = [user async for user in reaction.users()]
                            users_id = [user.id for user in users]
                            if payload.user_id in users_id and str(reaction.emoji) != str(payload.emoji):
                                # await message.remove_reaction(reaction.emoji, member)
                                already_voted = True
                        # if voted remove the new vote and send a message
                        if already_voted:
                            await message.remove_reaction(payload.emoji, member)
                            try:
                                await member.send("You can only vote once on this poll!")
                            except discord.errors.Forbidden as e:
                                pass # TODO: Add to logging

                    # if " Locked - " in embed_footer:
                    #     # Locked vote mode - Only users with a specific role may vote
                    #     # Finding the role id in the footer
                    #     locked_role_id = embed_footer[embed_footer.find("Locked - ") + len("Locked - "):]
                    #
                    #     # Check if user has the role
                    #     has_role = False
                    #     for role in member.roles:
                    #         if str(role.id) == locked_role_id:
                    #             has_role = True
                    #
                    #     # if user doesn't have the role remove the vote
                    #     if not has_role:
                    #         await message.remove_reaction(payload.emoji, member)
                    #         await member.send("This vote is locked for a specific role!")

    @app_commands.command(description="Host your own poll for up to 20 answers!")
    @app_commands.describe(vote_type="This defines if people can vote multiple times or only once!")
    async def poll(self, interaction: discord.Interaction,
                   vote_type: Literal["Single Vote", "Multiple Vote"],
                   question: str,
                   answer_1: str,
                   answer_2: str,
                   answer_3: str = None,
                   answer_4: str = None,
                   answer_5: str = None,
                   answer_6: str = None,
                   answer_7: str = None,
                   answer_8: str = None,
                   answer_9: str = None,
                   answer_10: str = None,
                   answer_11: str = None,
                   answer_12: str = None,
                   answer_13: str = None,
                   answer_14: str = None,
                   answer_15: str = None,
                   answer_16: str = None,
                   answer_17: str = None,
                   answer_18: str = None,
                   answer_19: str = None,
                   answer_20: str = None):

        answers_list = [answer_1,
                        answer_2,
                        answer_3,
                        answer_4,
                        answer_5,
                        answer_6,
                        answer_7,
                        answer_8,
                        answer_9,
                        answer_10,
                        answer_11,
                        answer_12,
                        answer_13,
                        answer_14,
                        answer_15,
                        answer_16,
                        answer_17,
                        answer_18,
                        answer_19,
                        answer_20]
        vote_options = ""
        vote_options_list = []
        emoji_nr = 0
        for answer in answers_list:
            if answer is not None:
                vote_options += f"{emoji_list[emoji_nr]} {answer}\n"
                vote_options_list.append(answer)
                emoji_nr = emoji_nr+1

        # make and send the embed
        embed = discord.Embed(color=0xf5c542, title=question)
        embed.add_field(name="React to this message to vote", value=vote_options)
        embed.set_footer(text=f"MODUS - Poll | {vote_type}")
        await interaction.response.send_message(embed=embed)

        # Add reactions to the message
        for i in range(len(vote_options_list)):
            message_object = await interaction.original_response()
            # message_object = await interaction.channel.fetch_message(int(message.interaction.id))
            await message_object.add_reaction(emoji_list[i])

    @commands.command(aliases=["poll"])
    async def _poll(self, ctx, *args):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        await ctx.send(config["LEGACY"]["UseSlash"])

        # Checks for advanced options and adds into the start index
        single_mode_vote_prefix = ["-single", "-s", "-sv"]
        start_index = 0
        picked_advanced_option = "| Multiple Vote "
        if args[0].lower() in single_mode_vote_prefix or args[1].lower() in single_mode_vote_prefix:
            start_index += 1
            location = 0
            if args[1].lower() in single_mode_vote_prefix:
                location = 1
            if args[location].lower() in single_mode_vote_prefix:
                picked_advanced_option = "| Single Vote "

        # In case of args 0 or 1 have a role mentioned as a lock option
        if args[0].lower().startswith("-<@&") or args[1].lower().startswith("-<@&"):
            start_index += 1
            location = 0
            if args[1].lower().startswith("-<@&"):
                location = 1
            role_id = args[location][4:-1]
            picked_advanced_option += "| Locked - {role_id} ".format(role_id=role_id)

        if not args:
            await ctx.send("Missing arguments.")
            return
        elif len(args) < 3 + start_index:
            await ctx.send("You need at least one question and two answers")
            return
        elif len(args) > 21 + start_index:
            await ctx.send("That's to many options. You may only have up to 20 answers")
            return

        # Organize the answers into the string
        options_str = ""
        for i in range(len(args) - 1 - start_index):
            options_str += emoji_names[i] + " - " + args[i + 1 + start_index]
            options_str += "\n"

        # make and send the embed
        embed = discord.Embed(color=0xf5c542, title=args[0 + start_index])
        embed.add_field(name="React to this message to vote", value=options_str)
        embed.set_footer(text="MODUS - Poll " + picked_advanced_option)
        message = await ctx.send(embed=embed)

        # Add reactions to the message
        for i in range(len(args) - 1 - start_index):
            await message.add_reaction(emoji_list[i])


async def setup(client: commands.Bot) -> None:
    await client.add_cog(poll_command(client))
