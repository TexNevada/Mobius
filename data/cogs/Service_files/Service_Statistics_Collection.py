# Imports commands
from discord.ext import commands
import json
from data.functions.MySQL_Connector import MyDB
import configparser
config = configparser.ConfigParser()
config.read("./config.ini")
from data.functions.logging import get_log
logger = get_log(__name__)


class Service_Statistics_Collection(commands.Cog):
    def __init__(self, client: commands.Bot) -> None:
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        c = MyDB("essential")
        c.execute("INSERT INTO GuildTable (GuildID, GuildName, GuildOwnerID, GuildOwnerName, GuildJoinDate, GuildShardID) "
                  "VALUES (%s, %s, %s, %s, %s, %s)",
                  (guild.id, guild.name, guild.owner.id, guild.owner.name, guild.me.joined_at, guild.shard_id))
        logger.info(f"{guild.name} invited {config['APP']['Bot_Name']} to their server!")
        c.commit()
        c.close()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        #
        # We delete data on those that do not wish to use this service.
        #
        c = MyDB("essential")
        # Deletes guild ID from the main table
        c.execute("DELETE FROM GuildTable WHERE GuildID = %s", (guild.id,))
        tables = ["Fallout76NewsWebhooks", "ReactionRoles", "Fo76ServerStatusWebhooks"]
        for table in tables:
            try:
                c.execute(f"DELETE FROM {table} WHERE GuildID = %s", (guild.id,))
            except Exception as e:
                logger.info(e)
        c.commit()
        c.close()
        logger.info('The bot has left guild: {}'.format(guild.name))

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        # For information:
        # before = A guild before a change
        # after = A guild after a change
        c = MyDB("essential")
        c.execute("SELECT * FROM GuildTable WHERE GuildID = %s", (after.id,))
        response = c.fetchone()
        if not response:
            try:
                c.execute("INSERT INTO GuildTable (GuildID, GuildName, GuildOwnerID, GuildOwnerName, GuildJoinDate, GuildShardID) "
                          "VALUES (%s, %s, %s, %s, %s, %s)",
                          (after.id, after.name, after.owner.id, after.owner.name, after.me.joined_at, after.shard_id))
                logger.info("============Guild_Update===========")
                logger.info(f"Missing guild data on {after.name}")
                logger.info("Added guild data to the database")
                logger.info("===================================")
            except Exception as e:
                logger.info("======Guild_Update_Failed=======")
                logger.info("Unable to add guild data to the database")
                logger.info(f"Reason: {e}")
                logger.info("===================================")
        try:
            if before.id != after.id:
                c.execute("UPDATE GuildTable SET GuildName = %s WHERE GuildID = %s", (after.name, before.id))
                logger.info("============Guild_Update===========")
                logger.info(f"Updated guild data for {after.name}")
                logger.info(f"Previous name: {before.name}")
                logger.info("===================================")
        except Exception as e:
            logger.info("======Guild_ID_Update_Failed=======")
            logger.info("Unable to fetch guild id")
            logger.info(f"Reason: {e}")
            logger.info("===================================")
        try:
            if before.owner.name != after.owner.name:
                c.execute("UPDATE GuildTable SET GuildOwnerName = %s WHERE GuildOwnerID = %s", (after.owner.name, before.owner.id))
                logger.info("============Guild_Update===========")
                logger.info(f"Updated guild owner name to {after.owner.name}")
                logger.info(f"Previous guild owner name: {before.owner.name}")
                logger.info("===================================")
        except Exception as e:
            logger.info("========Owner_Update_Failed========")
            logger.info("Unable to fetch owner name")
            logger.info(f"Reason: {e}")
            logger.info("===================================")
        try:
            if before.shard_id != after.shard_id:
                c.execute("UPDATE GuildTable SET GuildShardID = %s WHERE GuildID = %s", (after.shard_id, before.id))
                logger.info("============Guild_Update===========")
                logger.info(f"Updated guild shard ID to {after.shard_id}")
                logger.info(f"Previous guild shard ID: {before.shard_id}")
                logger.info("===================================")
        except Exception as e:
            logger.info("========Shard_Update_Failed========")
            logger.info("Unable to fetch shard ID")
            logger.info(f"Reason: {e}")
            logger.info("===================================")

        c.commit()
        c.close()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Service_Statistics_Collection(client))
