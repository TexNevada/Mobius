# Imports commands
from discord.ext import commands
import json
from data.functions.MySQL_Connector import MyDB
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")


class Service_Statistics_Collection(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        c = MyDB("essentials")
        c.execute("INSERT INTO GuildTable (GuildID, GuildName, GuildOwnerID, GuildOwnerName, GuildJoinDate) "
                  "VALUES (%s, %s, %s, %s, %s)",
                  (guild.id, guild.name, guild.owner.id, guild.owner.name, guild.me.joined_at))
        print(f"{guild.name} invited {config['APP']['Bot_Name']} to their server!")
        c.commit()
        c.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        #
        # We delete data on those that do not wish to use this service.
        #
        c = MyDB("essentials")
        # Deletes guild ID from the main table
        c.execute("DELETE FROM GuildTable WHERE GuildID = %s", (guild.id,))
        tables = ["BethesdaTracker", "Fallout76NewsWebhooks", "ReactionRoles", "Fo76ServerStatusWebhooks"]
        for table in tables:
            try:
                c.execute(f"DELETE FROM {table} WHERE GuildID = %s", (guild.id,))
            except Exception as e:
                print(e)
        c.commit()
        c.close()
        print('The bot has left guild: {}'.format(guild.name))

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        # For information:
        # before = A guild before a change
        # after = A guild after a change
        c = MyDB("essentials")
        c.execute("SELECT * FROM GuildTable WHERE GuildID = %s", (after.id,))
        response = c.fetchone()
        if not response:
            c.execute("INSERT INTO GuildTable (GuildID, GuildName, GuildOwnerID, GuildOwnerName, GuildJoinDate) "
                      "VALUES (%s, %s, %s, %s, %s)",
                      (after.id, after.name, after.owner.id, after.owner.name, after.me.joined_at))
            print("============Guild_Update===========")
            print(f"Missing guild data on {after.name}")
            print("Added guild data to the database")
            print("===================================")
        if before.id != after.id:
            c.execute("UPDATE GuildTable SET GuildName = %s WHERE GuildID = %s", (after.name, before.id))
            print("============Guild_Update===========")
            print(f"Updated guild data for {after.name}")
            print(f"Previous name: {before.name}")
            print("===================================")
        if before.owner.name != after.owner.name:
            c.execute("UPDATE GuildTable SET GuildOwnerName = %s WHERE GuildOwnerID = %s", (after.owner.name, before.owner.id))
            print("============Guild_Update===========")
            print(f"Updated guild owner name to {after.owner.name}")
            print(f"Previous guild owner name: {before.owner.name}")
            print("===================================")
        c.commit()
        c.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Service_Statistics_Collection(client))
