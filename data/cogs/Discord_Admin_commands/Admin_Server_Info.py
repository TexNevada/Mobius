import discord
import math
import datetime
import time
from discord.ext import commands
from data.functions.logging import get_log

logger = get_log(__name__)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


class Admin_Server_Info(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        logger.info(f"The serverinfo command was requested in {ctx.guild.name}")
        try:
            embed = discord.Embed(title=f"Server information for {ctx.guild.name}", color=discord.Color.red())
            embed.set_thumbnail(url=ctx.guild.icon.url)
            # embed.set_author(name=f"")
            embed.add_field(name="Server owner", value=f"{ctx.guild.owner.global_name}\n", inline=True)
            # embed.add_field(name="Region", value=ctx.guild.region, inline=True)
            embed.add_field(name="Server ID", value=f"`{ctx.guild.id}`", inline=True)
            # embed.add_field(name="\uFEFF", value="\uFEFF", inline=True)


            embed.add_field(name="Bot info", value=f"Shard ID: `{ctx.guild.shard_id}`", inline=True)


            # embed.add_field(name="Upload limit", value=f"`{convert_size(ctx.guild.filesize_limit)}`", inline=True)
            embed.add_field(name="Server Limits", value=f"Emoji: `{ctx.guild.emoji_limit}`\n"
                                                        f"Sticker: `{ctx.guild.sticker_limit}`\n"
                                                        f"Upload: `{convert_size(ctx.guild.filesize_limit)}`")
            # embed.add_field(name="Emoji limit", value=f"`{ctx.guild.emoji_limit}`", inline=True)
            # embed.add_field(name="Sticker limit", value=f"`{ctx.guild.sticker_limit}`", inline=True)



            channels = len(ctx.guild.channels) - len(ctx.guild.categories)
            total = channels + len(ctx.guild.threads)
            embed.add_field(name="Channels",
                            value=f"Text channels: `{len(ctx.guild.text_channels)}`\n"
                                  f"Voice channels: `{len(ctx.guild.voice_channels)}`\n"
                                  f"Threads: `{len(ctx.guild.threads)}`\n"
                                  f"Total: `{total}`",
                            inline=True)
            members = set(ctx.guild.members)
            bots = filter(lambda m: m.bot, members)
            bots = set(bots)
            users = members - bots
            embed.add_field(name="Members",
                            value=f"Users: `{len(users)}`\n"
                                  f"Bots: `{len(bots)}`\n"
                                  f"Total: `{ctx.guild.member_count}/{ctx.guild.max_members}`",
                            inline=True)

            #embed.add_field(name="\uFEFF", value="\uFEFF", inline=True)

            embed.add_field(name="Server boost status",
                            value=f"Boost Tier: `{ctx.guild.premium_tier}`\n"
                                  f"Subscriber count: `{ctx.guild.premium_subscription_count}`", inline=True)

            features = '\n'.join(item.capitalize() for item in ctx.guild.features)
            embed.add_field(name="Server features", value=features, inline=True)

            # try:
            #     bans = 0
            #     for x in await ctx.guild.bans():
            #         bans += 1
            #     embed.add_field(name="Bans", value=f"`{bans}`", inline=True)
            # except:
            #     embed.add_field(name="Bans", value="Missing ban perm", inline=True)

            try:
                estimate = await ctx.guild.estimate_pruned_members(days=1)
                estimate2 = await ctx.guild.estimate_pruned_members(days=7)
                estimate3 = await ctx.guild.estimate_pruned_members(days=30)
                embed.add_field(name="Prune estimate",
                                value=f"1 day: `{estimate}`\n"
                                      f"7 days: `{estimate2}`\n"
                                      f"30 days: `{estimate3}`\n",
                                inline=True)
            except:
                embed.add_field(name="Prune estimate", value="Missing kick perm", inline=True)

            year = ctx.guild.created_at.year
            month = ctx.guild.created_at.month
            day = ctx.guild.created_at.day
            hour = ctx.guild.created_at.hour
            minute = ctx.guild.created_at.minute
            second = ctx.guild.created_at.second

            unix_time_created_at = time.mktime(datetime.datetime(year, month, day, hour, minute, second).timetuple())

            year = ctx.guild.me.joined_at.year
            month = ctx.guild.me.joined_at.month
            day = ctx.guild.me.joined_at.day
            hour = ctx.guild.me.joined_at.hour
            minute = ctx.guild.me.joined_at.minute
            second = ctx.guild.me.joined_at.second

            unix_time = time.mktime(datetime.datetime(year, month, day, hour, minute, second).timetuple())

            # embed.add_field(name="\uFEFF", value="\uFEFF", inline=True)

            embed.add_field(name="Server created at", value=f"<t:{int(unix_time_created_at)}:f>\n", inline=True)
            embed.add_field(name="Bot joined date", value=f"<t:{int(unix_time)}:f>", inline=True)

            if ctx.guild.mfa_level.value == 0:
                embed.add_field(name="2 Factor Authentication Security",
                                value="**2FA Setting: `OFF`**\n"
                                      "We highly recommend turning on 2FA on the server for good security. "
                                      "This prevents hackers with access to compromised admin accounts "
                                      "from changing any server settings without a 2FA code.",
                                inline=False)
            elif ctx.guild.mfa_level.value == 1:
                embed.add_field(name="2 Factor Authentication Security",
                                value="**2FA Setting: `ON`**\n"
                                      "You are protected against compromised admin accounts!\n"
                                      "__This does not protect against compromised bot accounts.__",
                                inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            logger.info(e)
            await ctx.send("That's odd. I can't seem to give you that information. "
                           "You better report this in to support.")

    # @commands.command()
    # @commands.has_permissions(manage_channels=True)
    # @commands.guild_only()
    # async def auditlogs(self, ctx):
    #     return None

    # @commands.command()
    # @commands.has_permissions(manage_channels=True)
    # @commands.guild_only()
    # async def modactions(self, ctx, member: discord.Member = None):
    #     logger.info(f"The modactions command was requested in {ctx.guild.name}")
    #     try:
    #         if member is None:
    #             member = ctx.author
    #         entries = await ctx.guild.audit_logs(limit=None, user=member).flatten()
    #         await ctx.send(f'This user has made {len(entries)} moderation actions.')
    #     except:
    #         await ctx.send("I don't have access to view the audit logs. "
    #                        "Access can be gained by enabling Administrator or "
    #                        "View Audit Logs setting in the MODUS role")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Admin_Server_Info(client))
