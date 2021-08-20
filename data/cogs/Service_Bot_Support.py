# import discord library
import discord
# Imports commands
from discord.ext import commands
# Import permissions & error checks
from discord.ext.commands.cooldowns import BucketType
from data.functions.owner import is_owner
import configparser


class Service_Bot_Support(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.before_invoke(channel_check)
    @commands.guild_only()
    @commands.cooldown(rate=1, per=7200, type=BucketType.channel)
    @commands.command()
    async def modsupport(self, ctx):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        for key, value in config.items("ADMIN"):
            if eval(config["Credentials"]["Active"]) is True:
                # TODO: Authentication could be logged.
                pass
            if ctx.author.id == int(value):
                break
            else:
                embed = discord.Embed(color=discord.Color.blue(),
                                      title="I have contacted support for you. ✅")

                embed.add_field(name="Be sure to be as descriptive as possible so it is easier for us to help you.\n"
                                     "A few pointers to consider when asking for help.",
                                value="```md\n"
                                      "* Provide us with your guild name & guild id if possible.\n"
                                      "* What is the cause of your issue? Be descriptive.\n"
                                      "* Asking about the name of a command? Check the help command.\n"
                                      "* Have you checked our documentation page?.\n"
                                      "```",
                                inline=False)
                embed.set_footer(text="We are only human so if no one answers. Be patient. "
                                      "We will get back to you with a ping.")
                embed.set_thumbnail(url="https://cdn.edb.tools/MODUS_Project/images/PerkCardsAnimated/ExpertHacker.gif")

                # Bot runs the embed
                await ctx.send("<@&617655022636892160>", embed=embed)
                break

    @modsupport.error
    async def modsupport_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass

    @is_owner()
    @commands.command()
    async def resolved(self, ctx):
        command = self.client.get_command("modsupport")
        await ctx.send(f"Support has been resolved <:HappyModus:697900498313019502>")
        command.reset_cooldown(ctx)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith(">"):
            pass
        else:
            ctx = await self.client.get_context(message)
            if ctx.channel.id == 588400643266445342:
                command = self.client.get_command("modsupport")
                try:
                    await command.invoke(ctx)
                except Exception as e:
                    # print(e)
                    # print(f"Support message ratelimit: {e}")
                    pass


# ends the extension
def setup(client):
    client.add_cog(Service_Bot_Support(client))
