"""

This is old code and will most likely be deprecated in the future when discord announces it's reaction roles

"""


# import discord library
import discord
# Imports commands
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import re
# Importing our own MySQL prebuilt connection
import sys
sys.path.append(".")
from data.functions.MySQL_Connector import MyDB


def role_check(sql_results, payload, guild, reaction_type):
    roles = []
    role_names = []
    return_list = [roles, role_names]
    for result in sql_results:
        # First extract the ID
        regex_role = re.search('<@&([0-9]*)>', result['Role'])
        # Get the ID into a variable
        roleID = int(regex_role.group(1))
        # Send the ID back to get the role format
        role = guild.get_role(roleID)
        # Check to see if user has the role already in loop below
        user_roles = guild.get_member(payload.user_id).roles
        has_role = False
        for guild_role in user_roles:
            if guild_role == role:
                has_role = True
                break
        if has_role is False and reaction_type == "add" or has_role is True and reaction_type == "remove":
            # Append the role into a list
            roles.append(role)
            if not result["silent"]:
                role_names.append(role.name)
        else:
            # User has roles already
            pass
    return return_list


def reaction_error_response(error, arg=None, arg2=None, guild_id=None):
    print("==============Reaction=Roles=ERROR==============")
    print(f"Error applies to following server id: {guild_id}")
    response = False
    if error == "dms":
        print("Category: dms")
        print("I am unable to send messages to this user")
        print("This could be caused due to the user blocking the bot")
        print("or the user denies direct messages from the current server")
    elif error == "missing permissions":
        print("Category: missing permissions")
        print("I am unable to apply the current roles")
        print(f"Roles: {arg}")
        print(f"In server: {arg2}")
        print("This is due to missing permissions")
    elif error == "Reaction Server Issue":
        response = f"⚠ There seems to be a permission issue with reaction roles in {arg}. Please contact the local server admin. ⚠"
        print(response)
    elif error == "No messageID":
        response = "No message ID was given. Find out how to get your message ID here: https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID/"
        print(response)
    elif error == "No emoji":
        response = "No emoji was given. You need to add a emoji to your command."
        print(response)
    elif error == "Wrong messageID":
        response = f"{arg} is not a valid message ID. Find out how to get your message ID here: https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID/"
        print(response)
    elif error == "Role exists":
        response = f"Reaction role already exists for this emoji {arg}."
        print(response)
    elif error == "No role":
        response = "No role was given. You need to specify a role."
        print(response)
    elif error == "Role doesn't exist/above modus role":
        response = f"{arg} role does not exist in the current server or could be above the MODUS role."
        print(response)
    elif error == "Cannot manage roles":
        response = "I am unable to manage that role. I am either lacking permissions to do so or the role you are trying to use is above my roles in the settings."
        print(response)
    elif error == "No io":
        response = "You need to state if you want to \"add\" or \"remove\" a reaction role"
        print(response)
    print("======================END========================")
    if response is not False:
        return response


def reaction_response(event, arg=None, arg2=None):
    if event == "Multiple Role Add":
        return f"You received the following roles: **{', '.join(arg)}** in the **{arg2}** discord server."
    elif event == "Role Add":
        return f"You received the following role **{arg}** in the **{arg2}** discord server."
    elif event == "Multiple Role Remove":
        return f"The following roles: **{', '.join(arg)}** was removed in the **{arg2}** discord server."
    elif event == "Role Remove":
        return f"The following role **{arg}** was removed in the **{arg2}** discord server."
    elif event == "Reaction Role Set":
        return f"ReactionRole now set for {arg} with emoji {arg2}."


