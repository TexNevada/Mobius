# Based on Casper's code

async def get_user_from_guild(guild, user_id):
    user = guild.get_member(user_id) # We have the right intents, still returns None sometimes
    if not user:
        user = await guild.fetch_member(user_id)
    return user