# MongoDB access layer.

from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME


def get_db():
    return MongoClient(MONGO_URI)[MONGO_DB_NAME]