class reactionrole(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    # Starts a event with the bot
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        c = MyDB("essential")
        c.charset(charset="utf8mb4", collation="utf8mb4_unicode_ci")
        c.execute("SELECT * FROM ReactionRoles WHERE messageID = %s and Emoji = %s", (payload.message_id, str(payload.emoji)))
        results = c.fetchall()
        if results:
            #
            # Code here is for fixing empty fields in the database.
            # ~~~~ This is temporary ~~~~
            for result in results:
                if result["GuildID"] is None:
                    guild = self.client.get_guild(payload.guild_id)
                    c.execute('UPDATE ReactionRoles SET GuildID=%s, GuildName=%s, ChannelName=%s  WHERE messageID=%s and Emoji=%s',
                              (payload.guild_id, guild.name, payload.channel_id, payload.message_id, str(payload.emoji)))
                    c.commit()

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Proper code continues here
            #
            # If the reaction & message ID comes up in the database with a result

            # Gets the guild context by looking up the guild using payload guild ID
            guild = self.client.get_guild(payload.guild_id)
            # Gets the user's by looking the user up using payload user ID
            user = guild.get_member(payload.user_id)
            # Sends results, payload, guild & reaction event for processing roles and role names
            return_list = role_check(results, payload, guild, "add")
            # List of roles from role_check
            roles = return_list[0]
            # List of role names from role_check
            role_names = return_list[1]
            # Prepping for future error check
            error = False
            if roles:
                try:
                    await payload.member.add_roles(*roles, reason=f"Applied Reaction Role for User: {user.name} with user ID: {user.id}.")
                except:
                    reaction_error_response("missing permissions", arg=roles, arg2=guild.name, guild_id=payload.guild_id)
            if role_names and error is False:
                if len(role_names) > 1:
                    try:
                        response = reaction_response("Multiple Role Add", role_names, guild.name)
                        await payload.member.send(response)
                    except:
                        reaction_error_response("dms", guild_id=payload.guild_id)
                else:
                    try:
                        response = reaction_response("Role Add", roles[0], guild.name)
                        await payload.member.send(response)
                    except:
                        reaction_error_response("dms", guild_id=payload.guild_id)
            elif error is True:
                response = reaction_error_response("Reaction Server Issue", guild.name, guild_id=payload.guild_id)
                await user.send(response)
        c.close()

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        c = MyDB("essential")
        c.charset(charset="utf8mb4", collation="utf8mb4_unicode_ci")
        c.execute("SELECT * FROM ReactionRoles WHERE messageID = %s and Emoji = %s", (payload.message_id, str(payload.emoji)))
        results = c.fetchall()
        if results:
            #
            # Code here is for fixing empty fields in the database.
            # ~~~~ This is temporary ~~~~
            for result in results:
                if result["GuildID"] is None:
                    guild = self.client.get_guild(payload.guild_id)
                    c.execute('UPDATE ReactionRoles SET GuildID=%s, GuildName=%s, ChannelName=%s  WHERE messageID=%s and Emoji=%s',
                              (payload.guild_id, guild.name, payload.channel_id, payload.message_id, str(payload.emoji)))
                    c.commit()
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # Proper code continues here
            #
            # If the reaction & message ID comes up in the database with a result

            # Gets the guild context by looking up the guild using payload guild ID
            guild = self.client.get_guild(payload.guild_id)
            # Gets the user's by looking the user up using payload user ID
            user = guild.get_member(payload.user_id)
            # Sends results, payload, guild & reaction event for processing roles and role names
            return_list = role_check(results, payload, guild, "remove")
            # List of roles from role_check
            roles = return_list[0]
            # List of role names from role_check
            role_names = return_list[1]
            # Prepping for future error check
            error = False
            if roles:
                try:
                    await user.remove_roles(*roles, reason=f"Removed Reaction Role for User: {user.name} with user ID: {user.id}.")
                except:
                    reaction_error_response("missing permissions", arg=roles, arg2=guild.name)
                    error = True

            if role_names and error is False:
                if len(role_names) > 1:
                    try:
                        response = reaction_response("Multiple Role Remove", role_names, guild.name)
                        await user.send(response)
                    except:
                        reaction_error_response("dms")
                else:
                    try:
                        response = reaction_response("Role Remove", roles[0], guild.name)
                        await user.send(response)
                    except:
                        reaction_error_response("dms")
            elif error is True:
                response = reaction_error_response("Reaction Server Issue", guild.name)
                await user.send(response)

    @commands.command(aliases=["ReactionRoles", "ReactionRole"])
    @has_permissions(manage_channels=True, manage_roles=True)
    async def reaction_role(self, ctx, io=None, message_id=None, emoji=None, role=None, silent=None):
        none_check = [ctx, message_id, emoji, role, io]
        # Check if one argument is missing
        try:
            io = io.lower()
        except:
            pass
        input_check = False
        if None in none_check:
            if io is None or io not in ["add", "remove"]:
                response = reaction_error_response("No io", guild_id=ctx.guild.id)
                await ctx.send(response)
                input_check = True
            if message_id is None:
                response = reaction_error_response("No messageID", guild_id=ctx.guild.id)
                await ctx.send(response)
                input_check = True
            if emoji is None and io == "add":
                response = reaction_error_response("No emoji", guild_id=ctx.guild.id)
                await ctx.send(response)
                # Make sure user sent a emoji. Could be difficult to do?
            if role is None and io == "add":
                response = reaction_error_response("No role", guild_id=ctx.guild.id)
                await ctx.send(response)
        # Reaction roles code runs here
        if input_check is False:
            c = MyDB("essential")
            c.charset(charset="utf8mb4", collation="utf8mb4_unicode_ci")
            c.execute('SELECT * FROM ReactionRoles where channelID = %s and messageID = %s',
                      (ctx.channel.id, message_id))
            response = c.fetchall()
            if response and io == "remove":
                if emoji is None:
                    c.execute("DELETE FROM ReactionRoles WHERE channelID = %s and messageID = %s", (ctx.channel.id, message_id))
                    await ctx.send(f"All reaction roles to message id {message_id} has now been deleted and you can safely remove the emojis")
                else:
                    c.execute("DELETE FROM ReactionRoles WHERE channelID = %s and messageID = %s and Emoji = %s", (ctx.channel.id, message_id, emoji))
                    await ctx.send(f"Reaction role to {emoji} has now been deleted and you can safely remove the emoji")
                c.commit()
            else:
                c.execute("SELECT * FROM ReactionRoles WHERE channelID = %s and messageID = %s and Emoji = %s", (ctx.channel.id, message_id, emoji))
                response = c.fetchall()
                if response:
                    # Reaction roles exist on the message
                    react_response = reaction_error_response("Role exists", emoji)
                    await ctx.send(react_response)
                    pass
                else:
                    reaction_role = False
                    # role_id = re.search("<@&([0-9]*)>", role)
                    for guild_role in ctx.guild.roles:
                        if guild_role.mention == role:
                            reaction_role = True  # = ctx.guild.get_role(role_id)
                            break
                    if reaction_role is False:
                        # role does not exist in the current server or could be above the bot role?
                        react_response = reaction_error_response("Role doesn't exist/above modus role", role, guild_id=ctx.guild.id)
                        await ctx.send(react_response)
                        pass
                    else:
                        # Checks to see if the bot can manage roles or has administrator role
                        manage_user_roles = False
                        user_permissions = ctx.channel.permissions_for(ctx.guild.me)
                        for permission in user_permissions:
                            perm_check_list = ["manage_roles", "administrator"]
                            if permission[0] in perm_check_list and permission[1] is True:
                                # Bot has manage roles or administrator
                                manage_user_roles = True
                                break
                        if manage_user_roles is False:
                            pass
                            return_response = reaction_error_response("Cannot manage roles", guild_id=ctx.guild.id)
                            await ctx.send(return_response)
                        else:
                            try:
                                message = await ctx.channel.fetch_message(int(message_id))
                            except discord.errors.NotFound:
                                response = reaction_error_response("Wrong messageID", message_id, guild_id=ctx.guild.id)
                                await ctx.send(response)
                            else:
                                if silent is not None:
                                    if silent == "Silent" or silent == "SILENT":
                                        silent = "silent"
                                        sql = "INSERT INTO ReactionRoles (GuildID,GuildName,ChannelID,ChannelName,messageID,Role,Emoji,silent) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                                        sql_values = (ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, message_id, role, emoji, silent)
                                    else:
                                        sql = "INSERT INTO ReactionRoles (GuildID,GuildName,ChannelID,ChannelName,messageID,Role,Emoji) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                                        sql_values = (ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, message_id, role, emoji)

                                else:
                                    sql = "INSERT INTO ReactionRoles (GuildID,GuildName,ChannelID,ChannelName,messageID,Role,Emoji) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                                    sql_values = (ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name, message_id, role, emoji)
                                if '<' not in emoji:
                                    # emoji is text make sure it doesnt match this regex
                                    match = re.search('[a-zA-Z1-9]*', emoji)
                                    if match and match[0] != '':
                                        if '️⃣' not in emoji:
                                            # Emoji is an actual string and not an emoji
                                            # print('Possible false positive emoji: {}'.format(emoji))
                                            pass
                                        await message.add_reaction(emoji)
                                        await ctx.send(f"ReactionRole now set for {role} with emoji: {emoji}.")
                                        c.execute(sql, sql_values)
                                    else:
                                        # TODO: Its not the square emoji and it needs an error output. This needs testing
                                        await ctx.send("Well that\'s odd. Something you did didn't work. Contact support. You can use the `>support` command to get the link for the support server")
                                else:
                                    # customEmoji = True
                                    emoji_check = False
                                    match = re.search('<:(.*):([0-9]*)>', emoji)
                                    # emojiName = match.group(1)
                                    emojiID = match.group(2)
                                    for emoji_entry in self.client.emojis:
                                        if emojiID == emoji_entry.id:
                                            emoji_check = True
                                            c.execute(sql, sql_values)
                                            await message.add_reaction(emoji_entry)
                                            response = reaction_response("Reaction Role Set", role, emoji)
                                            await ctx.send(response)
                                    if emoji_check is False:
                                        try:
                                            c.execute(sql, sql_values)
                                            await message.add_reaction(emoji)
                                            response = reaction_response("Reaction Role Set", role, emoji)
                                            await ctx.send(response)
                                        except:
                                            await ctx.send("The emoji you are using is not from this server and I am there for unable to apply it. "
                                                           "It will still work but you need to add the emoji to the message yourself")

                c.commit()
            c.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(reactionrole(client))
