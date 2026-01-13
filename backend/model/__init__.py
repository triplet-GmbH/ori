from pymongo import MongoClient
from pymongo.database import Database

from bson import ObjectId
from .. import config


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info):
        if isinstance(v, ObjectId):
            return v
        return ObjectId(v)


def get_database() -> Database:
    return MongoClient(
        host=config.MONGO_HOSTNAME,
        port=config.MONGO_PORT,
        username=config.MONGO_USERNAME,
        password=config.MONGO_PASSWORD,
    )[config.MONGO_DATABASE]


CurrentDB: Database = get_database()
