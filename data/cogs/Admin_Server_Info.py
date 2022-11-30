# import discord py library
import discord
# Imports commands
from discord.ext import commands
import math
import datetime


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
        print(f"The serverinfo command was requested in {ctx.guild.name}")
        try:
            embed = discord.Embed(title=f"Server information for {ctx.guild.name}", color=discord.Color.red())
            embed.set_thumbnail(url=ctx.guild.icon_url)
            # embed.set_author(name=f"")
            embed.add_field(name="Server owner", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Region", value=ctx.guild.region, inline=True)
            embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            channels = len(ctx.guild.channels) - len(ctx.guild.categories)
            embed.add_field(name="Channels",
                            value=f"Text channels: `{len(ctx.guild.text_channels)}`\n"
                                  f"Voice channels: `{len(ctx.guild.voice_channels)}`\n"
                                  f"Total: `{channels}`",
                            inline=True)
            members = set(ctx.guild.members)
            bots = filter(lambda m: m.bot, members)
            bots = set(bots)
            users = members - bots
            embed.add_field(name="Members",
                            value=f"Users: `{len(users)}`\n"
                                  f"Bots: `{len(bots)}`\n"
                                  f"Total: `{ctx.guild.member_count}`",
                            inline=True)

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
            embed.add_field(name="Emoji limit", value=f"`{ctx.guild.emoji_limit}`", inline=True)
            uploadlimit = convert_size(ctx.guild.filesize_limit)
            embed.add_field(name="Upload limit", value=f"`{uploadlimit}`", inline=True)
            try:
                bans = 0
                for x in await ctx.guild.bans():
                    bans += 1
                embed.add_field(name="Bans", value=f"`{bans}`", inline=True)
            except:
                embed.add_field(name="Bans", value="Missing ban perm", inline=True)
            if ctx.guild.premium_tier != 0:
                embed.add_field(name="Server's Nitro Tier", value=f"`{ctx.guild.premium_tier}`", inline=True)
            if ctx.guild.premium_subscription_count != 0:
                embed.add_field(name="Total server boosts", value=f"`{ctx.guild.premium_subscription_count}`",
                                inline=True)
                embed.add_field(name="\uFEFF", value="\uFEFF", inline=True)
            if ctx.guild.features is False:
                embed.add_field(name="Server features", value=ctx.guild.features, inline=True)

            x = datetime.datetime.strptime(str(ctx.guild.created_at), "%Y-%m-%d %H:%M:%S.%f")
            x = x.strftime("%d %B %Y\n%H:%M:%S UTC")
            embed.add_field(name="Server created at", value=f"{x}", inline=True)

            x = datetime.datetime.strptime(str(ctx.guild.me.joined_at), "%Y-%m-%d %H:%M:%S.%f")
            x = x.strftime("%d %B %Y\n%H:%M:%S UTC")
            embed.add_field(name="Bot joined date", value=f"{x}", inline=True)

            if ctx.guild.mfa_level == 0:
                embed.add_field(name="2 Factor Authentication Security",
                                value="**2FA Setting: OFF!!**\n"
                                      "We highly recommend turning on 2FA on the server for good security\n"
                                      "This prevents any hackers who might have access to any compromised admin account"
                                      " from being able to administer the server.",
                                inline=False)
            elif ctx.guild.mfa_level == 1:
                embed.add_field(name="2 Factor Authentication Security",
                                value="**2FA Setting: ON!**\n"
                                      "You are protected against compromised admin accounts!\n"
                                      "__This does not protect against compromised bot accounts.__",
                                inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.send("That's odd. I can't seem to give you that information. "
                           "You better report this in to support.")

    # @commands.command()
    # @commands.has_permissions(manage_channels=True)
    # @commands.guild_only()
    # async def auditlogs(self, ctx):
    #     return None

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def modactions(self, ctx, member: discord.Member = None):
        print(f"The modactions command was requested in {ctx.guild.name}")
        try:
            if member is None:
                member = ctx.author
            entries = await ctx.guild.audit_logs(limit=None, user=member).flatten()
            await ctx.send(f'This user has made {len(entries)} moderation actions.')
        except:
            await ctx.send("I don't have access to view the audit logs. "
                           "Access can be gained by enabling Administrator or "
                           "View Audit Logs setting in the MODUS role")


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Admin_Server_Info(client))
