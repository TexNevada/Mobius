# import discord library
import discord
# Imports commands
from discord.ext import commands
# Import permissions & error checks
from discord.ext.commands import has_permissions
import mysql.connector
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")


class bethesdatracker(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command(name='togglebethesdatracker', aliases=["toggletracker", "bethesdatracker"])
    @has_permissions(manage_channels=True)
    async def togglebethesdatracker(self, ctx):
        print(f"A admin toggled the dev tracker in {ctx.guild.name}")
        try:
            # Connection to third party database
            conn = mysql.connector.connect(host=config["NukaCrypt"]["Host"],
                                           user=config["NukaCrypt"]["user"],
                                           passwd=config["NukaCrypt"]["passwd"],
                                           database=config["NukaCrypt"]["database"])
            c = conn.cursor(dictionary=True)
            c.execute("SELECT * FROM devWebhooks WHERE ChannelID = %s", (ctx.channel.id,))
            # should return false or None if blank, might want to double check.
            response = c.fetchall()
            # Dev Tracking Enabled, so we disable it
            if response:
                try:
                    webhooks = await ctx.channel.webhooks()
                    for hook in webhooks:
                        if hook.id == int(response[0]['WebhookID']):
                            await hook.delete()
                            break
                    c.execute("DELETE FROM devWebhooks WHERE ChannelID = %s", (ctx.channel.id,))
                    conn.commit()
                    await ctx.send("Dev Tracking is now disabled for this channel!")
                except discord.errors.Forbidden:
                    await ctx.send("The bot needs the manage webhooks permission")
                except Exception as e:
                    await ctx.send("Something went wrong here. Contact support")
                    print(e)
            # dev tracking not enabled, enable it
            else:
                try:
                    webhook = await ctx.channel.create_webhook(name='Dev Tracker Webhook')
                    c.execute("INSERT INTO devWebhooks (GuildID,GuildName,ChannelID,ChannelName,WebhookID,WebHookURL) "
                              "VALUES (%s,%s,%s,%s,%s,%s)",
                              (ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, webhook.id, webhook.url))
                    conn.commit()
                    await ctx.send(f"Dev comments will now be output in {ctx.channel.name}!")
                except discord.errors.Forbidden:
                    await ctx.send("The bot needs the manage webhooks permission")
                except Exception as e:
                    await ctx.send("What a mad lad, you passed the forbidden error. Contact support.")
                    print('Error creating webhook {}'.format(e))
            conn.close()
        except Exception as e:
            print(e)
            await ctx.send("There seems to be an issue with our connection to our partner database from NukaCrypt. "
                           "Please try again later. If this issue persist. Please report the issue to us "
                           "https://discord.gg/hMfgSaN")


# ends the extension
async def setup(client: commands.Bot) -> None:
    await client.add_cog(bethesdatracker(client))
