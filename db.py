import mysql.connector
import logging as logger
import os
from dotenv import load_dotenv

load_dotenv()

USER_DB = os.getenv("USER_DB")
PASSWORD_DB = os.getenv("PASS_DB")
INSTANCE_DB = os.getenv("INSTANCE_DB")
URL_DB = os.getenv("URL_DB")

logger.info("Conectando banco de dados")
class Database:
    __instance = None

    def __init__(self):
        if self.__instance is None or self.__instance.is_connected() == False:
            self.__instance = mysql.connector.connect(
                user=USER_DB,
                password=PASSWORD_DB,
                host=URL_DB,
                database=INSTANCE_DB,
            )
            self.__instance.autocommit = True            
            self.__instance.ping(reconnect=True)

    def query(self, query, autoCommit=None, fetch="ALL"):
        try:
            if not self.__instance.is_connected():
                self.__instance.reconnect()
                
            cursor = self.__instance.cursor()
            result = cursor.execute(query)
            if autoCommit is not None:
                self.__instance.commit()
                operation = True if cursor.lastrowid == 0 else {"id": cursor.lastrowid}
                return {"result": operation}
            fields = [field_md[0] for field_md in cursor.description]
            if fetch != "SINGLE":
                result = [dict(zip(fields, row)) for row in cursor.fetchall()]
                return {"result": result}
            else:
                result = [dict(zip(fields, row)) for row in cursor.fetchone()]
                return {"result": result}
        except Exception as e:
            return {"result": None, "error": e, "query": query}
            logger.error(e)
        finally:
            if self.__instance.is_connected():
                logger.info("Mantendo conexão.")
                # self.__instance.cursor.close()
                # self.__instance.close()
                # logger.debug("Removendo instancia da Database... OK")
