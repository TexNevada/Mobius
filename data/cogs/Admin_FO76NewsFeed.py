# import discord library
import discord
# Imports commands
from discord.ext import commands
# Import permissions & error checks
from discord.ext.commands import has_permissions, MissingPermissions
import sys
sys.path.append(".")
from data.functions.MySQL_Connector import MyDB

# TODO: Add proper error handling


class FO76NewsFeed(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command()
    @has_permissions(manage_channels=True)
    async def ToggleFo76News(self, ctx):
        print(f"A admin toggled the  in {ctx.guild.name}")

        Forbidden_error = "I need the manage webhooks permission to do that"
        Exception_error = "Something went wrong here. Please contact support here: https://discord.gg/hMfgSaN"

        try:
            # Connection to the database
            c = MyDB("essential")
            c.charset(charset="utf8mb4", collation="utf8mb4_unicode_ci")

            # Look for the channel ID in database
            c.execute("SELECT * FROM Fallout76NewsWebhooks WHERE ChannelID = %s", (ctx.channel.id,))

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
                    c.execute("DELETE FROM Fallout76NewsWebhooks WHERE ChannelID = %s", (ctx.channel.id,))
                    c.commit()
                    await ctx.send("This channel will no longer receive Fallout 76 News from Bethesda.net")

                except discord.errors.Forbidden:
                    await ctx.send(Forbidden_error)
                except Exception as e:
                    await ctx.send(Exception_error)
                    # TODO: Add proper error return
                    print(f"WARN Deletion: {e}")

            # Will Trigger if there is no db response
            else:
                try:
                    webhook = await ctx.channel.create_webhook(
                        name="MODUS - Fallout 76 News",
                        reason=f"Fallout 76 News Feed webhook created by {ctx.author.name}")
                    # avatar="https://i.imgur.com/vNJFngn.png",

                    c.execute("INSERT INTO Fallout76NewsWebhooks "
                              "(GuildID, GuildName, ChannelID, ChannelName, WebhookID, WebHookURL, LanguageCheck) "
                              "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                              (ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, webhook.id, webhook.url, "en"))
                    c.commit()
                    await ctx.send(f"Fallout 76 news will now be displayed in {ctx.channel.name}")
                except discord.errors.Forbidden:
                    await ctx.send(Forbidden_error)
                except Exception as e:
                    await ctx.send(Exception_error)
                    # TODO: Add proper error return
                    print(f"WARN Creation: {e}")
            c.close()
        except Exception as e:
            # TODO: Add proper error return
            print(f"WARN: {e}")
            await ctx.send("Something really bad must have happened here. Can you report this to support immediately? "
                           "Ping at support in our discord server https://discord.gg/hMfgSaN. "
                           "Provide any details you can")


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(FO76NewsFeed(client))
