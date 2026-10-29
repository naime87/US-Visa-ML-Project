
import sys
import os
import pymongo

from dotenv import load_dotenv
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.constants import DATABASE_NAME, MONGODB_URL_KEY

load_dotenv()


class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)

                if not mongo_db_url:
                    raise ValueError(
                        f"Environment variable {MONGODB_URL_KEY} is missing."
                    )

                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    serverSelectionTimeoutMS=5000
                )

                MongoDBClient.client.admin.command("ping")

                logging.info("MongoDB connection successful")

            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name

        except Exception as e:
            raise USvisaException(e, sys) from e

