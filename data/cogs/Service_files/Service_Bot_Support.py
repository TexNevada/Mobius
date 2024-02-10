# import discord library
import discord
import configparser
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from data.functions.owner import is_owner
from data.functions.logging import get_log
logger = get_log(__name__)


class Service_Bot_Support(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.guild_only()
    @commands.cooldown(rate=1, per=7200, type=BucketType.channel)
    @commands.command()
    async def modsupport(self, ctx):
        config = configparser.ConfigParser()
        config.read("./config.ini", encoding="utf-8")
        for key, value in config.items("ADMIN"):
            if ctx.author.id == int(value):
                break
            else:
                embed = discord.Embed(color=discord.Color.blue(),
                                      title=config["Support"]["Support_embed_title"])

                embed.add_field(name=config["Support"]["Support_embed_field_name"],
                                value=config["Support"]["Support_embed_field_value"],
                                inline=False)
                embed.set_footer(text=config["Support"]["Support_embed_footer"])
                embed.set_thumbnail(url=config["Support"]["Support_embed_image_thumbnail"])

                # Bot runs the embed
                await ctx.send(f'<@&{config["Support"]["Support_Role_ID"]}>', embed=embed)
                break

    @modsupport.error
    async def modsupport_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            pass

    @is_owner()
    @commands.command()
    async def resolved(self, ctx):
        logger.info("Resolved command issued for support function")
        config = configparser.ConfigParser()
        config.read("./config.ini")
        if ctx.channel.id == int(config["Support"]["Support_Channel_ID"]):
            command = self.client.get_command("modsupport")
            await ctx.send(config["Support"]["Support_resolved_message"])
            command.reset_cooldown(ctx)
        else:
            logger.info("Resolved command issues in the wrong channel.")
            await ctx.send("This command only works in the same channel as the support channel you have configured!")

    @commands.Cog.listener()
    async def on_message(self, message):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        if message.content.startswith(">"):
            pass
        else:
            ctx = await self.client.get_context(message)
            if config["Support"]["Support_Channel_ID"] != "" or config["Support"]["Support_Channel_ID"] is not None:
                if ctx.channel.id == int(config["Support"]["Support_Channel_ID"]):
                    command = self.client.get_command("modsupport")
                    try:
                        await command.invoke(ctx)
                    except discord.ext.commands.errors.CommandOnCooldown:
                        pass
                    except Exception as e:
                        logger.error(f"Support command failed. Reason: {e}")


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(Service_Bot_Support(client))
