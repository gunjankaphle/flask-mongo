from pymongo import MongoClient
from config import MongoConfig


def get_connection():
    return MongoClient(MongoConfig.MONGO_URI)
