import os
from pymongo import MongoClient


def get_mongo_conn() -> MongoClient:
    client_url = os.environ.get('CLIENT_URL')
    cluster = MongoClient(client_url)
    return cluster
