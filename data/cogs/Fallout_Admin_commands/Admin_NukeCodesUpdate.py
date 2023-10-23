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


class nukeUpdatesCommand(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(aliases=["ToggleCodesUpdate", "ToggleCodeUpdates", "ToggleCodesUpdates", "tcu"])
    @commands.guild_only()
    @has_permissions(manage_channels=True)
    async def ToggleCodeUpdate(self, ctx, *, arg=None):
        logger.info(f"A admin toggled code updates in {ctx.guild.name}")

        Forbidden_error = "I need the manage webhooks permission to do that"
        Exception_error = "Something went wrong here. Please contact support here: https://discord.gg/hMfgSaN"

        try:
            # Connection to the database
            c = MyDB("essential")
            c.charset(charset="utf8mb4", collation="utf8mb4_unicode_ci")

            # Look for results in the database
            c.execute("SELECT * FROM NukaCryptNukeCodesWebhooks WHERE ChannelID = %s", (ctx.channel.id,))
            response = c.fetchone()

            if response:
                try:
                    webhooks = await ctx.channel.webhooks()
                    for hook in webhooks:
                        if hook.id == int(response['WebhookID']):
                            await hook.delete()
                            break
                    c.execute("DELETE FROM NukaCryptNukeCodesWebhooks WHERE ChannelID = %s", (ctx.channel.id,))
                    c.commit()
                    c.close()
                    # translation strings needs to go from "something" to _("something") for it to work
                    await ctx.send("This channel will no longer receive updates when nuclear codes reset")

                except discord.errors.Forbidden as e:
                    await ctx.send(Forbidden_error)
                    # We should logger.info all errors :)
                    logger.info(f"WARNING: Discord Forbidden: {e}")
                except Exception as e:
                    await ctx.send(Exception_error)
                    # TODO: Add better exception logger.info
                    # I will work on a logging module soon.
                    logger.info(f"WARNING Deletion: {e}")

            # Will Trigger if there is no db response
            else:
                try:
                    webhook = await ctx.channel.create_webhook(
                        name="MODUS - Fallout 76 NukeCodes",
                        reason=f"Fallout 76 NukeCodes webhook created by {ctx.author.name}")
                    #   F strings sadly don't work well with gettext module. Use .format() instead
                    if arg is None:
                        sql = "INSERT INTO NukaCryptNukeCodesWebhooks (GuildID, GuildName, ChannelID, ChannelName, " \
                              "WebhookID, WebHookURL) VALUES (%s, %s, %s, %s, %s, %s)"
                        val = ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, webhook.id, webhook.url
                    else:
                        sql = "INSERT INTO NukaCryptNukeCodesWebhooks (GuildID, GuildName, ChannelID, ChannelName, " \
                              "WebhookID, WebHookURL, CustomMessage) VALUES " \
                              "(%s, %s, %s, %s, %s, %s, %s)"
                        val = ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, webhook.id, webhook.url, arg
                    c.execute(sql, val)
                    c.commit()
                    c.close()
                    if arg is None:
                        await ctx.send("This channel will now receive updates when nuclear codes reset")
                    else:
                        await ctx.send(f"This channel will now receive updates when nuclear "
                                       f"codes reset with the custom message {arg}")
                except discord.errors.Forbidden:
                    await ctx.send(Forbidden_error)
                except Exception as e:
                    await ctx.send(Exception_error)
                    # TODO: Add better exception logger.info
                    logger.info(f"WARNING Creation: {e}")

        except Exception as e:
            # TODO: Add proper error return
            logger.info(f"WARNING: {e}")
            await ctx.send("Something really bad must have happened here. Can you report this to support immediately? "
                           "Ping at support in our discord server https://discord.gg/hMfgSaN. "
                           "Provide any details you can")


# ends the extension
async def setup(client: commands.Bot):
    await client.add_cog(nukeUpdatesCommand(client))
