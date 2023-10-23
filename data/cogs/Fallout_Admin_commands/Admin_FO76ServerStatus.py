# import discord library
import discord
# Imports commands
from discord.ext import commands
# Import permissions & error checks
from discord.ext.commands import has_permissions
import sys
sys.path.append(".")
from data.functions.MySQL_Connector import MyDB
from data.functions.logging import get_log
logger = get_log(__name__)

class FO76ServerStatus(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command()
    @has_permissions(manage_channels=True)
    async def ToggleFO76Status(self, ctx, *, arg=None):
        logger.info(f"A admin toggled FO76ServerStatus in {ctx.guild.name}")

        Forbidden_error = "I need the manage webhooks permission to do that"
        Exception_error = "Something went wrong here. Please contact support here: https://discord.gg/hMfgSaN"
        Super_bad_error = "Something really bad must have happened here. Can you report this to support immediately? " \
                          "Ping at support in our discord server https://discord.gg/hMfgSaN. " \
                          "Provide any details you can"

        try:
            # Connection to the database
            c = MyDB("essential")
            c.charset(charset="utf8mb4", collation="utf8mb4_unicode_ci")

            # Look for the channel ID in database
            c.execute("SELECT * FROM Fo76ServerStatusWebhooks WHERE ChannelID = %s", (ctx.channel.id,))

            # Returns results from db
            response = c.fetchone()

            # Will trigger if there is a db response
            if response:
                try:
                    webhooks = await ctx.channel.webhooks()
                    for hook in webhooks:
                        if hook.id == int(response['WebhookID']):
                            await hook.delete()
                            break
                    c.execute("DELETE FROM Fo76ServerStatusWebhooks WHERE ChannelID = %s", (ctx.channel.id,))
                    c.commit()
                    c.close()
                    await ctx.send("This channel will no longer receive updates when Fallout 76 goes online or offline")

                except discord.errors.Forbidden:
                    await ctx.send(Forbidden_error)
                except Exception as e:
                    await ctx.send(Exception_error)
                    # TODO: Add better exception logger.info
                    logger.info(f"WARNING Deletion: {e}")

            # Will Trigger if there is no db response
            else:
                try:
                    webhook = await ctx.channel.create_webhook(
                        name="MODUS - Fallout 76 Status",
                        reason=f"Fallout 76 Server Status feed webhook created by {ctx.author.name}")
                    if arg is None:
                        sql = "INSERT INTO Fo76ServerStatusWebhooks (GuildID, GuildName, ChannelID, ChannelName, " \
                              "WebhookID, WebHookURL, LanguageCheck) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                        val = ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, webhook.id, webhook.url, "en"
                    else:
                        sql = "INSERT INTO Fo76ServerStatusWebhooks (GuildID, GuildName, ChannelID, ChannelName, " \
                              "WebhookID, WebHookURL, LanguageCheck, CustomMessage) VALUES " \
                              "(%s, %s, %s, %s, %s, %s, %s, %s)"
                        val = ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, webhook.id, webhook.url, "en", arg
                    c.execute(sql, val)
                    c.commit()
                    c.close()
                    if arg is None:
                        await ctx.send("This channel will now receive updates when Fallout 76 goes online or offline")
                    else:
                        await ctx.send(f"This channel will now receive updates when Fallout 76 goes online or offline with custom message {arg}")
                except discord.errors.Forbidden:
                    await ctx.send(Forbidden_error)
                except Exception as e:
                    await ctx.send(Exception_error)
                    # TODO: Add better exception logger.info
                    logger.info(f"WARNING Creation: {e}")

        except Exception as e:
            # TODO: Add better exception logger.info
            logger.info(f"WARNING: {e}")
            await ctx.send(Super_bad_error)


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(FO76ServerStatus(client))
