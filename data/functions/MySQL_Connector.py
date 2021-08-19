import mysql.connector
import configparser


class MyDB:
    def __init__(self, database):
        config = configparser.ConfigParser()
        config.read("./config.ini")
        db = config["Credentials"]
        databases = [key for key in config["Databases"]]
        print(databases)
        if database in databases:
            if db["Active"] == "True":
                self._db_connection = mysql.connector.connect(host=db['IP'],
                                                              user=db['Username'],
                                                              passwd=db['Password'],
                                                              database=config["Databases"][database])
                self._db_cur = self._db_connection.cursor(dictionary=True, buffered=True)
            else:
                raise Exception("Database credentials is not activated. Set the value to True to avoid this error")
        else:
            raise Exception("No Database Found By That Name, Please correct this by adding it to Config.ini")

    def execute(self, sqlQuery, params=None):
        if params:
            return self._db_cur.execute(sqlQuery, params)
        else:
            return self._db_cur.execute(sqlQuery)

    def fetchone(self):
        return self._db_cur.fetchone()

    def fetchall(self):
        return self._db_cur.fetchall()

    ############### CUSTOM QUERIES ##############
    def commit(self):
        self._db_connection.commit()

    def charset(self, charset, collation):
        self._db_connection.set_charset_collation(charset=charset, collation=collation)

    def close(self):
        self._db_connection.close()

    def __del__(self):
        self._db_connection.close()